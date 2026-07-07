import pytest
from unittest.mock import MagicMock, patch
from app.dashboard.models.supabase_model import SupabaseModel

@pytest.fixture
def mock_supabase():
    with patch('app.dashboard.models.supabase_model.create_client') as mock_create, \
         patch('app.dashboard.models.supabase_model.get_supabase_settings') as mock_settings:
        mock_settings.return_value = {"url": "http://test.com", "key": "test_key"}
        client = MagicMock()
        mock_create.return_value = client
        yield client

def test_model_initialization(mock_supabase):
    model = SupabaseModel()
    assert model.supabase == mock_supabase

def test_authenticate(mock_supabase):
    model = SupabaseModel()
    model.authenticate("user", "pass")
    mock_supabase.table.assert_called_with("usuarios")
    mock_supabase.table.return_value.select.assert_called()

def test_update_ping(mock_supabase):
    model = SupabaseModel()
    model.update_ping("uuid-123")
    mock_supabase.table.return_value.update.assert_called()
    mock_supabase.table.return_value.update.return_value.eq.assert_called_with("id", "uuid-123")

def test_get_vulnerabilities(mock_supabase):
    model = SupabaseModel()
    model.get_vulnerabilities("user-123")
    mock_supabase.table.assert_called_with("vulnerabilidades")
    mock_supabase.table.return_value.select.assert_called_with("*")
    mock_supabase.table.return_value.select.return_value.eq.assert_called_with("user_id", "user-123")
    mock_supabase.table.return_value.select.return_value.eq.return_value.order.assert_called_with("fecha", desc=True)

def test_apk_operations(mock_supabase):
    model = SupabaseModel()
    
    model.get_apk_scans("user-123")
    mock_supabase.table.assert_any_call("apk_scans")
    mock_supabase.table.return_value.select.return_value.eq.assert_any_call("user_id", "user-123")
    
    model.create_apk_scan({"test": 1})
    mock_supabase.table.return_value.insert.assert_called_with({"test": 1})
    
    model.get_apk_findings("id-1")
    mock_supabase.table.return_value.select.return_value.eq.assert_any_call("scan_id", "id-1")

    model.update_apk_scan("scan-1", {"status": "ok"})
    mock_supabase.table.return_value.update.assert_called_with({"status": "ok"})

    model.get_apk_artifacts("scan-1")
    mock_supabase.table.return_value.select.return_value.eq.assert_any_call("scan_id", "scan-1")

def test_bulk_inserts(mock_supabase):
    model = SupabaseModel()
    model.register("user", "pass")
    # Test empty lists
    assert model.create_apk_findings([]) is None
    assert model.create_apk_artifacts([]) is None
    
    # Test non-empty
    model.create_apk_findings([{"f": 1}])
    mock_supabase.table.return_value.insert.assert_any_call([{"f": 1}])

    model.create_apk_artifacts([{"a": 1}])
    mock_supabase.table.return_value.insert.assert_any_call([{"a": 1}])

def test_create_report_export(mock_supabase):
    model = SupabaseModel()
    payload = {"scan_id": 1, "user_id": "u1", "export_format": "csv"}
    model.create_report_export(payload)
    mock_supabase.table.return_value.insert.assert_called_with(payload)