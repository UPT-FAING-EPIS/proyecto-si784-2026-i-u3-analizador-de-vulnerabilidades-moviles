from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes.analizar import get_analysis_service


def test_analizar_repo_github_success():
    fake_service = MagicMock()
    fake_service.analizar_repo_github.return_value = {
        "estado": "ok",
        "tipo_analisis": "repo_github",
        "objetivo": "https://github.com/usuario/repo",
        "tamano_bytes": None,
        "resumen": {
            "total_vulnerabilidades": 0,
            "severidad_maxima": "Info",
            "conteo_por_severidad": {"Critico": 0, "Alto": 0, "Medio": 0, "Bajo": 0, "Info": 0},
        },
        "vulnerabilidades": [],
        "metricas_calidad": {
            "proyecto": "MiRepo",
            "lineas_codigo": 1250,
            "complejidad": 45,
            "code_smells": 12,
        },
        "fecha_analisis": "2026-06-12T00:00:00+00:00",
    }

    app.dependency_overrides[get_analysis_service] = lambda: fake_service
    client = TestClient(app)

    response = client.post(
        "/api/analizar",
        data={"tipo_analisis": "repo_github", "url": "https://github.com/usuario/repo"},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["metricas_calidad"]["proyecto"] == "MiRepo"
    fake_service.analizar_repo_github.assert_called_once_with("https://github.com/usuario/repo")


def test_analizar_repo_github_error_externo_devuelve_502():
    from app.api.services.analysis_service import ExternalServiceError

    fake_service = MagicMock()
    fake_service.analizar_repo_github.side_effect = ExternalServiceError(
        "El servicio externo de analisis de calidad respondio con error (500): boom"
    )

    app.dependency_overrides[get_analysis_service] = lambda: fake_service
    client = TestClient(app)

    response = client.post(
        "/api/analizar",
        data={"tipo_analisis": "repo_github", "url": "https://github.com/usuario/repo"},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 502
    assert "boom" in response.json()["detail"]


def test_analizar_repo_github_timeout_devuelve_502():
    from app.api.services.analysis_service import ExternalServiceError

    fake_service = MagicMock()
    fake_service.analizar_repo_github.side_effect = ExternalServiceError(
        "No se pudo contactar el servicio externo de analisis de calidad: timed out"
    )

    app.dependency_overrides[get_analysis_service] = lambda: fake_service
    client = TestClient(app)

    response = client.post(
        "/api/analizar",
        data={"tipo_analisis": "repo_github", "url": "https://github.com/usuario/repo"},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 502
    assert "No se pudo contactar" in response.json()["detail"]
