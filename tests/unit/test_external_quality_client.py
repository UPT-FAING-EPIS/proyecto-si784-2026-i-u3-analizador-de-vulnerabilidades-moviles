from unittest.mock import MagicMock, patch

from app.api.services.external_quality_client import ExternalQualityClient


def test_analizar_repo_usa_multipart_form_data():
    client = ExternalQualityClient(url="https://anestatico.onrender.com/api/analysis/external/github")

    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {
        "status": "success",
        "project_name": "MiRepo",
        "loc": 1250,
        "complexity": 45,
        "code_smells": 12,
    }

    with patch("app.api.services.external_quality_client.requests.post", return_value=mock_response) as mock_post:
        data = client.analizar_repo("https://github.com/usuario/repo")

    mock_post.assert_called_once_with(
        "https://anestatico.onrender.com/api/analysis/external/github",
        files={"repo_url": (None, "https://github.com/usuario/repo")},
        timeout=client.timeout,
    )
    mock_response.raise_for_status.assert_called_once()
    assert data["project_name"] == "MiRepo"


def test_usa_anzen_external_url_por_defecto():
    client = ExternalQualityClient()

    assert client.url == "https://anestatico.onrender.com/api/analysis/external/github"
