from datetime import datetime, timezone
from hashlib import pbkdf2_hmac, sha256

from supabase import create_client

from app.dashboard.config.settings import get_supabase_settings


class SupabaseModel:
    def __init__(self):
        settings = get_supabase_settings()
        self.supabase = create_client(settings["url"], settings["key"])

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password with PBKDF2-HMAC-SHA256 (key-stretching, Sonar S5344 compliant)."""
        dk = pbkdf2_hmac("sha256", password.encode(), b"anzencore", 260_000)
        return dk.hex()

    @staticmethod
    def _hash_password_legacy(password: str) -> str:
        """Legacy SHA-256 hash used before PBKDF2 migration."""
        return sha256(password.encode()).hexdigest()

    def _upgrade_password(self, user_id: str, password: str) -> None:
        """Silently re-hash a legacy password to PBKDF2 on first successful login."""
        new_hash = self._hash_password(password)
        self.supabase.table("usuarios").update({"password": new_hash}).eq("id", user_id).execute()

    def authenticate(self, username, password):
        # 1. Try current PBKDF2 hash
        hashed = self._hash_password(password)
        res = (
            self.supabase.table("usuarios")
            .select("*")
            .eq("username", username)
            .eq("password", hashed)
            .execute()
        )
        if res.data:
            return res

        # 2. Fall back to legacy SHA-256 hash (users created before PBKDF2 migration)
        legacy_hash = self._hash_password_legacy(password)
        res_legacy = (
            self.supabase.table("usuarios")
            .select("*")
            .eq("username", username)
            .eq("password", legacy_hash)
            .execute()
        )
        if res_legacy.data:
            # Upgrade stored hash transparently so next login uses PBKDF2
            self._upgrade_password(res_legacy.data[0]["id"], password)
            return res_legacy

        return res  # empty result → login failed


    def user_exists(self, username):
        return (
            self.supabase.table("usuarios")
            .select("id")
            .eq("username", username)
            .limit(1)
            .execute()
        )

    def register(self, username, password):
        hashed = self._hash_password(password)
        return (
            self.supabase.table("usuarios")
            .insert({"username": username, "password": hashed})
            .execute()
        )

    def update_ping(self, user_id):
        return (
            self.supabase.table("usuarios")
            .update({"last_ping": datetime.now(timezone.utc).isoformat()})
            .eq("id", user_id)
            .execute()
        )

    def get_online_users(self, time_limit):
        return (
            self.supabase.table("usuarios")
            .select("username")
            .gt("last_ping", time_limit)
            .execute()
        )

    def get_vulnerabilities(self, user_id):
        return (
            self.supabase.table("vulnerabilidades")
            .select("*")
            .eq("user_id", user_id)
            .order("fecha", desc=True)
            .execute()
        )

    def save_vulnerabilities(self, rows: list) -> None:
        """Inserta uno o varios reportes en la tabla vulnerabilidades."""
        if not rows:
            return
        self.supabase.table("vulnerabilidades").insert(rows).execute()

    def get_apk_scans(self, user_id):
        return (
            self.supabase.table("apk_scans")
            .select(
                "id, user_id, file_name, file_size_bytes, file_hash_sha256, "
                "package_name, app_name, version_name, version_code, "
                "status, severity_max, findings_count, summary, error_message, "
                "created_at, started_at, finished_at"
            )
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

    def get_all_apk_scans(self):
        return (
            self.supabase.table("apk_scans")
            .select("id, status, severity_max, findings_count, created_at, user_id")
            .order("created_at", desc=True)
            .execute()
        )

    def create_apk_scan(self, payload):
        return self.supabase.table("apk_scans").insert(payload).execute()

    def update_apk_scan(self, scan_id, payload):
        return (
            self.supabase.table("apk_scans")
            .update(payload)
            .eq("id", scan_id)
            .execute()
        )

    def get_apk_findings(self, scan_id):
        return (
            self.supabase.table("apk_findings")
            .select("*")
            .eq("scan_id", scan_id)
            .order("severity", desc=True)
            .execute()
        )

    def get_apk_artifacts(self, scan_id):
        return (
            self.supabase.table("apk_artifacts")
            .select("*")
            .eq("scan_id", scan_id)
            .order("artifact_type")
            .execute()
        )

    def create_apk_findings(self, findings):
        if not findings:
            return None
        return self.supabase.table("apk_findings").insert(findings).execute()

    def create_apk_artifacts(self, artifacts):
        if not artifacts:
            return None
        return self.supabase.table("apk_artifacts").insert(artifacts).execute()

    def create_report_export(self, payload):
        return self.supabase.table("report_exports").insert(payload).execute()
