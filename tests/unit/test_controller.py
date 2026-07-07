import pytest
import requests
from unittest.mock import MagicMock, patch
from app.dashboard.controllers.dashboard_controller import DashboardController

@pytest.fixture
def mock_model():
    return MagicMock()

@pytest.fixture
def controller(mock_model):
    # Parcheamos los servicios internos para que sea una prueba unitaria pura
    with patch('app.dashboard.controllers.dashboard_controller.VulnerabilityScanner'), \
         patch('app.dashboard.controllers.dashboard_controller.ApkScanService'), \
         patch('app.dashboard.controllers.dashboard_controller.ReportExportService'), \
         patch('app.dashboard.controllers.dashboard_controller.AnzenApiClient'):
        return DashboardController(mock_model)

def test_login_success(controller, mock_model):
    # Configurar el mock para devolver un usuario
    mock_model.authenticate.return_value.data = [{"id": 1, "username": "testuser"}]
    
    result = controller.login("testuser", "password123")
    
    assert result["username"] == "testuser"
    mock_model.authenticate.assert_called_once_with("testuser", "password123")

def test_signup_empty_fields(controller):
    success, message = controller.signup("", "")
    assert success is False
    assert "Completa usuario" in message

def test_signup_existing_user(controller, mock_model):
    # Simular que el usuario ya existe
    mock_model.user_exists.return_value.data = [{"id": 1}]
    
    success, message = controller.signup("existing", "pass")
    assert success is False
    assert "ya existe" in message

def test_signup_db_error(controller, mock_model):
    # Simular un error de base de datos
    mock_model.user_exists.return_value.data = []
    mock_model.register.side_effect = Exception("DB Error")
    
    success, message = controller.signup("newuser", "pass")
    assert success is False
    assert "No se pudo crear el usuario" in message

def test_fetch_online_list(controller, mock_model):
    # Simular respuesta de usuarios online
    mock_model.get_online_users.return_value.data = [{"username": "admin"}]
    
    users = controller.fetch_online_list()
    assert len(users) == 1
    assert users[0]["username"] == "admin"

def test_fetch_all_reports(controller, mock_model):
    mock_model.get_vulnerabilities.return_value.data = [{"id": 1}]
    
    reports = controller.fetch_all_reports("user-123")
    assert len(reports) == 1

def test_update_ping(controller, mock_model):
    mock_model.update_ping.return_value.data = [{"id": 1}]
    controller.update_user_ping(1)
    mock_model.update_ping.assert_called_once_with(1)

def test_scan_vulnerabilities(controller):
    with patch.object(controller.vulnerability_scanner, 'scan') as mock_scan:
        mock_scan.return_value = [{"vuln": "test"}]
        res = controller.scan_vulnerabilities("user-123", "127.0.0.1")
        assert res == [{"vuln": "test"}]
        mock_scan.assert_called_once_with("127.0.0.1")

def test_fetch_methods(controller, mock_model):
    mock_model.get_apk_scans.return_value.data = []
    mock_model.get_apk_findings.return_value.data = []
    mock_model.get_apk_artifacts.return_value.data = []
    
    assert controller.fetch_apk_scans("user-123") == []
    assert controller.fetch_apk_findings(1) == []
    assert controller.fetch_apk_artifacts(1) == []

def test_build_report_export_pdf(controller):
    with patch.object(controller.report_export_service, 'build_pdf') as mock_pdf, \
         patch.object(controller.report_export_service, 'build_filename') as mock_name:
        mock_pdf.return_value = b"pdf_data"
        mock_name.return_value = "file.pdf"
        
        name, data = controller.build_report_export({"id": 1}, [], [], "pdf")
        assert name == "file.pdf"
        assert data == b"pdf_data"

def test_build_report_export_invalid_format(controller):
    with pytest.raises(ValueError, match="Formato de exportacion no soportado"):
        controller.build_report_export({}, [], [], "invalid_format")

def test_create_apk_scan_invalid_file(controller):
    mock_file = MagicMock()
    with patch.object(controller.apk_scan_service, 'validate_apk_file') as mock_val:
        mock_val.return_value = (False, "Error")
        ok, msg = controller.create_apk_scan(1, mock_file)
        assert ok is False
        assert msg == "Error"

