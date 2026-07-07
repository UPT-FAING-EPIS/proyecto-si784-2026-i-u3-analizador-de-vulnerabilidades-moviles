import pytest
from unittest.mock import MagicMock, patch
from app.api.models.supabase_report_model import SupabaseReportModel

@pytest.fixture
def mock_supabase_api():
    with patch("app.api.models.supabase_report_model.create_client") as mock_create, \
         patch("app.api.models.supabase_report_model.ApiSettings") as mock_settings:
        mock_settings.supabase_url = "http://test.com"
        mock_settings.supabase_key = "test_key"
        client = MagicMock()
        mock_create.return_value = client
        yield client

def test_api_model_user_exists(mock_supabase_api):
    model = SupabaseReportModel()
    model.user_exists("uuid-test")
    mock_supabase_api.table.assert_called_with("usuarios")
    mock_supabase_api.table().select.assert_called()

def test_api_model_create_report(mock_supabase_api):
    model = SupabaseReportModel()
    payload = {"user_id": "1", "vulnerabilidad": "Test"}
    model.create_report(payload)
    mock_supabase_api.table.assert_called_with("vulnerabilidades")
    mock_supabase_api.table().insert.assert_called_with(payload)

def test_api_model_initialization_error():
    with patch("app.api.models.supabase_report_model.ApiSettings") as mock_settings:
        mock_settings.supabase_url = None
        mock_settings.supabase_key = None
        with pytest.raises(ValueError, match="son requeridos"):
            SupabaseReportModel()

def test_api_model_user_exists_empty_response(mock_supabase_api):
    model = SupabaseReportModel()
    mock_supabase_api.table().select().eq().limit().execute.return_value = MagicMock(data=[])
    res = model.user_exists("unknown")
    assert res.data == []

def test_api_model_create_report_error(mock_supabase_api):
    model = SupabaseReportModel()
    mock_supabase_api.table().insert().execute.side_effect = Exception("Insert failed")
    with pytest.raises(Exception, match="Insert failed"):
        model.create_report({})