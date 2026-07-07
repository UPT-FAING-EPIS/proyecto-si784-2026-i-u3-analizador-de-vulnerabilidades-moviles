from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.api.models.supabase_report_model import SupabaseReportModel


VALID_LEVELS = {"Critico", "Alto", "Medio", "Bajo", "Info"}


class ReportService:
    def __init__(self, model=None):
        self.model = model or SupabaseReportModel()

    def create_report(self, report):
        level = self._normalize_level(report.nivel)
        user_response = self.model.user_exists(report.user_id)
        if not getattr(user_response, "data", None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El user_id no existe.",
            )

        payload = report.model_dump()
        payload["nivel"] = level
        payload["fecha"] = datetime.now(timezone.utc).isoformat()

        response = self.model.create_report(payload)
        data = getattr(response, "data", None) or []
        created = data[0] if data else {}
        return {
            "id": created.get("id"),
            "status": "created",
            "message": "Reporte registrado correctamente.",
        }

    def _normalize_level(self, level):
        cleaned = level.strip().capitalize()
        if cleaned not in VALID_LEVELS:
            raise HTTPException(
                status_code=422,
                detail="nivel debe ser Critico, Alto, Medio, Bajo o Info.",
            )
        return cleaned
