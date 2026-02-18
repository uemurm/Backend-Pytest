import os
import pytest
from playwright.sync_api import Playwright, APIRequestContext, expect

# Define the base URL for the API
BASE_URL = os.getenv("TODO_API_URL", "http://127.0.0.1:8000")

@pytest.fixture(scope="module")
def api_context(playwright: Playwright) -> APIRequestContext:
    """
    Create an APIRequestContext for the test module.
    This context will be reused for all tests in this module.
    """
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()

def test_playwright_get_todos(api_context: APIRequestContext):
    """
    Test GET /todos using Playwright APIRequestContext
    """
    # Send GET request
    response = api_context.get("/todos")
    
    # Assert status code
    assert response.ok
    assert response.status == 200
    
    # Assert response body
    todos = response.json()
    assert isinstance(todos, list)

def test_playwright_create_todo(api_context: APIRequestContext):
    """
    Test POST /todos using Playwright APIRequestContext
    """
    new_todo = {
        "id": 901,
        "title": "Playwright API Test",
        "completed": False
    }
    
    # Send POST request
    response = api_context.post("/todos", data=new_todo)
    
    # Assert status code
    assert response.ok
    assert response.status == 201
    
    # Assert response body
    created_todo = response.json()
    assert created_todo["id"] == new_todo["id"]
    assert created_todo["title"] == new_todo["title"]

    # Cleanup (Delete the created todo)
    delete_response = api_context.delete(f"/todos/{new_todo['id']}")
    assert delete_response.ok
