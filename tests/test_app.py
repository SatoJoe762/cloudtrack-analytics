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
