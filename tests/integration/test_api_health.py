from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes.reports import get_report_service


def test_api_health_returns_ok():
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_create_report_returns_created():
    class FakeService:
        def create_report(self, report):
            return {
                "id": "report-1",
                "status": "created",
                "message": "Reporte registrado correctamente.",
            }

    app.dependency_overrides[get_report_service] = lambda: FakeService()
    client = TestClient(app)

    response = client.post(
        "/api/v1/reports",
        json={
            "user_id": "user-1",
            "dispositivo": "Android",
            "vulnerabilidad": "USB Debugging",
            "nivel": "Medio",
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["status"] == "created"
