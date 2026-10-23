"""Presentación del panel; las fórmulas de KPIs permanecen en analytics."""
import pandas as pd

GREEN = "#12624C"
BLUE = "#426B91"
STATUS_LABELS = {"entregado": "Entregado", "en_transito": "En tránsito", "cancelado": "Cancelado"}
STATUS_COLORS = {"Entregado": GREEN, "En tránsito": BLUE, "Cancelado": "#8C6B71"}


def selection_insights(df: pd.DataFrame) -> list[dict]:
    """Observaciones descriptivas sobre entregados, con empates y ceros explícitos."""
    delivered = df.loc[df.status.eq("entregado")]
    if delivered.empty:
        return []
    categories = delivered.groupby("category").amount_bob.sum().sort_index()
    maximum = categories.max()
    leaders = categories.index[categories.eq(maximum)].tolist()
    total = categories.sum()
    cities = delivered.groupby("city").on_time.mean().sort_index().mul(100)
    lowest = cities.min()
    lagging = cities.index[cities.eq(lowest)].tolist()
    return [
        {"title": "Mayor venta por categoría" if len(leaders) == 1 else "Categorías con mayor venta (empate)",
         "names": ", ".join(leaders), "value": float(maximum),
         "share": float(maximum / total * 100) if total else None},
        {"title": "Puntualidad de la ciudad" if len(cities) == 1 else (
            "Menor puntualidad por ciudad" if len(lagging) == 1 else "Menor puntualidad por ciudad (empate)"),
         "names": ", ".join(lagging), "value": float(lowest), "share": None},
    ]


def style_chart(fig, *, height=330, percent=False):
    """Un mismo lenguaje gráfico y márgenes para todas las vistas."""
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color="#243D35", size=13),
        margin=dict(l=12, r=18, t=20, b=12),
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#193D31", font_size=14),
        showlegend=False, separators=",.",
        modebar=dict(bgcolor="rgba(0,0,0,0)", color="#5C7169", activecolor=GREEN),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, title_font_size=12, automargin=True)
    fig.update_yaxes(gridcolor="#E5ECE8", zeroline=False, title_font_size=12, automargin=True)
    if percent:
        fig.update_xaxes(range=[0, 105], ticksuffix="%", dtick=25)
    return fig
