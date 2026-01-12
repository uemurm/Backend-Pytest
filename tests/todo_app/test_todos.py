import pytest
from todo_app import Todo
from api_client.base import BaseApiClient


class TestTodoApp:

    @pytest.fixture
    def managed_todo_id(self, todo_client: BaseApiClient):
        """ Manage Todo ID's then delete after tests"""
        todo_id = 101
        # Use session directly to avoid overwriting last_request/response
        url = f'{todo_client.base_url}/todos/{todo_id}'
        todo_client.session.delete(url)
        
        yield todo_id
        
        # Teardown
        todo_client.session.delete(url)

    def test_create_and_get_todo(self, todo_client: BaseApiClient, managed_todo_id: int):
        """
        Verify if a Todo is created then retrieved.
        """
        new_todo = {
            "id": managed_todo_id,
            "title": "Learn Pytest",
            "completed": False
        }

        post_res = todo_client.post('todos', json=new_todo)
        assert post_res.status_code == 201

        # Verify if the response comply with Todo model.
        created_todo = Todo(**post_res.json())
        assert created_todo.id == managed_todo_id
        assert created_todo.title == 'Learn Pytest'
        assert created_todo.completed is False

        # 2. Get the list of Todos
        get_res = todo_client.get('todos')
        assert get_res.status_code == 200
        
        # Verify that the list contains the Todo created earlier.
        todos = [Todo(**item) for item in get_res.json()]
        # Find an item with ID being `managed_todo_id`
        target_todo = next((t for t in todos if t.id == managed_todo_id), None)

        assert target_todo is not None
        assert dict(target_todo) == new_todo

    def test_delete_todo(self, todo_client: BaseApiClient):
        """
        Verify if Todo can be deleted.
        """
        # Create a Todo to be deleted.
        todo_id = 999
        todo_client.post("todos", json={"id": todo_id, "title": "To be deleted", "completed": True})

        del_res = todo_client.delete(f'todos/{todo_id}')
        assert del_res.status_code == 204
        
        # There should be no Todo with the ID.
        get_res = todo_client.get("todos")
        todos = [Todo(**item) for item in get_res.json()]
        assert not any(t.id == todo_id for t in todos)