def test_create_apk_scan_success(controller, mock_model):
    mock_file = MagicMock()
    analysis_mock = MagicMock(status="completed", summary="Success", findings=[], artifacts=[])
    
    with patch.object(controller.apk_scan_service, 'validate_apk_file', return_value=(True, "OK")), \
         patch.object(controller.apk_scan_service, 'build_scan_payload', return_value=({"id": 1}, b"bytes")), \
         patch.object(controller.apk_scan_service, 'analyze', return_value=analysis_mock), \
         patch.object(controller.apk_scan_service, 'build_scan_update_payload', return_value={}), \
         patch.object(controller.apk_scan_service, 'build_finding_payloads', return_value=[]), \
         patch.object(controller.apk_scan_service, 'build_artifact_payloads', return_value=[]):
        
        mock_model.create_apk_scan.return_value.data = [{"id": "scan-123"}]
        
        ok, msg = controller.create_apk_scan(1, mock_file)
        
        assert ok is True
        assert msg == {"message": "Success", "scan_id": "scan-123"}
        mock_model.create_apk_scan.assert_called_once()
        mock_model.update_apk_scan.assert_called()

def test_create_apk_scan_db_error(controller, mock_model):
    mock_file = MagicMock()
    with patch.object(controller.apk_scan_service, 'validate_apk_file', return_value=(True, "OK")), \
         patch.object(controller.apk_scan_service, 'build_scan_payload', return_value=({}, b"")):
        mock_model.create_apk_scan.return_value.data = []
        ok, msg = controller.create_apk_scan(1, mock_file)
        assert ok is False
        assert "No se pudo registrar" in msg

def test_analizar_repo_github_success(controller):
    with patch.object(controller.anzen_api_client, 'analizar_repo_github') as mock_call:
        mock_call.return_value = {
            "status": "success",
            "project_name": "usuario/repo",
            "loc": 100,
            "complexity": 10,
            "code_smells": 3,
        }
        ok, result = controller.analizar_repo_github("https://github.com/usuario/repo")
        assert ok is True
        assert result["proyecto"] == "usuario/repo"
        assert result["lineas_codigo"] == 100
        assert result["code_smells"] == 3
        mock_call.assert_called_once_with("https://github.com/usuario/repo")

def test_analizar_repo_github_normaliza_code_smells_objeto(controller):
    with patch.object(controller.anzen_api_client, 'analizar_repo_github') as mock_call:
        mock_call.return_value = {
            "status": "success",
            "project_name": "usuario/repo",
            "loc": 100,
            "complexity": 10,
            "code_smells": {"smells": ["a", "b"], "metrics": {}, "files": []},
        }
        ok, result = controller.analizar_repo_github("https://github.com/usuario/repo")
        assert ok is True
        assert result["code_smells"] == 2

def test_analizar_repo_github_http_error(controller):
    response = MagicMock()
    response.json.return_value = {"detail": "Repositorio no encontrado."}
    error = requests.exceptions.HTTPError(response=response)
    with patch.object(controller.anzen_api_client, 'analizar_repo_github', side_effect=error):
        ok, message = controller.analizar_repo_github("https://github.com/usuario/repo")
        assert ok is False
        assert "Repositorio no encontrado" in message

def test_analizar_repo_github_connection_error(controller):
    with patch.object(controller.anzen_api_client, 'analizar_repo_github', side_effect=requests.exceptions.ConnectionError("boom")):
        ok, message = controller.analizar_repo_github("https://github.com/usuario/repo")
        assert ok is False
        assert "No se pudo contactar" in message

def test_create_apk_scan_rls_error(controller, mock_model):
    mock_file = MagicMock()
    with patch.object(controller.apk_scan_service, 'validate_apk_file', return_value=(True, "OK")), \
         patch.object(controller.apk_scan_service, 'build_scan_payload', side_effect=Exception("row-level security error")):
        
        ok, msg = controller.create_apk_scan(1, mock_file)
        assert ok is False
        assert "Supabase bloqueo el registro por RLS" in msg