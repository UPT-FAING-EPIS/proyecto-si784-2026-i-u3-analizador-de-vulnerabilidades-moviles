from pathlib import Path


def test_dashboard_exposes_apk_scan_and_export_controls():
    view_source = Path("app/dashboard/views/dashboard_view.py").read_text(encoding="utf-8")

    assert "Escanear APK" in view_source
    assert "Analizar" in view_source
    assert "Descargar PDF" in view_source
