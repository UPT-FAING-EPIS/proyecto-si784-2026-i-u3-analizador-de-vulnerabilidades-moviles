import requests

from app.api.config.settings import ApiSettings


class ExternalQualityClient:
    def __init__(self, url=None, timeout=30):
        self.url = url or ApiSettings.anzen_external_url
        self.timeout = timeout

    def analizar_repo(self, repo_url):
        response = requests.post(
            self.url,
            files={"repo_url": (None, repo_url)},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
