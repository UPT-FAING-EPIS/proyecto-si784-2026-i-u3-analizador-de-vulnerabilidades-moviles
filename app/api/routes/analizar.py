import asyncio

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.api.schemas.analysis import AnalisisResponse
from app.api.services.analysis_service import AnalysisService, ExternalServiceError


router = APIRouter(prefix="/api", tags=["analizar"])

TIPOS_VALIDOS = {"apk", "codigo_fuente", "url", "repo_github"}


def get_analysis_service():
    return AnalysisService()


async def _analizar_archivo(tipo, archivo, service):
    if archivo is None:
        raise HTTPException(
            status_code=400,
            detail="Debes adjuntar 'archivo' para tipo_analisis 'apk' o 'codigo_fuente'.",
        )
    file_bytes = await archivo.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="El archivo esta vacio.")

    if tipo == "apk":
        return await asyncio.to_thread(service.analizar_apk, file_bytes, archivo.filename)
    return await asyncio.to_thread(service.analizar_codigo_fuente, file_bytes, archivo.filename)


async def _analizar_objetivo(tipo, url, service):
    if tipo == "repo_github":
        if not url:
            raise HTTPException(status_code=400, detail="Debes indicar 'url' con el repositorio de GitHub.")
        return await asyncio.to_thread(service.analizar_repo_github, url)

    if not url:
        raise HTTPException(status_code=400, detail="Debes indicar 'url' para tipo_analisis 'url'.")
    return await asyncio.to_thread(service.analizar_url, url)


@router.post("/analizar", response_model=AnalisisResponse)
async def analizar(
    tipo_analisis: str = Form(...),
    archivo: UploadFile | None = File(None),
    url: str | None = Form(None),
    service: AnalysisService = Depends(get_analysis_service),
):
    tipo = tipo_analisis.strip().lower()
    if tipo not in TIPOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"tipo_analisis debe ser uno de: {', '.join(sorted(TIPOS_VALIDOS))}.",
        )

    try:
        if tipo in {"apk", "codigo_fuente"}:
            return await _analizar_archivo(tipo, archivo, service)
        return await _analizar_objetivo(tipo, url, service)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except ExternalServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Error interno al analizar la aplicacion.") from exc
