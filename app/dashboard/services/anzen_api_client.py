import requests

from app.dashboard.config.settings import DashboardSettings


class AnzenApiClient:
    def __init__(self, url=None, folder_url=None, timeout=180):
        self.url = url or DashboardSettings.anzen_external_url
        self.folder_url = folder_url or DashboardSettings.anzen_folder_url
        self.timeout = timeout

    def analizar_repo_github(self, repo_url):
        response = requests.post(
            self.url,
            files={"repo_url": (None, repo_url)},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def analizar_carpeta(self, project_name: str, file_list: list):
        files_param = [("files", (name, content, "application/octet-stream")) for name, content in file_list]
        response = requests.post(
            self.folder_url,
            data={"project_name": project_name},
            files=files_param,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
