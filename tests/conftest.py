import os
import pytest
import requests
from dotenv import load_dotenv

from api_client.base import BaseApiClient


@pytest.fixture(scope="session")
def session() -> requests.Session:
    return requests.Session()


# Load environment variables from .env file if present
load_dotenv()

@pytest.fixture(scope="session")
def todo_client(session: requests.Session) -> BaseApiClient:
    """A client for a Todo app running on localhost"""
    base_url = os.getenv('TODO_API_URL', 'http://127.0.0.1:8000')
    return BaseApiClient(base_url=base_url, session=session, timeout_s=5)


# The client is created only once for a run of the entire tests.
# Will be created for each test method if it's "function"
@pytest.fixture(scope="session")
def httpbin_client(session: requests.Session) -> BaseApiClient:
    base_url = os.getenv('HTTPBIN_URL', 'https://httpbin.org')
    return BaseApiClient(base_url=base_url, session=session, timeout_s=10)


@pytest.fixture(scope="session")
def dummyjson_client(session: requests.Session) -> BaseApiClient:
    base_url = os.getenv('DUMMYJSON_URL', 'https://dummyjson.com')
    return BaseApiClient(base_url=base_url, session=session, timeout_s=10)


# auto_use is True for fixtures that should be done before/after every test.
# No need to be passed on to test functions as an argument.
@pytest.fixture(autouse=True)
def debug_on_failure(request, httpbin_client, dummyjson_client, todo_client):
    """
    Print last API request and response if a test fails.
    Automatically run for any tests because auto_use is True。
    """
    yield  # Control passed to the test function

    # Teardown is done here, irrespective of pass/fail of the test.
    clients = [httpbin_client, dummyjson_client, todo_client]

    # Always print out the latest request as it's hard to detect test failure.
    # Need to add -rF option to actually output to the console.

    print("\n\n=== [DEBUG] Last API Call Info ===")
    for client in clients:
        if client.last_request:
            print(f"--- Client: {client.base_url} ---")
            print(f"Request:  {client.last_request}")
            if client.last_response is not None:
                print(f"Response: {client.last_response.status_code} {client.last_response.reason}")
                print(f"Body: {client.last_response.text[:200]}...")
            print("--------------------------------")