import asyncio

import requests
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.api.services.external_quality_client import ExternalQualityClient
from app.api.services.folder_analyzer import FolderAnalyzer


router = APIRouter(prefix="/api/analysis/external", tags=["external-analysis"])


def _get_external_client():
    return ExternalQualityClient()


def _get_folder_analyzer():
    return FolderAnalyzer()


@router.post("/github")
async def analizar_github(
    repo_url: str = Form(...),
    client: ExternalQualityClient = Depends(_get_external_client),
):
    """Proxy al motor de análisis estático externo; retorna la respuesta completa incluyendo code_smells.files."""
    try:
        data = await asyncio.to_thread(client.analizar_repo, repo_url)
    except requests.exceptions.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"El servicio externo respondió con error ({exc.response.status_code}).",
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"No se pudo contactar el servicio externo de análisis: {exc}",
        ) from exc
    return data


@router.post("/upload_folder")
async def analizar_carpeta_local(
    project_name: str = Form(...),
    files: list[UploadFile] = File(...),
    analyzer: FolderAnalyzer = Depends(_get_folder_analyzer),
):
    """Analiza una carpeta local completa archivo por archivo y retorna métricas y code smells por archivo."""
    if not files:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un archivo.")

    file_data: list[tuple[str, bytes]] = []
    for upload in files:
        content = await upload.read()
        if content:
            file_data.append((upload.filename or "unknown", content))

    if not file_data:
        raise HTTPException(status_code=400, detail="Todos los archivos enviados están vacíos.")

    result = await asyncio.to_thread(analyzer.analyze_folder, project_name, file_data)
    return result
