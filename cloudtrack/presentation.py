"""Presentación del panel; las fórmulas de KPIs permanecen en analytics."""
import json
from pathlib import Path
import pandas as pd

ASSETS = Path(__file__).resolve().parents[1] / "assets"
TOKENS = json.loads((ASSETS / "design-tokens.json").read_text())
PRIMARY = TOKENS["primary"]
GREEN = TOKENS["success"]
BLUE = TOKENS["secondary"]
STATUS_LABELS = {"entregado": "Entregado", "en_transito": "En tránsito", "cancelado": "Cancelado"}
STATUS_COLORS = {"Entregado": GREEN, "En tránsito": BLUE, "Cancelado": TOKENS["danger"]}


def dashboard_styles():
    """CSS y gráficos comparten los mismos tokens de color locales."""
    variables = ";".join(f"--ct-{name}:{value}" for name, value in TOKENS.items() if isinstance(value, str))
    return ":root{" + variables + "}" + (ASSETS / "dashboard.css").read_text()


def icon(name):
    """Iconos geométricos propios, de trazo uniforme y sin peticiones externas."""
    paths = {
        "chart": '<path d="M4 18V11m8 7V5m8 13v-9M3 22h18"/>',
        "sales": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3 10h18m-6 5h3"/>',
        "box": '<path d="m12 3 9 5v9l-9 5-9-5V8l9-5Zm0 10 9-5M12 13 3 8m9 5v9M7.5 5.5l9 5"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "ticket": '<path d="M4 4h16v5a3 3 0 0 0 0 6v5H4v-5a3 3 0 0 0 0-6V4Zm11 0v3m0 4v2m0 4v3"/>',
        "filter": '<path d="M4 7h16M7 12h10m-7 5h4"/>',
        "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M7 3v4m10-4v4M3 11h18"/>',
        "insight": '<path d="m4 17 6-6 4 3 6-8m-6 0h6v6"/>',
        "warning": '<path d="m12 3 10 18H2L12 3Zm0 6v5m0 3v.1"/>',
        "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def category_colors(categories):
    """Asignación estable para el conjunto completo, incluso después de filtrar."""
    palette = TOKENS["chart-colors"]
    return {name: palette[index % len(palette)] for index, name in enumerate(sorted(categories))}


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


def style_chart(fig, *, height=310, percent=False, horizontal=False):
    """Un mismo lenguaje gráfico y márgenes para todas las vistas."""
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Source Sans 3, sans-serif", color=TOKENS["muted"], size=12),
        margin=dict(l=8, r=36, t=12, b=8),
        hoverlabel=dict(bgcolor=TOKENS["surface"], font_color=TOKENS["ink"], font_size=13, bordercolor=TOKENS["line"]),
        showlegend=False, separators=".,", bargap=0.42,
        modebar=dict(bgcolor="rgba(0,0,0,0)", color=TOKENS["muted"], activecolor=PRIMARY),
    )
    fig.update_xaxes(showgrid=horizontal, gridcolor=TOKENS["line"], zeroline=False, title_font_size=11, automargin=True, tickfont_size=11)
    fig.update_yaxes(showgrid=not horizontal, gridcolor=TOKENS["line"], zeroline=False, title_font_size=11, automargin=True, tickfont_size=11)
    if percent:
        fig.update_xaxes(range=[0, 105], ticksuffix="%", dtick=25)
    return fig
