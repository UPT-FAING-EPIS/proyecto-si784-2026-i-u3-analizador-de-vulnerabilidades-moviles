import pytest
from unittest.mock import MagicMock
from io import BytesIO
from app.dashboard.services.apk_scan_service import ApkScanService

def test_validate_apk_file_success():
    service = ApkScanService()
    mock_file = MagicMock()
    mock_file.name = "test_app.apk"
    mock_file.size = 1024
    
    is_valid, message = service.validate_apk_file(mock_file)
    
    assert is_valid is True
    assert "valido" in message.lower()

def test_validate_apk_file_invalid_extension():
    service = ApkScanService()
    mock_file = MagicMock()
    mock_file.name = "virus.exe"
    
    is_valid, message = service.validate_apk_file(mock_file)
    
    assert is_valid is False
    assert "extension .apk" in message

def test_build_scan_payload():
    service_instance = ApkScanService()
    mock_file = MagicMock()
    mock_file.name = "test.apk"
    mock_file.getvalue.return_value = b"apk_content"

    payload, content = service_instance.build_scan_payload("user-123", mock_file)

    assert payload["user_id"] == "user-123"
    assert "file_hash_sha256" in payload
    assert content == b"apk_content"

def test_build_scan_update_payload():
    service_instance = ApkScanService()
    mock_result = MagicMock()
    mock_result.status = "completed"
    mock_result.summary = "Scan done"
    mock_result.severity_max = "Alto"
    mock_result.findings = [1, 2, 3]
    mock_result.error_message = None

    update = service_instance.build_scan_update_payload(mock_result)

    assert update["status"] == "completed"
    assert update["findings_count"] == 3
    assert "finished_at" in update

def test_build_finding_payloads():
    service_instance = ApkScanService()
    mock_finding = MagicMock()
    mock_finding.finding_type = "perm"
    mock_finding.title = "Bad Permission"
    mock_finding.severity = "Alto"
    
    payloads = service_instance.build_finding_payloads("scan-1", [mock_finding])
    
    assert len(payloads) == 1
    assert payloads[0]["scan_id"] == "scan-1"
    assert payloads[0]["title"] == "Bad Permission"

def test_build_artifact_payloads():
    service_instance = ApkScanService()
    mock_art = MagicMock()
    mock_art.artifact_type = "url"
    mock_art.artifact_value = "http://test.com"
    mock_art.source_file = "classes.dex"
    
    payloads = service_instance.build_artifact_payloads("scan-1", [mock_art])
    
    assert len(payloads) == 1
    assert payloads[0]["artifact_value"] == "http://test.com"
    assert payloads[0]["source_file"] == "classes.dex"