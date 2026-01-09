import pytest
from api_client.base import BaseApiClient

success_status = [
    200,    # OK
    201,    # Created
    202,    # Accepted
    204,    # No Content (ex. successful deletion)
]
@pytest.mark.parametrize("status_code", success_status)
def test_status_codes_success(httpbin_client: BaseApiClient, status_code: int):
    response = httpbin_client.get(f"status/{status_code}")

    assert response.status_code == status_code

failure_status = [
    400,    # Bad Request
    401,    # Unauthorised
    404,    # Not Found
    500,    # Internal Server Error
]
@pytest.mark.parametrize("status_code", failure_status)
def test_status_codes_failure(httpbin_client: BaseApiClient, status_code: int):
    response = httpbin_client.get(f"status/{status_code}")

    assert response.status_code == status_code
