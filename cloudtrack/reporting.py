"""Resumen compartido entre la línea de comandos y el dashboard."""
import pandas as pd
from cloudtrack.analytics import STATUSES, delay_metrics, metrics


def summarize_orders(orders: pd.DataFrame) -> dict:
    """Resume filas ya validadas, después de aplicar los filtros deseados."""
    return {
        "validation": "passed",
        "orders": len(orders),
        "order_dates": {
            "from": orders["order_date"].min().date().isoformat() if len(orders) else None,
            "to": orders["order_date"].max().date().isoformat() if len(orders) else None,
        },
        "cities": {str(city): int(count) for city, count in orders.groupby("city").size().items()},
        "categories": {str(category): int(count) for category, count in orders.groupby("category").size().items()},
        "statuses": {status: int(orders["status"].eq(status).sum()) for status in sorted(STATUSES)},
        "metrics": metrics(orders),
        "delivery_delays": delay_metrics(orders),
    }

