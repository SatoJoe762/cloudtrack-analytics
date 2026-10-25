from pathlib import Path
from hashlib import sha256
import json
from html import escape
import pandas as pd
import plotly.express as px
import streamlit as st
from botocore.exceptions import BotoCoreError, ClientError
from cloudtrack.analytics import COLUMNS, delay_metrics, load_orders, metrics
from cloudtrack.reporting import summarize_orders
from cloudtrack.storage import R2ConfigurationError, read_r2_orders
from cloudtrack.presentation import PRIMARY, BLUE, STATUS_LABELS, STATUS_COLORS, category_colors, dashboard_styles, icon, selection_insights, style_chart

st.set_page_config(page_title="CloudTrack Analytics", page_icon=":material/monitoring:", layout="wide")
st.markdown("<style>" + dashboard_styles() + "</style>", unsafe_allow_html=True)
header = st.empty()

with st.sidebar:
    st.markdown(f'<div class="ct-brand"><span class="ct-brand-mark">{icon("chart")}</span>'
                '<div>CloudTrack<span>Analytics</span></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ct-sidebar-view">{icon("chart")}<span>Panel de análisis</span></div>', unsafe_allow_html=True)
    st.header("Datos y filtros")
    with st.container(key="source_panel"):
        st.markdown('<h3 class="ct-source-panel-title">Fuente de datos</h3>'
                    '<p class="ct-source-panel-help">Elige el origen de los pedidos que quieres analizar.</p>', unsafe_allow_html=True)
        source = st.radio(
            "Fuente de datos", ["Demostración", "Cargar CSV", "Almacenamiento cloud"],
            captions=["Usa datos de ejemplo para explorar el sistema",
                      "Importa datos desde un archivo local",
                      "Conecta una fuente remota o alojada en la nube"],
            label_visibility="collapsed", width="stretch",
        )

source_name = {"Demostración": "Datos de demostración", "Cargar CSV": "CSV de esta sesión"}.get(source)
if source_name is None:
    source_name = "Cloudflare R2"
header.markdown(f'''<div class="ct-header"><div><h1>Resumen de operaciones</h1>
<p>Una mirada a tus ventas y al cumplimiento de tus entregas.</p></div>
<div class="ct-source">{icon("database")}<span>{escape(source_name)}</span></div></div>''', unsafe_allow_html=True)

uploaded = None
if source == "Cargar CSV":
    st.subheader("Carga tus pedidos")
    st.write("Selecciona un archivo CSV para generar el análisis. Usa el ejemplo si quieres probar el formato.")
    uploaded = st.file_uploader("Selecciona tu archivo CSV (máximo 10 MB)", type="csv", key="orders_upload")
    st.download_button("Descargar CSV de ejemplo", (Path(__file__).parent / "data/orders_demo.csv").read_bytes(), file_name="cloudtrack_ejemplo.csv", mime="text/csv")
    st.caption("Formato UTF-8, separado por comas. Un pedido por fila. El archivo solo se analiza en esta sesión y no se guarda en R2.")

try:
    if source == "Demostración":
        content = (Path(__file__).parent / "data" / "orders_demo.csv").read_bytes()
        st.caption("Datos sintéticos de demostración. No representan una empresa real.")
    elif source == "Cargar CSV":
        if uploaded is None:
            st.info("Seleccione un CSV arriba para comenzar. También puede descargar y cargar el ejemplo.")
            st.stop()
        content = uploaded.getvalue()
        st.caption("Archivo cargado solo para esta sesión; no se guarda en el bucket cloud ni en el repositorio.")
    else:
        with st.spinner("Leyendo pedidos de Cloudflare R2…"):
            content = read_r2_orders()
        st.caption(f"Fuente: {source_name} · Lectura de un bucket privado. El panel no modifica el archivo.")
    orders = load_orders(content)
except R2ConfigurationError:
    st.warning("La conexión con Cloudflare R2 aún no está configurada.")
    st.info("Puedes usar Demostración o Cargar CSV mientras configuras la conexión. La configuración de Streamlit publicado y la de tu equipo son independientes.")
    with st.expander("Cómo configurar R2 en local"):
        st.write("Copia .streamlit/secrets.toml.example como .streamlit/secrets.toml, completa las credenciales de lectura de Cloudflare R2 y reinicia Streamlit. Ese archivo privado no se sube a GitHub.")
    st.stop()
except ValueError as exc:
    st.error(str(exc))
    st.stop()
except (BotoCoreError, ClientError):
    st.error("No se pudo leer el almacenamiento cloud. Revise endpoint, credenciales de lectura, bucket y ruta del objeto.")
    st.stop()

