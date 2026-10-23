from datetime import date
import json
from pathlib import Path
import pandas as pd
from streamlit.testing.v1 import AppTest
from cloudtrack.analytics import load_orders
from cloudtrack.reporting import summarize_orders

ROOT = Path(__file__).resolve().parents[1]
APP = str(ROOT / 'app.py')
CSV = '''order_id,order_date,city,category,amount_bob,shipping_cost_bob,status,promised_date,delivered_date
A,2026-01-01,La Paz,Hogar,100,10,entregado,2026-01-03,2026-01-03
B,2026-01-02,Santa Cruz,Moda,200,20,entregado,2026-01-04,2026-01-06
C,2026-01-03,La Paz,Hogar,900,10,cancelado,2026-01-05,
D,2026-01-02,La Paz,Hogar,150,10,entregado,2026-01-03,2026-01-08
'''


def metric(app, label):
    return next(item.value for item in app.metric if item.label == label)


def r2_app(monkeypatch, content=CSV.encode()):
    monkeypatch.setattr('cloudtrack.storage.read_r2_orders', lambda: content)
    app = AppTest.from_file(APP).run(timeout=30)
    app.sidebar.radio[0].set_value('Almacenamiento cloud').run()
    assert not app.exception
    return app


def test_reset_restores_all_filters_after_empty_selection_and_keeps_source(monkeypatch):
    app = r2_app(monkeypatch)
    app.sidebar.multiselect[1].set_value(['Moda']).run()
    app.sidebar.date_input[0].set_value((date(2026, 1, 2), date(2026, 1, 2))).run()
    app.sidebar.multiselect[0].set_value([]).run()
    assert app.warning
    app.sidebar.button[0].click().run()
    assert not app.exception
    assert app.sidebar.radio[0].value == 'Almacenamiento cloud'
    assert app.sidebar.multiselect[0].value == ['La Paz', 'Santa Cruz']
    assert app.sidebar.multiselect[1].value == ['Hogar', 'Moda']
    assert app.sidebar.date_input[0].value == (date(2026, 1, 1), date(2026, 1, 3))
    assert metric(app, 'Pedidos registrados') == '4'


def test_delay_indicators_follow_city_filter_and_no_late_case(monkeypatch):
    app = r2_app(monkeypatch)
    assert metric(app, 'Entregas tardías') == '2'
    assert metric(app, 'Retraso medio entre tardías') == '3.50 días'
    app.sidebar.multiselect[0].set_value(['La Paz']).run()
    assert not app.exception
    assert metric(app, 'Entregas tardías') == '1'
    assert metric(app, 'Retraso medio entre tardías') == '5.00 días'
    app.sidebar.date_input[0].set_value((date(2026, 1, 1), date(2026, 1, 1))).run()
    assert not app.exception
    assert metric(app, 'Entregas tardías') == '0'
    assert metric(app, 'Retraso medio entre tardías') == 'Sin entregas tardías'


def test_date_range_kpi_matches_independent_csv_calculation():
    app = AppTest.from_file(APP).run(timeout=30)
    start, end = date(2026, 2, 1), date(2026, 2, 28)
    app.sidebar.date_input[0].set_value((start, end)).run()
    assert not app.exception
    raw = pd.read_csv(ROOT / 'data/orders_demo.csv')
    selection = raw.loc[raw.order_date.between(start.isoformat(), end.isoformat())]
    delivered = selection.loc[selection.status.eq('entregado')]
    assert metric(app, 'Pedidos registrados') == f'{len(selection):,}'
    assert metric(app, 'Ventas entregadas · BOB') == f'{delivered.amount_bob.sum():,.2f}'
    assert metric(app, 'Entregas tardías') == str((delivered.delivered_date > delivered.promised_date).sum())


def test_new_r2_content_resets_incompatible_filters(monkeypatch):
    app = r2_app(monkeypatch)
    app.sidebar.multiselect[0].set_value(['La Paz']).run()
    replacement = CSV.replace('La Paz', 'Tarija').replace('Santa Cruz', 'Tarija').replace('2026-01-', '2026-02-')
    monkeypatch.setattr('cloudtrack.storage.read_r2_orders', lambda: replacement.encode())
    app.run()
    assert not app.exception
    assert app.sidebar.multiselect[0].value == ['Tarija']
    assert app.sidebar.date_input[0].value == (date(2026, 2, 1), date(2026, 2, 3))
    assert metric(app, 'Pedidos registrados') == '4'
    app.sidebar.radio[0].set_value('Demostración').run()
    assert not app.exception
    assert metric(app, 'Pedidos registrados') == '600'


def test_summary_matches_filtered_selection_and_serializes_empty_values():
    orders = load_orders(CSV.encode())
    selected = orders.loc[orders.city.eq('Santa Cruz')]
    report = json.loads(json.dumps(summarize_orders(selected), allow_nan=False))
    assert report['orders'] == 1
    assert report['cities'] == {'Santa Cruz': 1}
    assert report['delivery_delays'] == {'late_deliveries': 1, 'average_delay_days': 2}
    empty = json.loads(json.dumps(summarize_orders(orders.iloc[:0]), allow_nan=False))
    assert empty['orders'] == 0
    assert empty['order_dates'] == {'from': None, 'to': None}
    assert empty['delivery_delays']['average_delay_days'] is None
