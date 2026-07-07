# Frontend Dashboard (Streamlit Blueprint)

El frontend para la herramienta de Ingeniería Inversa debe ser directo, enfocado en subir archivos y mostrar los reportes de manera profesional. No necesitamos bases de datos ni logins, el estado vivirá únicamente en memoria durante la sesión activa.

## Layout Principal
La interfaz en Streamlit debe tener un diseño claro:

```python
import streamlit as st
import requests

st.set_page_config(page_title="Analizador Móvil", page_icon="🛡️", layout="wide")

def main():
    st.title("🛡️ Ingeniería Inversa y Análisis de APKs")
    
    uploaded_file = st.file_uploader("Sube un archivo .apk para analizar", type=["apk", "zip"])
    
    if uploaded_file is not None:
        if st.button("Iniciar Análisis y Extracción"):
            with st.spinner("Descompilando y buscando vulnerabilidades..."):
                # Hacer POST request a FastAPI
                files = {"files": (uploaded_file.name, uploaded_file.getvalue())}
                data = {"project_name": uploaded_file.name}
                try:
                    response = requests.post("http://api:8000/api/analysis/external/upload_folder", files=files, data=data)
                    result = response.json()
                    render_report(result)
                except Exception as e:
                    st.error(f"Error conectando al motor de análisis: {e}")

def render_report(result):
    # Dibuja los hallazgos agrupados por severidad
    pass

if __name__ == "__main__":
    main()
```

## Prácticas Recomendadas para Mostrar Hallazgos de Seguridad
1. **Métricas Rápidas:** Usa `st.metric` o tarjetas HTML para mostrar el Total de Vulnerabilidades, Severidad Máxima y Archivos Extraídos.
2. **Agrupación Visual:** Utiliza `st.expander` para agrupar los hallazgos. Un expander por vulnerabilidad o un tab (`st.tabs`) por nivel de severidad (Crítico en rojo, Alto en naranja, etc.).
3. **Evidencia en Código:** Muestra las porciones de código vulnerables usando `st.code(evidencia, language='java')`.
4. **Recomendaciones:** Muestra la información de mitigación (CWE o OWASP) en un bloque `st.info` o `st.warning`.
