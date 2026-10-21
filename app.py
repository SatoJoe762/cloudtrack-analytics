from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from botocore.exceptions import BotoCoreError, ClientError
from cloudtrack.analytics import COLUMNS, load_orders, metrics
from cloudtrack.storage import read_s3_orders

st.set_page_config(page_title="CloudTrack Analytics", layout="wide")
st.title("CloudTrack Analytics")
st.write("Comercio electrónico y entregas · Ventas y cumplimiento por ciudad")

with st.sidebar:
    st.header("Datos y filtros")
    source = st.radio("Fuente de datos", ["Demostración", "Cargar CSV", "Amazon S3"])
    uploaded = st.file_uploader("Pedidos en CSV (máximo 10 MB)", type="csv") if source == "Cargar CSV" else None
    st.caption("Sin datos personales. Importes expresados en bolivianos (BOB).")

try:
    if source == "Demostración":
        content = (Path(__file__).parent / "data" / "orders_demo.csv").read_bytes()
        st.info("Datos sintéticos de demostración. No representan una empresa real.")
    elif source == "Cargar CSV":
        if uploaded is None:
            st.info("Seleccione un CSV en el panel lateral para comenzar.")
            st.stop()
        content = uploaded.getvalue()
        st.caption("Archivo cargado solo para esta sesión; no se guarda en S3 ni en el repositorio.")
    else:
        content = read_s3_orders()
        st.caption("Fuente: objeto privado de Amazon S3. Lectura actualizada en cada interacción.")
    orders = load_orders(content)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
except (BotoCoreError, ClientError):
    st.error("No se pudo leer S3. Revise región, credenciales, permiso GetObject y ruta del objeto.")
    st.stop()

with st.sidebar:
    cities = st.multiselect("Ciudades", sorted(orders.city.unique()), default=sorted(orders.city.unique()))
    categories = st.multiselect("Categorías", sorted(orders.category.unique()), default=sorted(orders.category.unique()))
    dates = st.date_input("Fecha del pedido", value=(orders.order_date.min().date(), orders.order_date.max().date()))
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
a, b, c, d = st.columns(4)
a.metric("Pedidos registrados", f"{kpi['orders']:,}")
b.metric("Ventas entregadas · BOB", f"{kpi['revenue_bob']:,.2f}")
c.metric("Entregas a tiempo", f"{kpi['on_time_pct']:.1f}%" if kpi['on_time_pct'] is not None else "Sin entregas")
d.metric("Tiempo medio de entrega", f"{kpi['delivery_days']:.1f} días" if kpi['delivery_days'] is not None else "Sin entregas")
st.caption(f"Puntualidad y tiempo medio calculados sobre {kpi['delivered']} pedidos entregados. Las ventas excluyen cancelados y pedidos en tránsito.")

sales, logistics, detail = st.tabs(["Ventas", "Entregas", "Datos y metodología"])
with sales:
    delivered = filtered.loc[filtered.status.eq("entregado")]
    if delivered.empty:
        st.info("No hay ventas entregadas en esta selección.")
    else:
        daily = delivered.groupby("order_date", as_index=False).amount_bob.sum()
        st.plotly_chart(px.line(daily, x="order_date", y="amount_bob", title="Ventas entregadas por fecha del pedido", labels={"order_date": "Fecha del pedido", "amount_bob": "Ventas (BOB)"}, color_discrete_sequence=["#12624C"]), use_container_width=True)
        by_category = delivered.groupby("category", as_index=False).amount_bob.sum().sort_values("amount_bob")
        st.plotly_chart(px.bar(by_category, x="amount_bob", y="category", orientation="h", title="Ventas por categoría", labels={"amount_bob": "Ventas (BOB)", "category": "Categoría"}, color_discrete_sequence=["#12624C"]), use_container_width=True)
with logistics:
    statuses = filtered.groupby("status").size().reset_index(name="pedidos")
    st.plotly_chart(px.bar(statuses, x="status", y="pedidos", title="Estado de los pedidos", labels={"status": "Estado", "pedidos": "Pedidos"}, color_discrete_sequence=["#12624C"]), use_container_width=True)
    if not delivered.empty:
        city_summary = delivered.groupby("city").agg(entregados=("order_id", "count"), puntualidad=("on_time", "mean"), dias_promedio=("delivery_days", "mean")).reset_index()
        city_summary["puntualidad"] *= 100
        st.dataframe(city_summary.rename(columns={"city": "Ciudad", "entregados": "Entregados", "puntualidad": "A tiempo (%)", "dias_promedio": "Días promedio"}), hide_index=True, use_container_width=True)
with detail:
    st.write("Un pedido por fila. No mezclar monedas. Una entrega es puntual cuando delivered_date ≤ promised_date. El ticket medio usa únicamente pedidos entregados. Los días son calendario y el filtro usa order_date.")
    st.write("Ticket medio entregado (BOB):", f"{kpi['average_ticket_bob']:,.2f}" if kpi['average_ticket_bob'] is not None else "Sin entregas")
    st.dataframe(filtered, hide_index=True, use_container_width=True)
    st.download_button("Descargar pedidos filtrados", filtered[COLUMNS].to_csv(index=False).encode("utf-8"), file_name="cloudtrack_filtrado.csv", mime="text/csv")