filter_defaults = {
    "filter_cities": sorted(orders.city.unique()),
    "filter_categories": sorted(orders.category.unique()),
    "filter_dates": (orders.order_date.min().date(), orders.order_date.max().date()),
}


def reset_filters():
    for key, value in filter_defaults.items():
        st.session_state[key] = value


# Cambiar de fuente o CSV requiere opciones y fechas compatibles con el nuevo conjunto.
dataset_signature = (source, sha256(content).hexdigest())
if st.session_state.get("filter_dataset") != dataset_signature:
    reset_filters()
    st.session_state["filter_dataset"] = dataset_signature

with st.sidebar:
    st.markdown(f'<div class="ct-sidebar-section">{icon("filter")}<span>Filtrar selección</span></div>', unsafe_allow_html=True)
    cities = st.multiselect("Ciudades", filter_defaults["filter_cities"], default=filter_defaults["filter_cities"], key="filter_cities")
    categories = st.multiselect("Categorías", filter_defaults["filter_categories"], default=filter_defaults["filter_categories"], key="filter_categories")
    dates = st.date_input("Fecha del pedido", value=filter_defaults["filter_dates"], key="filter_dates", format="DD/MM/YYYY")
    st.button("Restablecer filtros", on_click=reset_filters, icon=":material/restart_alt:")
    st.markdown('<div class="ct-sidebar-note">Los filtros se aplican a todas las pestañas y descargas.</div>'
                '<div class="ct-sidebar-footer">CloudTrack Analytics<span>Ventas y entregas · BOB</span></div>', unsafe_allow_html=True)
if len(dates) != 2:
    st.info("Complete el rango de fechas para ver los resultados.")
    st.stop()
filtered = orders.loc[
    orders.city.isin(cities) & orders.category.isin(categories)
    & orders.order_date.between(pd.Timestamp(dates[0]), pd.Timestamp(dates[1]))
].copy()
if filtered.empty:
    st.warning("No hay pedidos con estos filtros. Amplíe el rango o seleccione otras ciudades.")
    st.stop()

kpi = metrics(filtered)
active_filters = sum((set(cities) != set(filter_defaults["filter_cities"]),
                      set(categories) != set(filter_defaults["filter_categories"]),
                      tuple(dates) != filter_defaults["filter_dates"]))
st.markdown(f'<div class="ct-selection"><div class="ct-date">{icon("calendar")}'
            f'<span>{dates[0]:%d/%m/%Y} — {dates[1]:%d/%m/%Y}</span></div>'
            f'<div class="ct-selection-detail">{len(cities)} ciudades · {len(categories)} categorías · '
            f'<strong>{len(filtered):,}</strong> de {len(orders):,} pedidos</div>'
            f'<span class="ct-filter-state">{active_filters} filtros activos</span></div>', unsafe_allow_html=True)
with st.container(key="kpis"):
    cards = [
        ("sales", "Ventas entregadas · BOB", f"{kpi['revenue_bob']:,.2f}", "Importe total, sin costo de envío", "Suma de importes de pedidos entregados, sin envío."),
        ("box", "Pedidos entregados", f"{kpi['delivered']:,}", f"De {kpi['orders']:,} pedidos registrados", "Cantidad de pedidos con estado entregado."),
        ("clock", "Entregas a tiempo", f"{kpi['on_time_pct']:.1f}%" if kpi['on_time_pct'] is not None else "Sin entregas", "En la fecha prometida o antes", "Entregados en la fecha prometida o antes / total de entregados."),
        ("ticket", "Ticket promedio · BOB", f"{kpi['average_ticket_bob']:,.2f}" if kpi['average_ticket_bob'] is not None else "Sin entregas", "Importe medio por pedido entregado", "Ventas entregadas / total de pedidos entregados."),
    ]
    for column, (symbol, label, value, context, help_text) in zip(st.columns(4), cards):
        with column, st.container(key=f"kpi_{symbol}"):
            st.markdown(f'<span class="ct-kpi-icon">{icon(symbol)}</span>', unsafe_allow_html=True)
            st.metric(label, value, help=help_text)
            st.caption(context)
st.caption(f"Base de cálculo: {kpi['delivered']:,} pedidos entregados. Ventas y ticket excluyen cancelados y pedidos en tránsito.")

