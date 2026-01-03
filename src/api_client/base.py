from dataclasses import dataclass
import requests


@dataclass
class BaseApiClient:
    base_url: str
    session: requests.Session
    timeout_s: float = 10.0

    def _url(self, path: str) -> str:
        return self.base_url.rstrip("/") + "/" + path.lstrip("/")

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(self._url(path), timeout=self.timeout_s, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.session.post(self._url(path), timeout=self.timeout_s, **kwargs)