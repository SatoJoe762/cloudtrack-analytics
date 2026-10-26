from io import StringIO
from pathlib import Path
import pandas as pd
import pytest
from cloudtrack.analytics import load_orders, metrics

CSV = '''order_id,order_date,city,category,amount_bob,shipping_cost_bob,status,promised_date,delivered_date
1,2026-01-01,La Paz,Hogar,100,10,entregado,2026-01-03,2026-01-03
2,2026-01-01,La Paz,Hogar,300,20,entregado,2026-01-03,2026-01-05
3,2026-01-01,La Paz,Hogar,900,10,cancelado,2026-01-03,
4,2026-01-01,La Paz,Hogar,800,10,en_transito,2026-01-03,
'''


def test_metrics_exclude_uncompleted_orders_and_include_deadline():
    assert metrics(load_orders(CSV.encode())) == {
        'orders': 4, 'delivered': 2, 'revenue_bob': 400,
        'average_ticket_bob': 200, 'on_time_pct': 50, 'delivery_days': 3,
    }


def test_no_deliveries_and_empty_selection_are_not_zero_percent():
    df = load_orders(CSV.encode())
    for subset in [df[df.status.eq('cancelado')], df.iloc[:0]]:
        result = metrics(subset)
        assert result['revenue_bob'] == 0
        assert result['on_time_pct'] is None
        assert result['delivery_days'] is None
        assert result['average_ticket_bob'] is None


@pytest.mark.parametrize(('column', 'value'), [
    ('order_id', '2'), ('order_id', ''), ('city', ' '), ('category', ''),
    ('amount_bob', '-1'), ('amount_bob', 'inf'), ('shipping_cost_bob', 'NaN'),
    ('status', 'perdido'), ('order_date', '2026-02-30'),
    ('promised_date', ''), ('promised_date', '2025-12-31'),
    ('delivered_date', ''), ('delivered_date', '2025-12-31'),
])
def test_invalid_rows_are_rejected(column, value):
    df = pd.read_csv(StringIO(CSV), dtype=str, keep_default_na=False)
    df.loc[0, column] = value
    with pytest.raises(ValueError):
        load_orders(df.to_csv(index=False).encode())


def test_non_delivered_cannot_have_delivery_date():
    with pytest.raises(ValueError, match='Solo los pedidos'):
        load_orders(CSV.replace('cancelado,2026-01-03,', 'cancelado,2026-01-03,2026-01-04').encode())


@pytest.mark.parametrize('content', [b'', b'foo\nbar\n', CSV.splitlines()[0].encode(), b'\xff'])
def test_invalid_files(content):
    with pytest.raises(ValueError):
        load_orders(content)


def test_size_limit():
    with pytest.raises(ValueError, match='10 MB'):
        load_orders(b'x' * (10 * 1024 * 1024 + 1))


def test_normalization():
    df = load_orders(CSV.replace('La Paz', ' La Paz ').replace('entregado', ' ENTREGADO ').encode())
    assert df.city.eq('La Paz').all()
    assert metrics(df)['delivered'] == 2


def test_demo_contract():
    demo = Path(__file__).resolve().parents[1] / 'data/orders_demo.csv'
    orders = load_orders(demo.read_bytes())
    result = metrics(orders)
    assert result['orders'] > 0
    assert result['on_time_pct'] is None or 0 <= result['on_time_pct'] <= 100


def test_generator_creates_100_reproducible_orders_distinct_from_original_cloud(tmp_path, monkeypatch):
    from scripts import generate_demo
    monkeypatch.setattr(generate_demo, '__file__', str(tmp_path / 'scripts/generate_demo.py'))
    generate_demo.main()
    generated = tmp_path / 'data/orders_demo.csv'
    content = generated.read_bytes()
    orders = load_orders(content)
    assert len(orders) == 100
    reference = load_orders((Path(__file__).resolve().parents[1] / 'data/orders_cloud_reference.csv').read_bytes())
    assert len(reference) == 600
    assert set(orders.order_id).isdisjoint(reference.order_id)
    generate_demo.main()
    assert generated.read_bytes() == content


def test_delay_metrics_average_only_positive_delivered_delays():
    from cloudtrack.analytics import delay_metrics
    content = CSV + '5,2026-01-01,Santa Cruz,Moda,200,10,entregado,2026-01-03,2026-01-08\n'
    result = delay_metrics(load_orders(content.encode()))
    assert result == {'late_deliveries': 2, 'average_delay_days': 3.5}


@pytest.mark.parametrize('selection', ['on_time', 'not_delivered', 'empty'])
def test_delay_metrics_without_late_deliveries(selection):
    from cloudtrack.analytics import delay_metrics
    df = load_orders(CSV.encode())
    subsets = {
        'on_time': df.loc[df['order_id'].eq('1')],
        'not_delivered': df.loc[~df['status'].eq('entregado')],
        'empty': df.iloc[:0],
    }
    assert delay_metrics(subsets[selection]) == {
        'late_deliveries': 0, 'average_delay_days': None,
    }
