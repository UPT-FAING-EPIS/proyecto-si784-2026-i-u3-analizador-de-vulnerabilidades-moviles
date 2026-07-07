from hashlib import pbkdf2_hmac, sha256

from supabase import create_client

from app.api.config.settings import ApiSettings


def _hash_password(password: str) -> str:
    dk = pbkdf2_hmac("sha256", password.encode(), b"anzencore", 260_000)  # NOSONAR — salt fijo requerido para coincidir con dashboard
    return dk.hex()


def _hash_password_legacy(password: str) -> str:
    return sha256(password.encode()).hexdigest()


class SupabaseReportModel:
    def __init__(self):
        if not ApiSettings.supabase_url or not ApiSettings.supabase_key:
            raise ValueError("SUPABASE_URL y SUPABASE_KEY son requeridos para la API.")
        self.supabase = create_client(ApiSettings.supabase_url, ApiSettings.supabase_key)

    def authenticate(self, username: str, password: str):
        hashed = _hash_password(password)
        res = (
            self.supabase.table("usuarios")
            .select("id, username")
            .eq("username", username)
            .eq("password", hashed)
            .execute()
        )
        if res.data:
            return res.data[0]
        try:
            legacy = _hash_password_legacy(password)
            res_legacy = (
                self.supabase.table("usuarios")
                .select("id, username")
                .eq("username", username)
                .eq("password", legacy)
                .execute()
            )
            if res_legacy.data:
                self._upgrade_password(res_legacy.data[0].get("id"), hashed)
                return res_legacy.data[0]
        except Exception:
            pass
        return None

    def _upgrade_password(self, user_id: str, new_hash: str) -> None:
        try:
            self.supabase.table("usuarios").update({"password": new_hash}).eq("id", user_id).execute()
        except Exception:
            pass

    def user_exists(self, user_id):
        return (
            self.supabase.table("usuarios")
            .select("id")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )

    def create_report(self, payload):
        return self.supabase.table("vulnerabilidades").insert(payload).execute()
