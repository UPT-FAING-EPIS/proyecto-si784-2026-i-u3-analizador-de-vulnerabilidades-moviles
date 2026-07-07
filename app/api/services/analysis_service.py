from datetime import datetime, timezone

import requests

from app.api.services.external_quality_client import ExternalQualityClient
from app.dashboard.services.apk_analyzer import ApkAnalyzer
from app.dashboard.services.vulnerability_scanner import VulnerabilityScanner


SEVERIDAD_ORDEN = {"Info": 0, "Bajo": 1, "Medio": 2, "Alto": 3, "Critico": 4}

# Para codigo_fuente se descartan los hallazgos de estructura de APK
# (manifest/dex) que no aplican a un zip de codigo fuente.
SOURCE_CODE_FINDING_TYPES = {"hardcoded_secret", "insecure_communication", "native_code"}


class ExternalServiceError(Exception):
    """El servicio externo de analisis de calidad no respondio o devolvio error."""


class AnalysisService:
    def __init__(self, apk_analyzer=None, vulnerability_scanner=None, external_quality_client=None):
        self.apk_analyzer = apk_analyzer or ApkAnalyzer()
        self.vulnerability_scanner = vulnerability_scanner or VulnerabilityScanner()
        self.external_quality_client = external_quality_client or ExternalQualityClient()

    def analizar_apk(self, file_bytes, file_name):
        result = self.apk_analyzer.analyze(file_bytes)
        if result.status == "failed":
            raise ValueError(result.error_message)
        vulnerabilidades = [
            self._finding_to_item(i, finding) for i, finding in enumerate(result.findings, start=1)
        ]
        return self._build_response("apk", file_name, len(file_bytes), vulnerabilidades)

    def analizar_codigo_fuente(self, file_bytes, file_name):
        result = self.apk_analyzer.analyze(file_bytes)
        if result.status == "failed":
            raise ValueError(result.error_message)
        findings = [f for f in result.findings if f.finding_type in SOURCE_CODE_FINDING_TYPES]
        vulnerabilidades = [self._finding_to_item(i, finding) for i, finding in enumerate(findings, start=1)]
        return self._build_response("codigo_fuente", file_name, len(file_bytes), vulnerabilidades)

    def analizar_url(self, url):
        resultados = self.vulnerability_scanner.scan(url)
        vulnerabilidades = [self._scan_item_to_item(i, item) for i, item in enumerate(resultados, start=1)]
        return self._build_response("url", url, None, vulnerabilidades)

    def analizar_repo_github(self, repo_url):
        try:
            data = self.external_quality_client.analizar_repo(repo_url)
        except requests.exceptions.HTTPError as exc:
            raise ExternalServiceError(self._external_http_error_message(exc)) from exc
        except requests.exceptions.RequestException as exc:
            raise ExternalServiceError(
                f"No se pudo contactar el servicio externo de analisis de calidad: {exc}"
            ) from exc

        response = self._build_response("repo_github", repo_url, None, [])
        response["metricas_calidad"] = {
            "proyecto": data.get("project_name"),
            "lineas_codigo": data.get("loc"),
            "complejidad": data.get("complexity"),
            "code_smells": self._code_smells_count(data.get("code_smells")),
        }
        return response

    def _code_smells_count(self, code_smells):
        if isinstance(code_smells, dict):
            return len(code_smells.get("smells", []))
        return code_smells

    def _external_http_error_message(self, exc):
        response = exc.response
        try:
            body = response.json()
            mensaje = body.get("message") or body.get("detail") or body.get("error") or response.text
        except ValueError:
            mensaje = response.text
        return (
            f"El servicio externo de analisis de calidad respondio con error "
            f"({response.status_code}): {mensaje}"
        )

    def _finding_to_item(self, index, finding):
        return {
            "id": f"{finding.finding_type}-{index}",
            "tipo": finding.finding_type,
            "titulo": finding.title,
            "severidad": finding.severity,
            "descripcion": finding.description,
            "evidencia": finding.evidence,
            "recomendacion": finding.recommendation,
            "archivo_origen": finding.source_file,
            "cwe": finding.cwe,
            "owasp": finding.owasp_mobile,
        }

    def _scan_item_to_item(self, index, item):
        return {
            "id": f"remote_scan-{index}",
            "tipo": "remote_scan",
            "titulo": item.get("vulnerabilidad"),
            "severidad": item.get("nivel"),
            "descripcion": item.get("descripcion"),
            "evidencia": None,
            "recomendacion": item.get("recommendation"),
            "archivo_origen": item.get("dispositivo"),
            "cwe": item.get("cwe"),
            "owasp": item.get("owasp"),
        }

    def _build_response(self, tipo_analisis, objetivo, tamano_bytes, vulnerabilidades):
        conteo = {"Critico": 0, "Alto": 0, "Medio": 0, "Bajo": 0, "Info": 0}
        for vuln in vulnerabilidades:
            conteo[vuln["severidad"]] = conteo.get(vuln["severidad"], 0) + 1

        severidad_maxima = "Info"
        if vulnerabilidades:
            severidad_maxima = max(
                vulnerabilidades, key=lambda v: SEVERIDAD_ORDEN.get(v["severidad"], 0)
            )["severidad"]

        return {
            "estado": "ok",
            "tipo_analisis": tipo_analisis,
            "objetivo": objetivo,
            "tamano_bytes": tamano_bytes,
            "resumen": {
                "total_vulnerabilidades": len(vulnerabilidades),
                "severidad_maxima": severidad_maxima,
                "conteo_por_severidad": conteo,
            },
            "vulnerabilidades": vulnerabilidades,
            "fecha_analisis": datetime.now(timezone.utc).isoformat(),
        }
