# Backend & API (FastAPI Blueprint)

El backend de AnzenCore se basa en endpoints eficientes orientados a recibir archivos o URLs de repositorios, procesarlos de manera aislada (stateless) y devolver la información procesada.

## Patrón de Endpoints

Debes implementar endpoints que acepten `UploadFile` (para APKs) o `Form` fields (para repositorios) y deleguen a los *Services*. 

### Ejemplo de Endpoint para Analizador Móvil / de Código (Stateless)
```python
import asyncio
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

router = APIRouter(prefix="/api/analysis/external", tags=["external-analysis"])

@router.post("/upload_folder")
async def analizar_carpeta_local(
    project_name: str = Form(...),
    files: list[UploadFile] = File(...),
    analyzer = Depends(get_folder_analyzer_service),
):
    \"\"\"Analiza una carpeta local completa archivo por archivo.\"\"\"
    if not files:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un archivo.")

    file_data = []
    for upload in files:
        content = await upload.read()
        if content:
            file_data.append((upload.filename or "unknown", content))

    if not file_data:
        raise HTTPException(status_code=400, detail="Archivos vacíos.")

    # Uso de asyncio.to_thread para no bloquear el Event Loop con análisis pesados
    result = await asyncio.to_thread(analyzer.analyze_folder, project_name, file_data)
    return result
```

## Manejo de Tareas Pesadas
El análisis estático o decompilación de un APK puede tardar segundos. Siempre utiliza `asyncio.to_thread` o un esquema de BackgroundTasks/Celery si el tiempo excede los tiempos de timeout HTTP habituales.

## Estructura de Respuesta API (Contrato)
La API siempre responde con este JSON estándar:
```json
{
  "status": "success",
  "project_name": "NombreProyecto",
  "loc": 1250,
  "complexity": 45,
  "code_smells": {
    "smells": ["Posible secreto en config.js"],
    "metrics": { "nom": 12, "noa": 5 },
    "files": [
      {
         "file_path": "src/main/App.java",
         "loc": 43,
         "complexity": 3,
         "smells": ["..."]
      }
    ]
  }
}
```
Manten este contrato invariable para que el dashboard Streamlit o clientes externos lo interpreten correctamente.
