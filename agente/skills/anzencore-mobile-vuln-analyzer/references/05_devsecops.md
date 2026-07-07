# Infraestructura y Despliegue (Blueprint)

El despliegue de la herramienta de Ingeniería Inversa y Análisis debe ser ligero, utilizando contenedores e infraestructura como código sin dependencias complejas.

## 1. Contenedores (Docker)
Los servicios se empaquetan por separado:
- **API (`Dockerfile.api`)**: Ejecuta `uvicorn` (FastAPI) exponiendo el puerto 8000.
- **Dashboard (`Dockerfile.dashboard`)**: Ejecuta `streamlit` exponiendo el puerto 8501. Configurado para apuntar a la URL de la API.

Ambos Dockerfiles deben ser optimizados, utilizando imágenes base ligeras de Python 3.12 (por ejemplo, `python:3.12-slim`).

## 2. Infraestructura como Código (Terraform)
La infraestructura despliega los contenedores en Azure Container Apps o servicios similares serverless (ECS, Cloud Run).

- **Azure Container Registry (ACR)**: Almacena las imágenes Docker de la API y el Dashboard.
- **Azure Container Apps Environment**: Orquestador donde viven los contenedores.
- **Container Apps**:
  - `analyzer-api`: Expone puerto 8000. Escala basado en peticiones HTTP concurrentes.
  - `analyzer-dashboard`: Expone puerto 8501. Configurado con un tráfico del 100% apuntando a la última revisión. Conoce a la API usando la FQDN interna de la Container App de la API (a través de la variable `API_URL`).

*(No es necesario provisionar bases de datos como Postgres o Redis en esta arquitectura).*

## 3. CI/CD & Calidad
El código de la herramienta de análisis debe probarse a sí mismo:
- **Pytest**: Para asegurar que las expresiones regulares de ingeniería inversa realmente detectan los secretos y fallas en los APKs de prueba.
- **Mutmut** (Opcional pero recomendado): Pruebas de mutación para asegurar que los tests son robustos contra cambios accidentales en las reglas de detección.
