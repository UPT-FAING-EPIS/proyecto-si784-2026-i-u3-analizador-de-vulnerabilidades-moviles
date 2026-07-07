import pytest
from app.dashboard.services.report_export_service import ReportExportService


def test_report_export_service_build_filename():
    service = ReportExportService()
    scan = {"id": "12345678-abcd", "file_name": "My App! @v1.apk"}
    
    filename = service.build_filename(scan, "pdf")
    
    assert filename.startswith("anzencore_My_App___v1_")
    assert filename.endswith(".pdf")
    assert "12345678" in filename


def test_report_export_service_build_export_log():
    service = ReportExportService()
    scan = {"id": 101}
    
    log = service.build_export_log(scan, "user-1", "pdf", "report.pdf")
    
    assert log["scan_id"] == 101
    assert log["user_id"] == "user-1"
    assert log["export_format"] == "pdf"
    assert log["file_name"] == "report.pdf"


def test_report_export_service_build_pdf():
    service = ReportExportService()
    scan = {
        "app_name": "Demo",
        "package_name": "com.test",
        "version_name": "1.0",
        "version_code": "1",
        "file_name": "demo.apk",
        "file_size_bytes": 1024 * 1024,
        "file_hash_sha256": "hash",
        "created_at": "2026-06-12T12:00:00",
        "severity_max": "Info",
        "findings_count": 0
    }
    pdf_bytes = service.build_pdf(scan, [], [])
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
