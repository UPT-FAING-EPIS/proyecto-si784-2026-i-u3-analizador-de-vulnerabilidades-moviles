from hashlib import sha256
from datetime import datetime, timezone

from app.dashboard.services.apk_analyzer import ApkAnalyzer


class ApkScanService:
    def __init__(self):
        self.analyzer = ApkAnalyzer()

    def build_scan_payload(self, user_id, uploaded_file):
        file_bytes = uploaded_file.getvalue()
        return {
            "user_id": user_id,
            "file_name": uploaded_file.name,
            "file_size_bytes": len(file_bytes),
            "file_hash_sha256": sha256(file_bytes).hexdigest(),
            "status": "pending",
            "summary": "APK recibido para analisis de ingenieria inversa.",
        }, file_bytes

    def analyze(self, file_bytes):
        return self.analyzer.analyze(file_bytes)

    def build_scan_update_payload(self, analysis_result):
        return {
            "status": analysis_result.status,
            "summary": analysis_result.summary,
            "severity_max": analysis_result.severity_max,
            "findings_count": len(analysis_result.findings),
            "error_message": analysis_result.error_message,
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }

    def build_finding_payloads(self, scan_id, findings):
        return [
            {
                "scan_id": scan_id,
                "finding_type": finding.finding_type,
                "title": finding.title,
                "severity": finding.severity,
                "description": finding.description,
                "evidence": finding.evidence,
                "recommendation": finding.recommendation,
                "source_file": finding.source_file,
                "cwe": finding.cwe,
                "owasp_mobile": finding.owasp_mobile,
            }
            for finding in findings
        ]

    def build_artifact_payloads(self, scan_id, artifacts):
        return [
            {
                "scan_id": scan_id,
                "artifact_type": artifact.artifact_type,
                "artifact_value": artifact.artifact_value,
                "source_file": artifact.source_file,
            }
            for artifact in artifacts
        ]

    def validate_apk_file(self, uploaded_file):
        if uploaded_file is None:
            return False, "Selecciona un archivo APK."
        if not uploaded_file.name.lower().endswith(".apk"):
            return False, "El archivo debe tener extension .apk."
        if uploaded_file.size == 0:
            return False, "El archivo APK esta vacio."
        return True, "Archivo APK valido."