insights = selection_insights(filtered)
if insights:
    with st.container(key="insights"):
        st.markdown(f'<h2 class="ct-insights-heading">{icon("insight")}Lectura de la selección</h2>', unsafe_allow_html=True)
        left, right = st.columns(2, gap="large")
        for index, (column, insight) in enumerate(zip((left, right), insights)):
            if index == 0:
                detail_text = f"BOB {insight['value']:,.2f} en ventas entregadas"
                if insight["share"] is not None:
                    detail_text += f" · {insight['share']:.1f}% del total" + (" por cada categoría indicada." if "empate" in insight["title"] else ".")
                else:
                    detail_text += ". El total de ventas es cero."
            else:
                detail_text = f"{insight['value']:.1f}% de sus entregados llegaron a tiempo."
            symbol = "insight" if index == 0 else "warning"
            column.markdown(f'''<div class="ct-insight ct-insight-{index}"><span class="ct-insight-icon">{icon(symbol)}</span><div><p class="ct-insight-title">{escape(insight['title'])}</p>
<p class="ct-insight-value">{escape(insight['names'])}</p>
<p class="ct-insight-detail">{escape(detail_text)}</p></div></div>''', unsafe_allow_html=True)
        st.caption(f"Lectura descriptiva sobre {kpi['delivered']:,} entregados de la selección. No implica causalidad ni predicción.")

sales, logistics, detail = st.tabs(["Ventas", "Entregas", "Datos y metodología"])
delivered = filtered.loc[filtered.status.eq("entregado")]
chart_config = {"displaylogo": False, "scrollZoom": False, "locale": "es", "toImageButtonOptions": {"format": "png", "scale": 2}}
with sales:
    st.subheader("Cómo se distribuyen las ventas")
    st.caption("Importes de pedidos entregados, agrupados por la fecha en que se hizo el pedido.")
    if delivered.empty:
        st.info("No hay ventas entregadas en esta selección. Amplía las fechas o cambia los filtros.")
    else:
        daily = delivered.groupby("order_date", as_index=False).amount_bob.sum()
        by_category = delivered.groupby("category", as_index=False).amount_bob.sum().sort_values("amount_bob")
        trend, categories_chart = st.columns([3, 2], gap="large")
        with trend, st.container(key="chart_trend"):
            st.markdown("### Ventas en el tiempo")
            st.caption("Evolución diaria · Ventas entregadas en BOB")
            fig = px.area(daily, x="order_date", y="amount_bob", labels={"order_date": "Fecha del pedido", "amount_bob": "Ventas (BOB)"}, color_discrete_sequence=[PRIMARY])
            fig.update_traces(line_width=2.5, fillcolor="rgba(79,70,229,0.08)", hovertemplate="%{x|%d/%m/%Y}<br>BOB %{y:,.2f}<extra></extra>")
            fig.update_layout(hovermode="x unified")
            fig.update_xaxes(tickformat="%d/%m", nticks=6)
            fig.update_yaxes(rangemode="tozero", tickformat="~s")
            st.plotly_chart(style_chart(fig), width="stretch", theme=None, config=chart_config, key="sales_trend")
        with categories_chart, st.container(key="chart_categories"):
            st.markdown("### Ventas por categoría")
            st.caption("Comparación de importes entregados · BOB")
            fig = px.bar(by_category, x="amount_bob", y="category", orientation="h", color="category", color_discrete_map=category_colors(orders.category.unique()), labels={"amount_bob": "Ventas (BOB)", "category": ""})
            fig.update_traces(hovertemplate="%{y}<br>BOB %{x:,.2f}<extra></extra>")
            fig.update_xaxes(rangemode="tozero", tickformat="~s", nticks=4)
            st.plotly_chart(style_chart(fig, height=max(310, len(by_category) * 42), horizontal=True), width="stretch", theme=None, config=chart_config, key="sales_categories")
        st.caption("Las fechas sin pedidos entregados no tienen observaciones; las líneas conectan los días disponibles.")
