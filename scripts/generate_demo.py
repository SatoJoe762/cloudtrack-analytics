"""Genera datos sintéticos reproducibles sin dependencias externas."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path


def main():
    rng = random.Random(42)
    target = Path(__file__).resolve().parents[1] / "data" / "orders_demo.csv"
    target.parent.mkdir(exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as output:
        fields = ["order_id", "order_date", "city", "category", "amount_bob", "shipping_cost_bob", "status", "promised_date", "delivered_date"]
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for i in range(1, 601):
            ordered = date(2026, 1, 1) + timedelta(days=rng.randrange(90))
            promised = ordered + timedelta(days=rng.randint(2, 6))
            status = rng.choices(["entregado", "en_transito", "cancelado"], weights=[85, 10, 5])[0]
            delivered = ordered + timedelta(days=rng.randint(1, 8)) if status == "entregado" else None
            writer.writerow(dict(order_id=f"CT-{i:05}", order_date=ordered.isoformat(), city=rng.choice(["La Paz", "Cochabamba", "Santa Cruz"]), category=rng.choice(["Tecnología", "Hogar", "Moda", "Deportes"]), amount_bob=f"{rng.randint(5000, 200000)/100:.2f}", shipping_cost_bob=f"{rng.randint(1000, 5000)/100:.2f}", status=status, promised_date=promised.isoformat(), delivered_date=delivered.isoformat() if delivered else ""))
    print(f"600 pedidos sintéticos: {target}")


if __name__ == "__main__":
    main()
