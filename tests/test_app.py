from pathlib import Path
from streamlit.testing.v1 import AppTest
from cloudtrack.analytics import load_orders, metrics

APP = str(Path(__file__).resolve().parents[1] / 'app.py')


def test_panel_filters_empty_selection_and_upload_prompt():
    total = len(load_orders((Path(APP).parent / 'data/orders_demo.csv').read_bytes()))
    app = AppTest.from_file(APP).run(timeout=30)
    assert not app.exception
    assert next(item.value for item in app.metric if item.label == 'Pedidos registrados') == str(total)
    app.sidebar.multiselect[0].set_value(['La Paz']).run()
    assert not app.exception
    registered = next(item.value for item in app.metric if item.label == 'Pedidos registrados')
    assert 0 < int(registered.replace(',', '')) < total
    app.sidebar.multiselect[0].set_value([]).run()
    assert not app.exception
    assert 'No hay pedidos' in app.warning[0].value
    app.sidebar.radio[0].set_value('Cargar CSV').run()
    assert not app.exception
    assert 'Seleccione un CSV' in app.info[0].value
    assert any(item.label == 'Descargar CSV de ejemplo' for item in app.get('download_button'))
    assert len(app.sidebar.get('file_uploader')) == 0
    assert len(app.get('file_uploader')) == 1


def test_panel_r2_configuration_error_is_controlled(monkeypatch):
    monkeypatch.delenv('CLOUDTRACK_S3_BUCKET', raising=False)
    app = AppTest.from_file(APP).run(timeout=30)
    app.sidebar.radio[0].set_value('Almacenamiento cloud').run()
    assert not app.exception
    assert not app.error
    assert 'Cloudflare R2' in app.warning[0].value
    assert 'Amazon' not in str([item.value for item in app.markdown])
    assert 'Cómo configurar R2 en local' in [item.label for item in app.expander]


def test_dashboard_kpis_match_filtered_data_and_preserve_all_tabs():
    app = AppTest.from_file(APP).run(timeout=30)
    app.sidebar.multiselect[0].set_value(['La Paz']).run()
    app.sidebar.multiselect[1].set_value(['Hogar']).run()
    assert not app.exception
    data = load_orders((Path(APP).parent / 'data/orders_demo.csv').read_bytes())
    expected = metrics(data.loc[data.city.eq('La Paz') & data.category.eq('Hogar')])
    values = {item.label: item.value for item in app.metric}
    assert values['Ventas entregadas · BOB'] == f"{expected['revenue_bob']:,.2f}"
    assert values['Pedidos entregados'] == str(expected['delivered'])
    assert values['Entregas a tiempo'] == f"{expected['on_time_pct']:.1f}%"
    assert values['Ticket promedio · BOB'] == f"{expected['average_ticket_bob']:,.2f}"
    assert [tab.label for tab in app.tabs] == ['Ventas', 'Entregas', 'Datos y metodología']


def test_dashboard_without_deliveries_uses_explicit_empty_states(monkeypatch):
    content = b'order_id,order_date,city,category,amount_bob,shipping_cost_bob,status,promised_date,delivered_date\nA,2026-01-01,La Paz,Hogar,100,10,cancelado,2026-01-03,\n'
    monkeypatch.setattr('cloudtrack.storage.read_r2_orders', lambda: content)
    app = AppTest.from_file(APP).run(timeout=30)
    app.sidebar.radio[0].set_value('Almacenamiento cloud').run()
    assert not app.exception
    values = {item.label: item.value for item in app.metric}
    assert values['Ventas entregadas · BOB'] == '0.00'
    assert values['Pedidos entregados'] == '0'
    assert values['Entregas a tiempo'] == 'Sin entregas'
    assert values['Ticket promedio · BOB'] == 'Sin entregas'
    assert any('No hay ventas entregadas' in item.value for item in app.info)
    assert not any('<p class="ct-insight-value">' in item.value for item in app.markdown)
