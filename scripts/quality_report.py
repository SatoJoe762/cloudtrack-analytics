"""Reporte reproducible: python -m scripts.quality_report [archivo.csv] [--json]."""
import argparse
import json
from pathlib import Path
import sys

from cloudtrack.analytics import load_orders
from cloudtrack.reporting import summarize_orders


def build_report(content: bytes) -> dict:
    return summarize_orders(load_orders(content))


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
