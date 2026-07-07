import os

import requests

_DEFAULT_URL = os.getenv("SECURITY_API_URL", "http://38.250.116.71:8000")
_DEFAULT_TOKEN = os.getenv("SECURITY_API_TOKEN", "c9a95739-03e5-44b4-ab75-b7f61996149c")


class ExternalSecurityClient:
    def __init__(self, base_url: str | None = None, token: str | None = None, timeout: int = 60):
        self.base_url = (base_url or _DEFAULT_URL).rstrip("/")
        self.token = token or _DEFAULT_TOKEN
        self.timeout = timeout

    @property
    def _headers(self):
        return {"X-API-Key": self.token, "Content-Type": "application/json"}

    def analyze(self, target_type: str, target_value: str) -> dict:
        resp = requests.post(
            f"{self.base_url}/analyze/api",
            json={"target_type": target_type, "target_value": target_value},
            headers=self._headers,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def get_reports(self) -> list:
        resp = requests.get(
            f"{self.base_url}/reports/api",
            headers=self._headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def get_report(self, scan_id: int) -> dict:
        resp = requests.get(
            f"{self.base_url}/reports/api/{scan_id}",
            headers=self._headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def check_health(self) -> dict:
        resp = requests.get(f"{self.base_url}/health", timeout=10)
        resp.raise_for_status()
        return resp.json()
