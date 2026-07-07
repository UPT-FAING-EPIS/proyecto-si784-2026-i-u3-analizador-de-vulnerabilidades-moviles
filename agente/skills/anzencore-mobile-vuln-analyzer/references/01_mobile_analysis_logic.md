# Ingeniería Inversa y Lógica de Análisis Móvil

Esta referencia contiene las lógicas centrales de ingeniería inversa estática para diseccionar APKs y buscar vulnerabilidades. El agente usará estas heurísticas para construir el motor de la herramienta.

## Proceso de Ingeniería Inversa (APK)
1. Recibir archivo binario (`.apk`).
2. Tratarlo como un archivo comprimido (`zipfile.ZipFile`) para extraer su contenido.
3. Extraer e identificar artefactos estructurales:
   - `AndroidManifest.xml`: Metadatos de la app.
   - `classes.dex` / `classes*.dex`: El código bytecode compilado (Dalvik/ART).
   - `lib/*.so`: Librerías nativas compiladas (C/C++).
   - Bases de datos locales (`.db`, `.sqlite`).

### Heurísticas Estructurales
- **Ausencia de AndroidManifest.xml**: Riesgo Alto. Indica manipulación maliciosa o corrupción del APK.
- **Ausencia de código (sin .dex)**: Riesgo Alto. App vacía o técnicas extremas de ofuscación.
- **Múltiples archivos .dex (MultiDex)**: Informativo.
- **Librerías Nativas (`lib/*.so`)**: Riesgo Medio. Puede ocultar código malicioso y dificulta la ingeniería inversa tradicional (CWE-427 / OWASP M7).
- **Bases de datos locales empaquetadas**: Riesgo Medio. A menudo filtran datos de testing o esquemas internos (OWASP M1).

## Análisis Estático por Expresiones Regulares (Patrones en texto bruto)

Al leer archivos `.dex`, `.xml`, `.properties` o `.js` extraídos del APK, debes aplicar expresiones regulares para "cazar" anomalías de seguridad:

1. **Uso de HTTP no cifrado (CWE-319, OWASP M5)**
   - Ignorar: URLs de esquemas XML comunes (`http://schemas.android.com/`, `http://www.w3.org/`).
   - Detectar: Patrón genérico `http://` que no esté en la lista blanca.
   - Recomendación: Forzar HTTPS.

2. **Extracción de Secrets y Tokens (CWE-798, OWASP M9)**
   - Regex: `(?i)(api[_-]?key|apikey|secret|token|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{16,})`
   - Regex JWT: `eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+`
   - **Regla Crítica**: Mostrar el hallazgo, pero **enmascarar** el valor real en el reporte para no exponer el token en pantalla.

3. **Criptografía Débil o Insegura (CWE-327, OWASP M5)**
   - Regex: `MessageDigest\.getInstance\(\s*[\"'](MD5|SHA-1)[\"']\s*\)`
   - Regex: `Cipher\.getInstance\(\s*[\"'](DES|DESede|AES/ECB/PKCS5Padding)[\"']\s*\)`

4. **WebViews Expuestos a XSS (CWE-79, OWASP M7)**
   - Regex: `setJavaScriptEnabled\(\s*true\s*\)`

5. **Entropía Débil / PRNG Inseguro (CWE-330)**
   - Regex: `new\s+java\.util\.Random\(\s*\)`

6. **IPs Hardcodeadas (CWE-200, OWASP M9)**
   - Extraer IPs IPv4 que no sean locales (`127.0.0.1`, `0.0.0.0`) ni de multicast/broadcast.

## Deduplicación
- Es vital limpiar los resultados. Agrupar hallazgos idénticos para evitar saturar el reporte (`set` por tipo, título y evidencia).
