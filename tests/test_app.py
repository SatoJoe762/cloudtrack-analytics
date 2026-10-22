from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / 'app.py')


def test_panel_filters_empty_selection_and_upload_prompt():
    app = AppTest.from_file(APP).run(timeout=30)
    assert not app.exception
    assert app.metric[0].value == '600'
    app.sidebar.multiselect[0].set_value(['La Paz']).run()
    assert not app.exception
    assert 0 < int(app.metric[0].value.replace(',', '')) < 600
    app.sidebar.multiselect[0].set_value([]).run()
    assert not app.exception
    assert 'No hay pedidos' in app.warning[0].value
    app.sidebar.radio[0].set_value('Cargar CSV').run()
    assert not app.exception
    assert 'Seleccione un CSV' in app.info[0].value


def test_panel_s3_configuration_error_is_controlled(monkeypatch):
    monkeypatch.delenv('CLOUDTRACK_S3_BUCKET', raising=False)
    app = AppTest.from_file(APP).run(timeout=30)
    app.sidebar.radio[0].set_value('Almacenamiento cloud').run()
    assert not app.exception
    assert 'CLOUDTRACK_S3_BUCKET' in app.error[0].value
