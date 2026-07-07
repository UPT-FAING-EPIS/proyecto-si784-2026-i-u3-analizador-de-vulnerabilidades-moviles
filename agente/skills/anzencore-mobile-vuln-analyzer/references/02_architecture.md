# Blueprint de Arquitectura (Stateless)

Para la herramienta de Ingeniería Inversa y Análisis de Vulnerabilidades, usaremos una arquitectura de microservicios limpia y **100% Stateless** (sin estado). No necesitamos bases de datos complejas ni autenticación. El objetivo es que la herramienta arranque rápido y procese archivos en memoria.

## Componentes del Stack

1. **Backend / Motor de Ingeniería Inversa (FastAPI - Python 3.12)**
   - Puerto por defecto: 8000
   - Responsabilidad: Recibir el binario (APK) o el ZIP del código, extraerlo en memoria, ejecutar las heurísticas de seguridad y devolver un JSON estructurado.
   - Componentes clave:
     - `api/`: Define los endpoints POST.
     - `services/`: Donde vive la lógica pesada (`ApkAnalyzer`, `FolderAnalyzer`).

2. **Frontend / Interfaz de Auditoría (Streamlit - Python 3.12)**
   - Puerto por defecto: 8501
   - Responsabilidad: Ser la UI amigable donde el auditor sube el APK. Muestra spinners/barras de carga mientras el backend trabaja, y luego renderiza el reporte de vulnerabilidades de forma visual.
   - Estructura: Layout directo. Sin pantallas de login. Subir -> Analizar -> Ver Reporte.

3. **Despliegue Aislado (Docker)**
   - Cada servicio tiene su propio `Dockerfile` y corren de forma independiente.
   - El frontend de Streamlit se comunica con la API de FastAPI a través de peticiones HTTP (mediante la variable de entorno `API_URL`).

## Diagrama de Flujo
1. **Auditor** arrastra un archivo `.apk` a la interfaz de Streamlit.
2. Streamlit toma los bytes del archivo y hace un `POST multipart/form-data` a la API de FastAPI.
3. FastAPI recibe los bytes, los pasa al `ApkAnalyzer`.
4. El Analyzer hace **ingeniería inversa** extrayendo el contenido y aplicando reglas de detección.
5. FastAPI devuelve un JSON con todas las vulnerabilidades encontradas, artefactos extraídos y métricas de complejidad.
6. Streamlit dibuja métricas visuales, tablas, y bloques de código con las evidencias encontradas.
