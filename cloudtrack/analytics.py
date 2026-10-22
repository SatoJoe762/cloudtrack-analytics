"""Contrato y métricas para un pedido por fila; moneda única: BOB."""
from io import BytesIO
from math import isfinite
import pandas as pd

COLUMNS = ["order_id", "order_date", "city", "category", "amount_bob",
           "shipping_cost_bob", "status", "promised_date", "delivered_date"]
STATUSES = {"entregado", "en_transito", "cancelado"}


def load_orders(content: bytes) -> pd.DataFrame:
    if len(content) > 10 * 1024 * 1024:
        raise ValueError("El CSV supera el límite de 10 MB.")
    try:
        df = pd.read_csv(BytesIO(content), dtype=str, keep_default_na=False)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as exc:
        raise ValueError("CSV ilegible: use UTF-8 y separador coma.") from exc
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError("Faltan columnas: " + ", ".join(sorted(missing)))
    df = df[COLUMNS].copy()
    if df.empty:
        raise ValueError("El archivo no contiene pedidos.")
    for column in COLUMNS:
        df[column] = df[column].str.strip()
    if df["order_id"].eq("").any() or df["order_id"].duplicated().any():
        raise ValueError("Cada pedido debe tener un order_id único y no vacío.")
    for column in ["city", "category"]:
        if df[column].eq("").any():
            raise ValueError(f"{column} no puede estar vacío.")
    df["status"] = df["status"].str.lower()
    if not df["status"].isin(STATUSES).all():
        raise ValueError("status debe ser entregado, en_transito o cancelado.")
    for column in ["amount_bob", "shipping_cost_bob"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        if not (df[column].map(isfinite) & df[column].ge(0)).all():
            raise ValueError(f"{column} debe contener números finitos no negativos.")
    for column in ["order_date", "promised_date", "delivered_date"]:
        original = df[column]
        dates = pd.to_datetime(original, format="%Y-%m-%d", errors="coerce")
        invalid = original.ne("") & dates.isna()
        if column != "delivered_date":
            invalid |= dates.isna()
        if invalid.any():
            raise ValueError(f"{column}: use fechas válidas YYYY-MM-DD.")
        df[column] = dates
    delivered = df["status"].eq("entregado")
    if (delivered & df["delivered_date"].isna()).any():
        raise ValueError("Un pedido entregado necesita delivered_date.")
    if (~delivered & df["delivered_date"].notna()).any():
        raise ValueError("Solo los pedidos entregados pueden tener delivered_date.")
    if (df["promised_date"] < df["order_date"]).any() or (
        df["delivered_date"] < df["order_date"]
    ).any():
        raise ValueError("Las fechas de entrega no pueden preceder al pedido.")
    df["delivery_days"] = (df["delivered_date"] - df["order_date"]).dt.days
    df["on_time"] = delivered & (df["delivered_date"] <= df["promised_date"])
    return df


def metrics(df: pd.DataFrame) -> dict:
    delivered = df.loc[df["status"].eq("entregado")]
    return {
        "orders": len(df),
        "delivered": len(delivered),
        "revenue_bob": float(delivered["amount_bob"].sum()),
        "average_ticket_bob": float(delivered["amount_bob"].mean()) if len(delivered) else None,
        "on_time_pct": float(delivered["on_time"].mean() * 100) if len(delivered) else None,
        "delivery_days": float(delivered["delivery_days"].mean()) if len(delivered) else None,
    }


def delay_metrics(df: pd.DataFrame) -> dict:
    """Retrasos de pedidos entregados; recibe filas validadas por load_orders."""
    delivered = df.loc[df["status"].eq("entregado")]
    delay_days = (delivered["delivered_date"] - delivered["promised_date"]).dt.days
    late_days = delay_days.loc[delay_days.gt(0)]
    return {
        "late_deliveries": len(late_days),
        "average_delay_days": float(late_days.mean()) if len(late_days) else None,
    }
