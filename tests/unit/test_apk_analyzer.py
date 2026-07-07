from io import BytesIO
import zipfile

from app.dashboard.services.apk_analyzer import ApkAnalyzer


def build_test_apk(files):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as apk:
        for name, content in files.items():
            apk.writestr(name, content)
    return buffer.getvalue()


def test_apk_analyzer_detects_basic_structure():
    apk_bytes = build_test_apk(
        {
            "AndroidManifest.xml": "<manifest />",
            "classes.dex": "dex content",
        }
    )

    result = ApkAnalyzer().analyze(apk_bytes)

    assert result.status == "completed"
    assert result.severity_max == "Info"
    assert any(item.artifact_type == "dex_count" for item in result.artifacts)


def test_apk_analyzer_detects_insecure_http():
    apk_bytes = build_test_apk(
        {
            "AndroidManifest.xml": "<manifest />",
            "classes.dex": "http://insecure.example.com/api",
        }
    )

    result = ApkAnalyzer().analyze(apk_bytes)

    assert result.status == "completed"
    assert any(
        finding.finding_type == "insecure_communication"
        for finding in result.findings
    )


def test_apk_analyzer_rejects_invalid_apk():
    result = ApkAnalyzer().analyze(b"not an apk")

    assert result.status == "failed"
    assert "APK valido" in result.summary
