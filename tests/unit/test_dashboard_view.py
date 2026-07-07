import pytest
from unittest.mock import MagicMock, patch
from app.dashboard.views.dashboard_view import DashboardView

@pytest.fixture
def view():
    return DashboardView()

@patch("app.dashboard.views.dashboard_view.st")
def test_render_login(mock_st, view):
    # Configurar mocks para tabs e inputs
    mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
    mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
    mock_st.text_input.return_value = "test_val"
    mock_st.button.return_value = True

    controller = MagicMock()
    controller.fetch_global_apk_scans.return_value = []

    res = view.render_login(controller)
    assert len(res) == 6
    assert mock_st.markdown.called

@patch("app.dashboard.views.dashboard_view.st")
@patch("app.dashboard.views.dashboard_view.os.path.exists")
@patch("app.dashboard.views.dashboard_view.os.path.getsize")
@patch("app.dashboard.views.dashboard_view.pd.DataFrame")
@patch("builtins.open", new_callable=MagicMock)
def test_render_dashboard(mock_open, mock_df, mock_getsize, mock_exists, mock_st, view):
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    mock_df.return_value.columns = ["severity_max", "file_name", "id", "dispositivo"] # Asegurar que los checks de columnas pasen
    mock_st.columns.side_effect = [
        [MagicMock(), MagicMock(), MagicMock(), MagicMock()], # Métricas inicio (c1, c2, c3, c4)
        [MagicMock(), MagicMock()]  # Columnas descarga y tabla (col_apk, col_info)
    ]
    mock_st.sidebar = MagicMock()
    mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
    
    # Configurar botones para que entren en las ramas de lógica
    # 1. Analizar APK, 2. Descargar CSV, 3. Descargar JSON, 4. Escanear manual
    mock_st.button.side_effect = [False, True, True, True] 

    # Simular session_state
    mock_st.session_state = MagicMock()
    def session_state_get(key, default=None):
        data = {
            "nav_section": "inicio",
            "online_users": [],
            "scan_results": []
        }
        return data.get(key, default)
    mock_st.session_state.get.side_effect = session_state_get

    # Mock para el selectbox para evitar KeyError
    mock_st.selectbox.return_value = "test.apk | 2023-01-01 | 0 hallazgos"

    # Configurar controlador para evitar ValueError en el unpacking
    controller = MagicMock()
    controller.create_apk_scan.return_value = (True, "Analysis Success")
    controller.fetch_apk_findings.return_value = []
    controller.fetch_apk_artifacts.return_value = []
    controller.build_report_export.return_value = ("report.csv", b"csv,data")

    user = {"username": "admin", "id": "user-123"}
    reports = [{"dispositivo": "Android", "vulnerabilidad": "SSL", "nivel": "Alto", "fecha": "2023-01-01"}]
    apk_scans = [{"id": 1, "file_name": "test.apk", "findings_count": 0, "severity_max": "Info", "created_at": "2023-01-01"}]

    view.render_dashboard(user, reports, apk_scans, controller)
    assert mock_st.markdown.called
    assert mock_st.columns.called
    assert mock_st.dataframe.called

@patch("app.dashboard.views.dashboard_view.st")
def test_render_apk_download(mock_st, view):
    # Mock del contexto de apertura de archivo
    with patch("builtins.open", MagicMock()):
        view.render_apk_download("dummy.apk", "Anzen.apk")
        assert mock_st.download_button.called
        args, kwargs = mock_st.download_button.call_args
        assert kwargs['file_name'] == "Anzen.apk"