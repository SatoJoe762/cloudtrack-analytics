"""Reporte reproducible: python -m scripts.quality_report [archivo.csv] [--json]."""
import argparse
import json
from pathlib import Path
import sys

from cloudtrack.analytics import STATUSES, delay_metrics, load_orders, metrics


def build_report(content: bytes) -> dict:
    orders = load_orders(content)
    return {
        "validation": "passed",
        "orders": len(orders),
        "order_dates": {
            "from": orders["order_date"].min().date().isoformat(),
            "to": orders["order_date"].max().date().isoformat(),
        },
        "cities": {str(city): int(count) for city, count in orders.groupby("city").size().items()},
        "categories": {str(category): int(count) for category, count in orders.groupby("category").size().items()},
        "statuses": {status: int(orders["status"].eq(status).sum()) for status in sorted(STATUSES)},
        "metrics": metrics(orders),
        "delivery_delays": delay_metrics(orders),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validar un CSV y resumir pedidos y entregas sin modificar el archivo.")
    parser.add_argument("csv", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[1] / "data" / "orders_demo.csv")
    parser.add_argument("--json", action="store_true", help="Mostrar JSON para guardar o comparar el reporte.")
    args = parser.parse_args(argv)
    try:
        with args.csv.open("rb") as source:
            report = build_report(source.read(10 * 1024 * 1024 + 1))
    except (OSError, ValueError) as exc:
        print(f"No se pudo generar el reporte: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False))
        return 0

    print("CloudTrack Analytics · Reporte de calidad y entregas")
    print("Contrato CSV: válido (no se descartaron filas)")
    print(f"Pedidos: {report['orders']}")
    print(f"Fechas de pedido: {report['order_dates']['from']} a {report['order_dates']['to']}")
    for title, field in [("Ciudades", "cities"), ("Categorías", "categories"), ("Estados", "statuses")]:
        print(title + ": " + ", ".join(f"{label}: {count}" for label, count in report[field].items()))
    print(f"Ventas entregadas (BOB): {report['metrics']['revenue_bob']:,.2f}")
    print(f"Entregados: {report['metrics']['delivered']}")
    print(f"Entregados tardíos: {report['delivery_delays']['late_deliveries']}")
    average = report["delivery_delays"]["average_delay_days"]
    print("Retraso medio entre tardíos: " + (f"{average:.2f} días" if average is not None else "Sin entregas tardías"))
    print("El retraso se evalúa solo entre entregados; no reconstruye estados históricos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
