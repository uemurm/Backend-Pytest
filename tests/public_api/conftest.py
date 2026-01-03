import pytest
import requests

from api_client.base import BaseApiClient


@pytest.fixture(scope="session")
def session() -> requests.Session:
    return requests.Session()


@pytest.fixture(scope="session")
def httpbin_client(session: requests.Session) -> BaseApiClient:
    return BaseApiClient(base_url="https://httpbin.org", session=session, timeout_s=10)


@pytest.fixture(scope="session")
def dummyjson_client(session: requests.Session) -> BaseApiClient:
    return BaseApiClient(base_url="https://dummyjson.com", session=session, timeout_s=10)
