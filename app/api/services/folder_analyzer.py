import re


# Mirror detection patterns from ApkAnalyzer for consistency
_SECRET_PATTERNS = [  # nosonar - these regexes detect secrets in source files, not store credentials
    re.compile(r"(?i)(api[_-]?key|apikey|secret|token|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{16,})"),  # nosonar
    re.compile(r"sb_publishable_[A-Za-z0-9_\-]+"),  # nosonar
    re.compile(r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+"),  # nosonar
]
_HTTP_PATTERN = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+")
_IGNORED_HTTP_PREFIXES = (
    "http://www.apache.org/licenses/",
    "http://schemas.android.com/",
    "http://ns.adobe.com/",
    "http://www.w3.org/",
)
_CRYPTO_PATTERNS = [
    re.compile(r"MessageDigest\.getInstance\(\s*[\"'](MD5|SHA-1)[\"']\s*\)", re.IGNORECASE),
    re.compile(r"Cipher\.getInstance\(\s*[\"'](DES|DESede|AES/ECB/PKCS5Padding)[\"']\s*\)", re.IGNORECASE),
]
_WEBVIEW_PATTERN = re.compile(r"setJavaScriptEnabled\(\s*true\s*\)")
_RANDOM_PATTERN = re.compile(r"new\s+java\.util\.Random\(\s*\)")
_IP_PATTERN = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
_IGNORED_IPS = {"127.0.0.1", "0.0.0.0", "255.255.255.255"}

# Decision points that contribute to cyclomatic complexity
_COMPLEXITY_TOKENS = re.compile(
    r"\b(if|else\s+if|elif|for|while|do|switch|case|catch)\b|&&|\|\||\?(?![\?:])"
)

# NOM: method/function declarations across Java, Kotlin, Python, JS/TS, C#
_METHOD_PATTERN = re.compile(
    r"(?:"
    r"(?:public|private|protected|static|final|async|override|abstract)\s+[\w<>\[\]?]+\s+\w+\s*\("
    r"|^\s*(?:async\s+)?function\s+\w+\s*\("
    r"|^\s*(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>"
    r"|^\s*def\s+\w+\s*\("
    r"|^\s*fun\s+\w+\s*\("
    r")",
    re.MULTILINE,
)

# NOA: field/attribute/property declarations
_ATTR_PATTERN = re.compile(
    r"(?:"
    r"(?:private|protected|public|internal|final|static)\s+[\w<>\[\]?]+\s+\w+\s*[;=]"
    r"|^\s*(?:val|var)\s+\w+\s*(?::|=)"
    r"|^\s*self\.\w+\s*="
    r")",
    re.MULTILINE,
)


class FolderAnalyzer:
    def analyze_folder(self, project_name: str, files: list[tuple[str, bytes]]) -> dict:
        file_results = []
        for file_path, content_bytes in files:
            content = content_bytes.decode("utf-8", errors="ignore")
            file_results.append(self._analyze_file(file_path, content))

        total_loc = sum(f["loc"] for f in file_results)
        total_complexity = sum(f["complexity"] for f in file_results)
        total_nom = sum(f["metrics"]["nom"] for f in file_results)
        total_noa = sum(f["metrics"]["noa"] for f in file_results)
        all_smells = [smell for f in file_results for smell in f["smells"]]

        return {
            "status": "success",
            "project_name": project_name,
            "loc": total_loc,
            "complexity": total_complexity,
            "code_smells": {
                "smells": all_smells,
                "metrics": {"nom": total_nom, "noa": total_noa},
                "files": file_results,
            },
        }

    def _analyze_file(self, file_path: str, content: str) -> dict:
        lines = content.splitlines()
        loc = sum(1 for line in lines if line.strip())
        complexity = 1 + len(_COMPLEXITY_TOKENS.findall(content))
        nom = len(_METHOD_PATTERN.findall(content))
        noa = len(_ATTR_PATTERN.findall(content))
        smells = self._detect_smells(file_path, lines)

        return {
            "file_path": file_path,
            "loc": loc,
            "complexity": complexity,
            "metrics": {"nom": nom, "noa": noa},
            "smells": smells,
        }

    def _detect_smells(self, file_path: str, lines: list[str]) -> list[str]:
        smells = []
        for line in lines:
            for pattern in _SECRET_PATTERNS:
                if pattern.search(line):
                    smells.append(f"Posible secreto hardcodeado detectado en {file_path}")
                    break

            for url in _HTTP_PATTERN.findall(line):
                if url.startswith("http://") and not url.startswith(_IGNORED_HTTP_PREFIXES):
                    smells.append(f"Comunicación HTTP insegura detectada: {url[:80]}")
                    break

            for pattern in _CRYPTO_PATTERNS:
                if pattern.search(line):
                    smells.append(f"Criptografía débil o insegura detectada en {file_path}")
                    break

            if _WEBVIEW_PATTERN.search(line):
                smells.append(f"WebView con JavaScript habilitado en {file_path}")

            if _RANDOM_PATTERN.search(line):
                smells.append(
                    f"Generador de números aleatorios inseguro (java.util.Random) en {file_path}"
                )

            for ip in _IP_PATTERN.findall(line):
                if ip not in _IGNORED_IPS and not ip.startswith(("1.", "2.")):
                    parts = ip.split(".")
                    if all(int(p) <= 255 for p in parts):
                        smells.append(f"Dirección IP hardcodeada ({ip}) detectada en {file_path}")
                        break

        return list(dict.fromkeys(smells))
