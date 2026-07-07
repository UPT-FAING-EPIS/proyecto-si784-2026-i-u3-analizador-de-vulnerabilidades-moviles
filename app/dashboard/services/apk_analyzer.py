import re
import zipfile
from dataclasses import dataclass, field
from io import BytesIO


SEVERITY_ORDER = {
    "Info": 0,
    "Bajo": 1,
    "Medio": 2,
    "Alto": 3,
    "Critico": 4,
}


@dataclass
class ApkFinding:
    finding_type: str
    title: str
    severity: str
    description: str
    evidence: str | None = None
    recommendation: str | None = None
    source_file: str | None = None
    cwe: str | None = None
    owasp_mobile: str | None = None


@dataclass
class ApkArtifact:
    artifact_type: str
    artifact_value: str
    source_file: str | None = None


@dataclass
class ApkAnalysisResult:
    status: str = "completed"
    summary: str = ""
    severity_max: str | None = None
    findings: list[ApkFinding] = field(default_factory=list)
    artifacts: list[ApkArtifact] = field(default_factory=list)
    error_message: str | None = None


class ApkAnalyzer:
    text_file_extensions = (
        ".xml",
        ".json",
        ".txt",
        ".html",
        ".js",
        ".properties",
        ".MF",
        ".RSA",
        ".SF",
    )

    url_pattern = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+")
    secret_patterns = [  # nosonar - these regexes detect secrets in APK files, not store credentials
        re.compile(r"(?i)(api[_-]?key|apikey|secret|token|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{16,})"),  # nosonar
        re.compile(r"sb_publishable_[A-Za-z0-9_\-]+"),  # nosonar
        re.compile(r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+"),  # nosonar
    ]
    
    crypto_patterns = [
        re.compile(r"MessageDigest\.getInstance\(\s*[\"'](MD5|SHA-1)[\"']\s*\)", re.IGNORECASE),
        re.compile(r"Cipher\.getInstance\(\s*[\"'](DES|DESede|AES/ECB/PKCS5Padding)[\"']\s*\)", re.IGNORECASE)
    ]
    
    webview_patterns = [
        re.compile(r"setJavaScriptEnabled\(\s*true\s*\)")
    ]
    
    random_patterns = [
        re.compile(r"new\s+java\.util\.Random\(\s*\)")
    ]
    
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

    ignored_http_prefixes = (
        "http://www.apache.org/licenses/",
        "http://schemas.android.com/",
        "http://ns.adobe.com/",
        "http://www.w3.org/",
    )

    def analyze(self, file_bytes):
        result = ApkAnalysisResult()
        try:
            with zipfile.ZipFile(BytesIO(file_bytes)) as apk_zip:
                file_names = apk_zip.namelist()
                result.artifacts.extend(self._build_structure_artifacts(file_names))
                result.findings.extend(self._analyze_structure(file_names))

                text_samples = self._read_text_samples(apk_zip, file_names)
                result.artifacts.extend(self._extract_url_artifacts(text_samples))
                result.findings.extend(self._detect_insecure_http(text_samples))
                result.findings.extend(self._detect_possible_secrets(text_samples))
                result.findings.extend(self._detect_weak_crypto(text_samples))
                result.findings.extend(self._detect_insecure_webview(text_samples))
                result.findings.extend(self._detect_insecure_random(text_samples))
                result.findings.extend(self._detect_hardcoded_ips(text_samples))

            result.findings = self._deduplicate_findings(result.findings)
            result.artifacts = self._deduplicate_artifacts(result.artifacts)
            result.severity_max = self._max_severity(result.findings)
            result.summary = (
                f"Analisis completado: {len(result.findings)} hallazgos y "
                f"{len(result.artifacts)} artefactos extraidos."
            )
        except zipfile.BadZipFile:
            result.status = "failed"
            result.error_message = "El archivo no es un APK valido o esta corrupto."
            result.summary = result.error_message
        except Exception as exc:
            result.status = "failed"
            result.error_message = f"Error analizando APK: {exc}"
            result.summary = result.error_message
        return result

    def _build_structure_artifacts(self, file_names):
        artifacts = []
        dex_count = len([name for name in file_names if name.endswith(".dex")])
        native_libs = [name for name in file_names if name.startswith("lib/") and name.endswith(".so")]

        artifacts.append(ApkArtifact("dex_count", str(dex_count)))
        artifacts.append(ApkArtifact("file_count", str(len(file_names))))
        for lib in native_libs[:50]:
            artifacts.append(ApkArtifact("native_library", lib, lib))
        return artifacts

    def _analyze_structure(self, file_names):
        findings = []
        if "AndroidManifest.xml" not in file_names:
            findings.append(
                ApkFinding(
                    finding_type="manifest",
                    title="AndroidManifest.xml no encontrado",
                    severity="Alto",
                    description="No se encontro el manifiesto principal del APK.",
                    recommendation="Verificar que el archivo APK no este corrupto o manipulado.",
                    owasp_mobile="M8",
                )
            )

        dex_files = [name for name in file_names if name.endswith(".dex")]
        if not dex_files:
            findings.append(
                ApkFinding(
                    finding_type="dex",
                    title="Archivo DEX no encontrado",
                    severity="Alto",
                    description="No se encontraron clases DEX dentro del APK.",
                    recommendation="Validar integridad del APK.",
                )
            )
        elif len(dex_files) > 1:
            findings.append(
                ApkFinding(
                    finding_type="dex",
                    title="MultiDex detectado",
                    severity="Info",
                    description=f"Se detectaron {len(dex_files)} archivos DEX.",
                    evidence=", ".join(dex_files[:10]),
                    recommendation="Revisar clases decompiladas durante el analisis profundo.",
                )
            )

        if any(name.startswith("lib/") and name.endswith(".so") for name in file_names):
            findings.append(
                ApkFinding(
                    finding_type="native_code",
                    title="Librerias nativas detectadas",
                    severity="Medio",
                    description="El APK incluye codigo nativo, lo que puede ocultar logica sensible o controles de seguridad.",
                    recommendation="Analizar las librerias nativas con herramientas especializadas.",
                    owasp_mobile="M7",
                )
            )
            
        db_files = [name for name in file_names if name.endswith((".db", ".sqlite", ".sqlite3"))]
        if db_files:
            findings.append(
                ApkFinding(
                    finding_type="internal_database",
                    title="Bases de datos locales empaquetadas",
                    severity="Medio",
                    description="Se detectaron archivos de base de datos dentro del APK, lo que puede revelar datos de prueba o estructura del esquema.",
                    evidence="Archivos encontrados:\n" + "\n".join(db_files[:5]),
                    recommendation="Asegurarse de no empaquetar bases de datos pre-pobladas con datos sensibles en producción.",
                    owasp_mobile="M1",
                )
            )
            
        return findings

    def _read_text_samples(self, apk_zip, file_names):
        samples = []
        readable_names = [
            name
            for name in file_names
            if name.endswith(self.text_file_extensions) or name.endswith(".dex")
        ]
        for name in readable_names[:250]:
            try:
                data = apk_zip.read(name)
            except Exception:
                continue
            if len(data) > 1_000_000:
                data = data[:1_000_000]
            text = data.decode("utf-8", errors="ignore").replace("\x00", "")
            if text:
                samples.append((name, text))
        return samples

    def _extract_url_artifacts(self, text_samples):
        artifacts = []
        for source_file, text in text_samples:
            for url in self.url_pattern.findall(text):
                artifacts.append(ApkArtifact("url", url, source_file))
        return artifacts[:200]

    def _detect_insecure_http(self, text_samples):
        insecure_evidence = []
        for source_file, text in text_samples:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                urls = self.url_pattern.findall(line)
                for url in urls:
                    if url.lower().startswith("http://") and not url.lower().startswith(self.ignored_http_prefixes):
                        start = max(0, i - 1)
                        end = min(len(lines), i + 2)
                        context = "\n".join(lines[start:end])
                        insecure_evidence.append((url, source_file, context))
                        
        unique_urls = {}
        for url, source, context in insecure_evidence:
            if url not in unique_urls:
                unique_urls[url] = (source, context)
                
        if not unique_urls:
            return []
            
        sources = sorted({src for src, ctx in unique_urls.values()})[:5]
        
        # Build evidence with code context
        evidence_text = "Se encontraron URLs HTTP en el código:\n"
        for idx, (url, (source, context)) in enumerate(list(unique_urls.items())[:3]):
            evidence_text += f"\nArchivo: {source}\nCódigo encontrado:\n```java\n{context}\n```\n"

        recommendation_text = """Usar HTTPS y validar certificados correctamente.

**Solución en código sugerida (Android/Java):**
```java
// ❌ Código vulnerable:
// URL url = new URL("http://ejemplo.com/api");

// ✅ Código seguro (cambiar http por https):
URL url = new URL("https://ejemplo.com/api");
HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
```
"""

        return [
            ApkFinding(
                finding_type="insecure_communication",
                title="Uso de HTTP no cifrado",
                severity="Alto",
                description="Se detectaron endpoints HTTP sin cifrado dentro del APK.",
                evidence=evidence_text,
                recommendation=recommendation_text,
                source_file=", ".join(sources),
                cwe="CWE-319",
                owasp_mobile="M5",
            )
        ]

    def _detect_possible_secrets(self, text_samples):
        findings = []
        for source_file, text in text_samples:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                for pattern in self.secret_patterns:
                    matches = pattern.findall(line)
                    if matches:
                        start = max(0, i - 1)
                        end = min(len(lines), i + 2)
                        raw_context = "\n".join(lines[start:end])
                        
                        # Use search to find the exact matched string to mask it
                        match_obj = pattern.search(line)
                        if match_obj:
                            # Usually the secret is in the last group or the whole match
                            full_match = match_obj.group(0)
                            safe_match = self._mask_secret(full_match)
                            context = raw_context.replace(full_match, safe_match)
                        else:
                            context = raw_context

                        evidence_text = f"Código encontrado:\n```java\n{context}\n```"
                        
                        recommendation_text = """Eliminar secretos del código fuente y moverlos a un backend seguro o a configuraciones protegidas.

**Solución en código sugerida (Android/Java):**
```java
// ❌ Código vulnerable (Hardcoded):
// String apiKey = "1234567890abcdef1234567890abcdef";

// ✅ Código seguro (Usar BuildConfig o Keystore):
// 1. En tu archivo local.properties añade: MY_API_KEY="123456..."
// 2. En build.gradle: buildConfigField "String", "API_KEY", properties.getProperty("MY_API_KEY")
// 3. En tu código Java/Kotlin:
String apiKey = BuildConfig.API_KEY;
```
"""

                        findings.append(
                            ApkFinding(
                                finding_type="hardcoded_secret",
                                title="Posible secreto hardcodeado",
                                severity="Critico",
                                description="Se detectaron patrones compatibles con tokens, secrets o API keys embebidas en el código.",
                                evidence=evidence_text,
                                recommendation=recommendation_text,
                                source_file=source_file,
                                cwe="CWE-798",
                                owasp_mobile="M9",
                            )
                        )
        return findings

    def _extract_context(self, lines, line_idx):
        start = max(0, line_idx - 1)
        end = min(len(lines), line_idx + 2)
        return "\n".join(lines[start:end])

    def _detect_weak_crypto(self, text_samples):
        findings = []
        for source_file, text in text_samples:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                for pattern in self.crypto_patterns:
                    if pattern.search(line):
                        context = self._extract_context(lines, i)
                        evidence_text = f"Archivo: {source_file}\nCódigo encontrado:\n```java\n{context}\n```"
                        recommendation_text = """Evitar el uso de algoritmos criptográficos rotos o débiles (MD5, SHA-1, DES, ECB).

**Solución en código sugerida (Android/Java):**
```java
// ❌ Código vulnerable:
// MessageDigest md = MessageDigest.getInstance("MD5");
// Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");

// ✅ Código seguro:
MessageDigest md = MessageDigest.getInstance("SHA-256");
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
```
"""
                        findings.append(
                            ApkFinding(
                                finding_type="weak_crypto",
                                title="Criptografía Débil o Insegura",
                                severity="Alto",
                                description="Se encontraron referencias a algoritmos criptográficos obsoletos y propensos a colisiones.",
                                evidence=evidence_text,
                                recommendation=recommendation_text,
                                source_file=source_file,
                                cwe="CWE-327",
                                owasp_mobile="M5",
                            )
                        )
        return findings

    def _detect_insecure_webview(self, text_samples):
        findings = []
        for source_file, text in text_samples:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                for pattern in self.webview_patterns:
                    if pattern.search(line):
                        context = self._extract_context(lines, i)
                        evidence_text = f"Archivo: {source_file}\nCódigo encontrado:\n```java\n{context}\n```"
                        recommendation_text = """Habilitar JavaScript en WebViews aumenta el riesgo de ataques Cross-Site Scripting (XSS).

**Solución en código sugerida (Android/Java):**
```java
// ❌ Código vulnerable:
// webView.getSettings().setJavaScriptEnabled(true);

// ✅ Código seguro: Solo habilitar si es estrictamente necesario y controlando el origen.
// Preferiblemente mantener desactivado si el contenido a cargar no lo requiere.
```
"""
                        findings.append(
                            ApkFinding(
                                finding_type="insecure_webview",
                                title="Configuración Insegura de WebView (XSS)",
                                severity="Medio",
                                description="Se ha habilitado la ejecución de JavaScript en un WebView, lo que podría permitir inyección de código malicioso.",
                                evidence=evidence_text,
                                recommendation=recommendation_text,
                                source_file=source_file,
                                cwe="CWE-79",
                                owasp_mobile="M7",
                            )
                        )
        return findings

    def _detect_insecure_random(self, text_samples):
        findings = []
        for source_file, text in text_samples:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                for pattern in self.random_patterns:
                    if pattern.search(line):
                        context = self._extract_context(lines, i)
                        evidence_text = f"Archivo: {source_file}\nCódigo encontrado:\n```java\n{context}\n```"
                        recommendation_text = """El generador 'java.util.Random' no es criptográficamente seguro y sus valores pueden ser predecibles.

**Solución en código sugerida (Android/Java):**
```java
// ❌ Código vulnerable:
// Random rand = new java.util.Random();

// ✅ Código seguro:
import java.security.SecureRandom;
SecureRandom secureRand = new SecureRandom();
```
"""
                        findings.append(
                            ApkFinding(
                                finding_type="insecure_random",
                                title="Generador de Números Aleatorios Inseguro",
                                severity="Bajo",
                                description="Uso de un PRNG predecible en lugar de un CSPRNG seguro.",
                                evidence=evidence_text,
                                recommendation=recommendation_text,
                                source_file=source_file,
                                cwe="CWE-330",
                                owasp_mobile="M5",
                            )
                        )
        return findings

    def _detect_hardcoded_ips(self, text_samples):
        findings = []
        ignored_ips = {"127.0.0.1", "0.0.0.0", "255.255.255.255"}
        for source_file, text in text_samples:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                matches = self.ip_pattern.findall(line)
                for ip in matches:
                    if ip in ignored_ips or ip.startswith("1.") or ip.startswith("2."):
                        continue
                    parts = ip.split(".")
                    if all(int(p) <= 255 for p in parts):
                        context = self._extract_context(lines, i)
                        evidence_text = f"Archivo: {source_file}\nCódigo encontrado:\n```java\n{context}\n```"
                        recommendation_text = """Evitar dejar direcciones IP internas o externas quemadas en el código fuente.
Extraer a variables de entorno de compilación o resolver mediante DNS.
"""
                        findings.append(
                            ApkFinding(
                                finding_type="hardcoded_ip",
                                title="Dirección IP Hardcodeada detectada",
                                severity="Bajo",
                                description=f"Se detectó una dirección IP ({ip}) dentro del código compilado.",
                                evidence=evidence_text,
                                recommendation=recommendation_text,
                                source_file=source_file,
                                cwe="CWE-200",
                                owasp_mobile="M9",
                            )
                        )
        return findings


    def _mask_secret(self, value):
        clean = value.replace("\\n", " ")
        if len(clean) <= 24:
            return clean[:4] + "***"
        return clean[:12] + "***" + clean[-6:]

    def _deduplicate_findings(self, findings):
        seen = set()
        unique = []
        for finding in findings:
            key = (finding.finding_type, finding.title, finding.source_file, finding.evidence)
            if key in seen:
                continue
            seen.add(key)
            unique.append(finding)
        return unique

    def _deduplicate_artifacts(self, artifacts):
        seen = set()
        unique = []
        for artifact in artifacts:
            key = (artifact.artifact_type, artifact.artifact_value)
            if key in seen:
                continue
            seen.add(key)
            unique.append(artifact)
        return unique

    def _max_severity(self, findings):
        if not findings:
            return "Info"
        return max(findings, key=lambda item: SEVERITY_ORDER[item.severity]).severity
