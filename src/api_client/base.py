from dataclasses import dataclass
from typing import Any
import requests


@dataclass
class BaseApiClient:
    base_url: str
    session: requests.Session
    timeout_s: float = 10.0

    last_request: dict[str, Any] | None = None
    # This can be either Response or None. Initialise it to None.
    last_response: requests.Response | None = None

    def _url(self, path: str) -> str:
        return self.base_url.rstrip("/") + "/" + path.lstrip("/")

    def get(self, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        self.last_request = {"method": "GET", "url": url, "kwargs": kwargs}
        response = self.session.get(self._url(path), timeout=self.timeout_s, **kwargs)
        self.last_response = response

        return response

    def post(self, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        self.last_request = {"method": "POST", "url": url, "kwargs": kwargs}

        response = self.session.post(url, timeout=self.timeout_s, **kwargs)
        self.last_response = response
        return response
