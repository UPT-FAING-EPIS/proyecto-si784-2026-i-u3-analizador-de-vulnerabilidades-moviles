from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.api.schemas.reports import ReportCreate
from app.api.services.report_service import ReportService


class FakeReportModel:
    def __init__(self, user_data=None):
        self.user_data = user_data if user_data is not None else [{"id": "user-1"}]
        self.created_payload = None

    def user_exists(self, user_id):
        return SimpleNamespace(data=self.user_data)

    def create_report(self, payload):
        self.created_payload = payload
        return SimpleNamespace(data=[{"id": "report-1"}])


def test_create_report_persists_payload_with_normalized_level():
    model = FakeReportModel()
    service = ReportService(model)
    report = ReportCreate(
        user_id="user-1",
        dispositivo="Android",
        vulnerabilidad="USB Debugging",
        nivel="medio",
        descripcion="Modo desarrollador activo",
    )

    response = service.create_report(report)

    assert response["status"] == "created"
    assert response["id"] == "report-1"
    assert model.created_payload["nivel"] == "Medio"
    assert "fecha" in model.created_payload


def test_create_report_rejects_unknown_user():
    service = ReportService(FakeReportModel(user_data=[]))
    report = ReportCreate(
        user_id="missing",
        dispositivo="Android",
        vulnerabilidad="USB Debugging",
        nivel="Medio",
    )

    with pytest.raises(HTTPException) as exc:
        service.create_report(report)

    assert exc.value.status_code == 404


def test_create_report_rejects_invalid_level():
    service = ReportService(FakeReportModel())
    report = ReportCreate(
        user_id="user-1",
        dispositivo="Android",
        vulnerabilidad="USB Debugging",
        nivel="Urgente",
    )

    with pytest.raises(HTTPException) as exc:
        service.create_report(report)

    assert exc.value.status_code == 422
