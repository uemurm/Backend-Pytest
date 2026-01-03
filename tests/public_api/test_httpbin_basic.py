import pytest

pytestmark = pytest.mark.smoke


def test_httpbin_get_echoes_args(httpbin_client):
    r = httpbin_client.get("/get", params={"q": "hello"})
    assert r.status_code == 200

    body = r.json()
    assert body["args"]["q"] == "hello"


def test_httpbin_status_404(httpbin_client):
    r = httpbin_client.get("/status/404")
    assert r.status_code == 404
