from unittest.mock import MagicMock

import pytest
import requests

from app.api.services.analysis_service import AnalysisService, ExternalServiceError


@pytest.fixture
def service():
    return AnalysisService(external_quality_client=MagicMock())


def test_analizar_repo_github_success(service):
    service.external_quality_client.analizar_repo.return_value = {
        "status": "success",
        "project_name": "MiRepo",
        "loc": 1250,
        "complexity": 45,
        "code_smells": 12,
    }

    result = service.analizar_repo_github("https://github.com/usuario/repo")

    assert result["estado"] == "ok"
    assert result["tipo_analisis"] == "repo_github"
    assert result["objetivo"] == "https://github.com/usuario/repo"
    assert result["metricas_calidad"] == {
        "proyecto": "MiRepo",
        "lineas_codigo": 1250,
        "complejidad": 45,
        "code_smells": 12,
    }
    service.external_quality_client.analizar_repo.assert_called_once_with(
        "https://github.com/usuario/repo"
    )


def test_analizar_repo_github_normaliza_code_smells_objeto(service):
    service.external_quality_client.analizar_repo.return_value = {
        "status": "success",
        "project_name": "MiRepo",
        "loc": 3885,
        "complexity": 603,
        "code_smells": {
            "smells": ["Long method: foo", "Long method: bar"],
            "metrics": {"nom": 1, "npm": 1, "noa": 0, "cloc": 1},
            "files": [],
        },
    }

    result = service.analizar_repo_github("https://github.com/usuario/repo")

    assert result["metricas_calidad"]["code_smells"] == 2


def test_analizar_repo_github_http_error(service):
    response = MagicMock(status_code=500)
    response.json.return_value = {"detail": "Error interno del analizador externo"}
    error = requests.exceptions.HTTPError(response=response)
    service.external_quality_client.analizar_repo.side_effect = error

    with pytest.raises(ExternalServiceError) as exc_info:
        service.analizar_repo_github("https://github.com/usuario/repo")

    assert "500" in str(exc_info.value)
    assert "Error interno del analizador externo" in str(exc_info.value)


def test_analizar_repo_github_http_error_non_json_body(service):
    response = MagicMock(status_code=502)
    response.json.side_effect = ValueError("not json")
    response.text = "Bad Gateway"
    error = requests.exceptions.HTTPError(response=response)
    service.external_quality_client.analizar_repo.side_effect = error

    with pytest.raises(ExternalServiceError) as exc_info:
        service.analizar_repo_github("https://github.com/usuario/repo")

    assert "Bad Gateway" in str(exc_info.value)


def test_analizar_repo_github_timeout(service):
    service.external_quality_client.analizar_repo.side_effect = requests.exceptions.Timeout("timed out")

    with pytest.raises(ExternalServiceError) as exc_info:
        service.analizar_repo_github("https://github.com/usuario/repo")

    assert "No se pudo contactar" in str(exc_info.value)


def test_analizar_repo_github_connection_error(service):
    service.external_quality_client.analizar_repo.side_effect = requests.exceptions.ConnectionError("boom")

    with pytest.raises(ExternalServiceError) as exc_info:
        service.analizar_repo_github("https://github.com/usuario/repo")

    assert "No se pudo contactar" in str(exc_info.value)