with logistics:
    st.subheader("Del pedido a la entrega")
    delays = delay_metrics(filtered)
    with st.container(key="delivery_metrics"):
        late_count, late_average, delivery_average = st.columns(3)
        late_count.metric("Entregas tardías", f"{delays['late_deliveries']:,}")
        late_average.metric("Retraso medio entre tardías", f"{delays['average_delay_days']:.2f} días" if delays['average_delay_days'] is not None else "Sin entregas tardías")
        delivery_average.metric("Tiempo medio de entrega", f"{kpi['delivery_days']:.1f} días" if kpi['delivery_days'] is not None else "Sin entregas", help="Días calendario desde el pedido hasta la entrega real; incluye todos los entregados.")
    st.caption("Entregas tardías y retraso medio: solo entregados después de la fecha prometida. Tiempo medio de entrega: todos los entregados, desde el pedido hasta su entrega real.")
    status_chart, city_chart = st.columns([2, 3], gap="large")
    with status_chart, st.container(key="chart_status"):
        st.markdown("### Estado de los pedidos")
        st.caption("Distribución de todos los pedidos seleccionados")
        statuses = filtered.groupby("status").size().reset_index(name="pedidos")
        statuses["Estado"] = statuses.status.map(STATUS_LABELS)
        fig = px.bar(statuses, x="pedidos", y="Estado", orientation="h", color="Estado", color_discrete_map=STATUS_COLORS, text="pedidos", labels={"pedidos": "Pedidos", "Estado": ""})
        fig.update_traces(textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x} pedidos<extra></extra>")
        fig.update_xaxes(rangemode="tozero")
        st.plotly_chart(style_chart(fig, horizontal=True), width="stretch", theme=None, config=chart_config, key="order_status")
    with city_chart, st.container(key="chart_cities"):
        st.markdown("### Puntualidad por ciudad")
        st.caption("Porcentaje a tiempo · Solo pedidos entregados")
        if delivered.empty:
            st.info("No hay entregados para comparar puntualidad entre ciudades.")
        else:
            city_summary = delivered.groupby("city").agg(entregados=("order_id", "count"), puntualidad=("on_time", "mean"), dias_promedio=("delivery_days", "mean")).reset_index()
            city_summary["puntualidad"] *= 100
            ranked = city_summary.sort_values("puntualidad")
            fig = px.bar(ranked, x="puntualidad", y="city", orientation="h", text="puntualidad", custom_data=["entregados"], labels={"puntualidad": "Entregas a tiempo (%)", "city": ""}, color_discrete_sequence=[BLUE])
            fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside", cliponaxis=False, hovertemplate="%{y}<br>%{x:.1f}% a tiempo<br>%{customdata[0]} entregados<extra></extra>")
            st.plotly_chart(style_chart(fig, height=max(310, len(ranked) * 42), percent=True, horizontal=True), width="stretch", theme=None, config=chart_config, key="city_on_time")
    if not delivered.empty:
        st.markdown("### Detalle de cumplimiento")
        st.dataframe(city_summary.rename(columns={"city": "Ciudad", "entregados": "Entregados", "puntualidad": "A tiempo (%)", "dias_promedio": "Días promedio"}), hide_index=True, width="stretch", column_config={"A tiempo (%)": st.column_config.NumberColumn(format="%.1f %%"), "Días promedio": st.column_config.NumberColumn(format="%.2f")})
with detail:
    st.subheader("Datos que puedes verificar")
    st.success(f"CSV validado: {len(orders):,} pedidos. Selección actual: {len(filtered):,} pedidos.")
    st.metric("Pedidos registrados", f"{kpi['orders']:,}", help="Incluye entregados, en tránsito y cancelados en la selección.")
    st.caption(f"Fuente actual: {source_name}. Las descargas contienen únicamente la selección de filtros activa.")
    report = summarize_orders(filtered)
    export_csv, export_json = st.columns(2)
    export_csv.download_button("Descargar pedidos filtrados", filtered[COLUMNS].to_csv(index=False).encode("utf-8"), file_name="cloudtrack_filtrado.csv", mime="text/csv", width="stretch")
    export_json.download_button("Descargar reporte de la selección (JSON)", json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), file_name="cloudtrack_reporte.json", mime="application/json", width="stretch")
    st.dataframe(filtered[COLUMNS], hide_index=True, width="stretch")
    with st.expander("Cómo calculamos los indicadores"):
        st.write("Un pedido por fila. No mezclar monedas. Una entrega es puntual cuando delivered_date ≤ promised_date. El ticket medio usa únicamente pedidos entregados. Los días son calendario y el filtro usa order_date.")
        st.write("Ticket medio entregado (BOB):", f"{kpi['average_ticket_bob']:,.2f}" if kpi['average_ticket_bob'] is not None else "Sin entregas")
        st.caption("La puntualidad excluye cancelados y pedidos en tránsito. Estos resultados describen la selección; no establecen causas ni predicen entregas futuras.")
    with st.expander("Resumen de la selección"):
        st.json(report, expanded=False)

st.markdown('<div class="ct-footer">CloudTrack Analytics · Proyecto académico de Computación en la Nube. '
            'Usar datos sintéticos o autorizados para publicación. Importes en bolivianos (BOB).</div>', unsafe_allow_html=True)
