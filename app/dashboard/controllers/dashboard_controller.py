import socket
from datetime import datetime, timedelta, timezone

import requests

from app.dashboard.services.anzen_api_client import AnzenApiClient
from app.dashboard.services.apk_scan_service import ApkScanService
from app.dashboard.services.report_export_service import ReportExportService
from app.dashboard.services.vulnerability_scanner import VulnerabilityScanner


class DashboardController:
    def __init__(self, model):
        self.model = model
        self.vulnerability_scanner = VulnerabilityScanner()
        self.apk_scan_service = ApkScanService()
        self.report_export_service = ReportExportService()
        self.anzen_api_client = AnzenApiClient()

    def login(self, username, password):
        res = self.model.authenticate(username, password)
        return res.data[0] if res.data else None

    def signup(self, username, password):
        username = username.strip()
        if not username or not password:
            return False, "Completa usuario y contrasena."

        try:
            existing = self.model.user_exists(username)
            if existing.data:
                return False, "El usuario ya existe."
            self.model.register(username, password)
            return True, "Registrado. Ingresa ahora."
        except socket.gaierror:
            return False, "No se pudo conectar con Supabase: revisa internet, DNS o la URL del proyecto."
        except Exception as exc:
            if "getaddrinfo failed" in str(exc):
                return False, "No se pudo conectar con Supabase: revisa internet, DNS o la URL del proyecto."
            return False, f"No se pudo crear el usuario: {exc}"

    def update_user_ping(self, user_id):
        return self.model.update_ping(user_id)

    def fetch_online_list(self):
        threshold = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        res = self.model.get_online_users(threshold)
        return res.data

    def fetch_all_reports(self, user_id):
        res = self.model.get_vulnerabilities(user_id)
        if res.data:
            from app.dashboard.services.vulnerability_scanner import _enrich
            return [_enrich(row.get("vulnerabilidad", ""), row) for row in res.data]
        return res.data

    def scan_vulnerabilities(self, user_id: str, target=None):
        results = self.vulnerability_scanner.scan(target)
        if results:
            # Filtrar columnas para guardar únicamente campos válidos en la tabla vulnerabilidades
            db_columns = {"user_id", "dispositivo", "vulnerabilidad", "nivel", "descripcion", "fecha"}
            rows_to_save = []
            for row in results:
                clean_row = {k: v for k, v in row.items() if k in db_columns}
                clean_row["user_id"] = user_id
                rows_to_save.append(clean_row)
            try:
                self.model.save_vulnerabilities(rows_to_save)
            except Exception:
                pass  # Si falla el guardado, igual devolvemos los resultados en memoria
        return results

    def fetch_apk_scans(self, user_id):
        res = self.model.get_apk_scans(user_id)
        return res.data

    def fetch_global_apk_scans(self):
        res = self.model.get_all_apk_scans()
        return res.data

    def fetch_apk_findings(self, scan_id):
        res = self.model.get_apk_findings(scan_id)
        return res.data

    def fetch_apk_artifacts(self, scan_id):
        res = self.model.get_apk_artifacts(scan_id)
        return res.data

    def build_report_export(self, scan, findings, artifacts, export_format):
        if export_format == "pdf":
            data = self.report_export_service.build_pdf(scan, findings, artifacts)
        else:
            raise ValueError("Formato de exportacion no soportado.")

        file_name = self.report_export_service.build_filename(scan, export_format)
        return file_name, data

    def analizar_carpeta_local(self, project_name: str, uploaded_files):
        file_list = [(f.name, f.read()) for f in uploaded_files]
        try:
            data = self.anzen_api_client.analizar_carpeta(project_name, file_list)
        except requests.exceptions.HTTPError as exc:
            try:
                detail = exc.response.json().get("detail", str(exc))
            except ValueError:
                detail = str(exc)
            return False, f"El servicio externo respondió con error: {detail}"
        except requests.exceptions.Timeout:
            return False, "El servicio tardó demasiado en responder. Puede estar iniciando (Render free tier). Espera 30 segundos e intenta de nuevo."
        except requests.exceptions.RequestException as exc:
            return False, f"No se pudo contactar el servicio externo: {exc}"

        code_smells_raw = data.get("code_smells")
        if isinstance(code_smells_raw, dict):
            code_smells_count = len(code_smells_raw.get("smells", []))
            files = code_smells_raw.get("files", [])
        else:
            code_smells_count = code_smells_raw
            files = []

        return True, {
            "proyecto": data.get("project_name", project_name),
            "lineas_codigo": data.get("loc"),
            "complejidad": data.get("complexity"),
            "code_smells": code_smells_count,
            "files": files,
        }

    def analizar_repo_github(self, repo_url):
        try:
            data = self.anzen_api_client.analizar_repo_github(repo_url)
        except requests.exceptions.HTTPError as exc:
            try:
                detail = exc.response.json().get("detail", str(exc))
            except ValueError:
                detail = str(exc)
            return False, f"El servicio externo de analisis de calidad respondio con error: {detail}"
        except requests.exceptions.Timeout:
            return False, "El servicio externo tardó demasiado en responder. Puede estar iniciando (Render free tier). Espera 30 segundos e intenta de nuevo."
        except requests.exceptions.RequestException as exc:
            return False, f"No se pudo contactar el servicio externo de analisis de calidad: {exc}"

        code_smells_raw = data.get("code_smells")
        if isinstance(code_smells_raw, dict):
            code_smells_count = len(code_smells_raw.get("smells", []))
            files = code_smells_raw.get("files", [])
        else:
            code_smells_count = code_smells_raw
            files = []

        return True, {
            "proyecto": data.get("project_name"),
            "lineas_codigo": data.get("loc"),
            "complejidad": data.get("complexity"),
            "code_smells": code_smells_count,
            "files": files,
            "_raw": data,
        }

    def analizar_con_api_externa(self, target_type: str, target_value: str):
        from app.dashboard.services.external_security_client import ExternalSecurityClient
        client = ExternalSecurityClient()
        try:
            result = client.analyze(target_type, target_value)
            return True, result
        except requests.exceptions.HTTPError as exc:
            try:
                detail = exc.response.json().get("detail", str(exc))
            except ValueError:
                detail = str(exc)
            return False, detail
        except requests.exceptions.RequestException as exc:
            return False, f"No se pudo contactar la API externa: {exc}"

    def get_reportes_api_externa(self):
        from app.dashboard.services.external_security_client import ExternalSecurityClient
        client = ExternalSecurityClient()
        try:
            return True, client.get_reports()
        except requests.exceptions.HTTPError as exc:
            try:
                detail = exc.response.json().get("detail", str(exc))
            except ValueError:
                detail = str(exc)
            return False, detail
        except requests.exceptions.RequestException as exc:
            return False, f"No se pudo contactar la API externa: {exc}"

    def create_apk_scan(self, user_id, uploaded_file):
        is_valid, message = self.apk_scan_service.validate_apk_file(uploaded_file)
        if not is_valid:
            return False, message

        try:
            payload, file_bytes = self.apk_scan_service.build_scan_payload(
                user_id,
                uploaded_file,
            )
            created = self.model.create_apk_scan(payload)
            if not created.data:
                return False, "No se pudo registrar el escaneo del APK."

            scan_id = created.data[0]["id"]
            self.model.update_apk_scan(
                scan_id,
                {
                    "status": "processing",
                    "started_at": datetime.now(timezone.utc).isoformat(),
                },
            )

            analysis = self.apk_scan_service.analyze(file_bytes)
            self.model.update_apk_scan(
                scan_id,
                self.apk_scan_service.build_scan_update_payload(analysis),
            )

            finding_payloads = self.apk_scan_service.build_finding_payloads(
                scan_id,
                analysis.findings,
            )
            artifact_payloads = self.apk_scan_service.build_artifact_payloads(
                scan_id,
                analysis.artifacts,
            )
            self.model.create_apk_findings(finding_payloads)
            self.model.create_apk_artifacts(artifact_payloads)

            if analysis.status == "failed":
                return False, analysis.summary
            return True, {"message": analysis.summary, "scan_id": scan_id}
        except Exception as exc:
            message = str(exc)
            if "row-level security" in message.lower():
                return (
                    False,
                    "Supabase bloqueo el registro por RLS. Revisa las politicas de permisos en el SQL Editor de Supabase.",
                )
            return False, f"No se pudo analizar el APK: {exc}"
