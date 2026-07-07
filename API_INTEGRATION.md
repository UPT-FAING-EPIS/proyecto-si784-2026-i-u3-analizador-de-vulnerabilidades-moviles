# Guía de Integración de API: AnzenCore

Esta guía describe cómo cualquier microservicio externo o Frontend puede consumir las capacidades de análisis de nuestra API. Hemos habilitado endpoints específicos que no requieren autenticación ni manejo de sesiones para facilitar la integración.

## 1. Analizar un Repositorio de GitHub

Este endpoint analiza un repositorio público de GitHub de forma *stateless* (no requiere autenticación y no se guarda en el historial de un usuario, aunque sí se registra en logs internos).

### Endpoint
- **URL:** `/api/analysis/external/github`
- **Método HTTP:** `POST`
- **Content-Type:** `application/x-www-form-urlencoded` o `multipart/form-data`

### Parámetros Requeridos (Body)

| Parámetro | Tipo | Descripción |
| :--- | :--- | :--- |
| `repo_url` | `string` | URL completa del repositorio de GitHub (ej: `https://github.com/usuario/repo`). |

### Estructura de Respuesta

La API responderá con un JSON (Content-Type: `application/json`) con el siguiente formato:

```json
{
  "status": "success",
  "project_name": "NombreDelRepositorio",
  "loc": 1250,
  "complexity": 45,
  "code_smells": {
    "smells": [ ... ],
    "metrics": { "nom": 12, "npm": 10, "noa": 5, "cloc": 100 },
    "files": [
      {
        "file_path": "src/main/DatabaseConnection.java",
        "loc": 43,
        "complexity": 3,
        "metrics": {
           "nom": 2,
           "noa": 5
        },
        "smells": [ "Código duplicado detectado..." ]
      }
    ]
  }
}
```

> [!NOTE]
> - `loc`: Líneas de código (Lines of Code).
> - `complexity`: Complejidad ciclomática calculada del código.
> - Toda la información detallada archivo por archivo se encuentra dentro del arreglo `code_smells.files`.

---

## 2. Analizar una Carpeta Local

Este endpoint permite subir múltiples archivos (toda una carpeta local) sin necesidad de manejar sesiones.

### Endpoint
- **URL:** `/api/analysis/external/upload_folder`
- **Método HTTP:** `POST`
- **Content-Type:** `multipart/form-data`

### Parámetros Requeridos (FormData)
- `project_name` (Text): El nombre de la carpeta o del proyecto.
- `files` (File Array): La lista de archivos que conforman el directorio.

> [!IMPORTANT]
> Para permitir la selección de carpetas enteras desde el navegador, deben asegurarse de utilizar los atributos `webkitdirectory` y `multiple` en su input HTML.

### Respuesta del Endpoint
El endpoint devolverá **exactamente la misma estructura JSON** detallada en el endpoint de GitHub. 

---

## 3. Ejemplos de Implementación

A continuación, ejemplos de cómo consumir estos endpoints:

### JavaScript / React (Fetch API - GitHub)

```javascript
async function analyzeRepo(repoUrl) {
  const formData = new FormData();
  formData.append("repo_url", repoUrl);

  try {
    const response = await fetch("http://<NUESTRO_HOST>/api/analysis/external/github", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
    const result = await response.json();
    console.log("Resultados del análisis:", result);
  } catch (error) {
    console.error("Error al consumir la API:", error);
  }
}
```

### JavaScript / React (Subir Carpeta)

```html
<!-- Input HTML para carpetas -->
<input type="file" id="folderInput" webkitdirectory multiple />
```

```javascript
async function analizarCarpetaLocal() {
    const input = document.getElementById('folderInput');
    const files = input.files;
    
    if (files.length === 0) return alert("Selecciona una carpeta.");

    const formData = new FormData();
    const nombreCarpeta = files[0].webkitRelativePath.split('/')[0] || "Carpeta_Local";
    formData.append("project_name", nombreCarpeta);

    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    try {
        const response = await fetch("http://<NUESTRO_HOST>/api/analysis/external/upload_folder", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        
        // Renderizar comparativas
        const detallesPorArchivo = data.code_smells.files;
        console.log(detallesPorArchivo);
    } catch (error) {
        console.error("Error al analizar la carpeta:", error);
    }
}
```

### Python (Requests - GitHub)

```python
import requests

def analyze_repo(repo_url):
    url = "http://<NUESTRO_HOST>/api/analysis/external/github"
    data = {"repo_url": repo_url}
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Análisis exitoso:", response.json())
    else:
        print("Error:", response.status_code, response.text)

analyze_repo("https://github.com/usuario/repo")
```
