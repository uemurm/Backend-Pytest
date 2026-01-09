import pytest
from pydantic import BaseModel, HttpUrl

pytestmark = pytest.mark.smoke


def test_httpbin_get_echoes_args(httpbin_client):
    r = httpbin_client.get("/get", params={"q": "hello"})
    assert r.status_code == 200

    body = r.json()
    assert body["args"]["q"] == "hello"


class HttpBinResponse(BaseModel):
    # Move these to `src/schemas/httpbin.py` later.
    args: dict[str, str]
    headers: dict[str, str]
    origin: str
    url: HttpUrl


def test_httpbin_get_with_pydantic(httpbin_client):
    test_param = 'pydantic_test'
    response = httpbin_client.get('/get', params={'q': test_param})
    assert response.status_code == 200

    # Convert the JSON of the response body to the model.
    # It's automatically validated here such as mandatory fields and types.
    model = HttpBinResponse(**response.json())

    assert model.args['q'] == test_param
    assert str(model.url) == f"https://httpbin.org/get?q={test_param}"


def test_httpbin_status_404(httpbin_client):
    r = httpbin_client.get("/status/404")
    assert r.status_code == 404
