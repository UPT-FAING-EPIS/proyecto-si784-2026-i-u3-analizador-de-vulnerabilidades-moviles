# AnzenCore para VS Code

Analizador de vulnerabilidades móviles y code smells de [AnzenCore](../README.md), sin salir del editor.

## Comandos

| Comando | Qué hace | ¿Requiere el backend? |
| --- | --- | --- |
| **AnzenCore: Analizar Workspace** | Analiza code smells/complejidad de la carpeta raíz del workspace. | Sí (llama a la API) |
| **AnzenCore: Analizar esta carpeta** | Igual que el anterior, clic derecho sobre una carpeta en el Explorer. | Sí |
| **AnzenCore: Analizar archivo actual** | Analiza solo el archivo abierto en el editor. | Sí |
| **AnzenCore: Analizar APK (vulnerabilidades móviles)** | Escanea un `.apk` en busca de secretos, HTTP inseguro, criptografía débil, WebView inseguro, IPs hardcodeadas, etc. | **No — 100% local y offline** |

Los resultados de code smells se muestran en un panel lateral (resumen + tabla por archivo) y también aparecen como advertencias en el panel **Problems**.

### Análisis de APK (local)

El escaneo de APK reimplementa la lógica de `ApkAnalyzer` (backend Python) directamente en TypeScript — no sube el archivo a ningún servidor, así que funciona sin conexión y es instantáneo. Se activa:

- Clic derecho sobre un `.apk` en el Explorer → **AnzenCore: Analizar APK**.
- Desde la Command Palette (abre un selector de archivo si no hay uno seleccionado).
- Automáticamente al correr **Analizar Workspace**/**Analizar esta carpeta**: si se detectan `.apk` en el proyecto, se ofrece analizarlos.

Los hallazgos (con severidad, CWE, OWASP Mobile, evidencia y recomendación) se muestran en un panel dedicado. Como el archivo `.apk` es un binario, estos hallazgos no navegan a líneas de un archivo del workspace (a diferencia de los code smells).

## Configuración

| Setting | Default | Descripción |
| --- | --- | --- |
| `anzencore.apiBaseUrl` | `http://localhost:8000` | URL de la API (local o desplegada en Azure). |
| `anzencore.excludeGlobs` | node_modules, .git, .venv, venv, __pycache__, dist, build, .pytest_cache | Carpetas a ignorar al recolectar archivos. |
| `anzencore.maxFileSizeKb` | `512` | Tamaño máximo por archivo a incluir. |

> **Nota:** los "code smells" que devuelve la API son mensajes a nivel de archivo (no incluyen número de línea exacto), por lo que las advertencias en el panel Problems se anclan a la línea 1 del archivo.

## Desarrollo

```powershell
npm install
npm run watch
```

Presiona `F5` en VS Code (con esta carpeta abierta) para lanzar el Extension Development Host y probar los comandos.

## Publicar en el Marketplace

1. Reemplaza `media/icon.png` por el logo real de AnzenCore (el actual es un placeholder).
2. Crea/actualiza tu publisher en https://marketplace.visualstudio.com/manage y actualiza el campo `publisher` en `package.json`.
3. `npm install -g @vscode/vsce`
4. `vsce login <tu-publisher>` (requiere un Personal Access Token de Azure DevOps con scope *Marketplace: Manage*).
5. `vsce publish` (o `vsce package` para generar solo el `.vsix` y subirlo manualmente).
