import pytest
from todo_app import Todo
from api_client.base import BaseApiClient


@pytest.fixture
def managed_todo_id(todo_client: BaseApiClient):
    """ Manage Todo ID's then delete after tests"""
    todo_id = 101
    # Use session directly to avoid overwriting last_request/response
    url = f'{todo_client.base_url}/todos/{todo_id}'
    todo_client.session.delete(url)

    yield todo_id

    # Teardown
    todo_client.session.delete(url)


class TestTodoOperations:
    """Test happy path"""

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
        # Pydantic v2 way to dump model to dict
        assert target_todo.model_dump() == new_todo

    def test_create_todo_default_values(self, todo_client: BaseApiClient):
        """
        Verify that 'completed' defaults to False if missing.
        """
        # 'completed' is missing, but it should be valid (default=False)
        new_todo = {'id': 202, 'title': 'Defaults Test'}
        
        res = todo_client.post('todos', json=new_todo)
        assert res.status_code == 201
        
        created = Todo(**res.json())
        assert created.completed is False

        # Cleanup
        todo_client.delete(f'todos/{created.id}')

    class TestVariousID:
        def test_create_without_id(self, todo_client: BaseApiClient):
            """
            Verify that a request without ID results in Unprocessable Entity (422)
            """
            new_todo = {
                'title': 'Learn Pytest',
                'completed': False,
            }

            post_res = todo_client.post('todos', json=new_todo)
            assert post_res.status_code == 422

        def test_create_with_id_0(self, todo_client: BaseApiClient):
            """
            Verify that a request with ID being 0 results in Created (201)
            """
            new_todo = {
                'id': 0,
                'title': 'Learn Pytest',
                'completed': False,
            }

            post_res = todo_client.post('todos', json=new_todo)
            assert post_res.status_code == 201

        def test_create_with_negative_id(self, todo_client: BaseApiClient):
            """
            Verify that a request with ID being -1 results in Unprocessable Entity (422)
            """
            new_todo = {
                'id': -1,
                'title': 'Learn Pytest',
                'completed': False,
            }

            post_res = todo_client.post('todos', json=new_todo)
            assert post_res.status_code == 422

        def test_create_with_string_id(self, todo_client: BaseApiClient):
            """
            Verify that a request with ID being 'foo' results in Unprocessable Entity (422)
            """
            new_todo = {
                'id': 'foo',
                'title': 'Learn Pytest',
                'completed': False,
            }

            post_res = todo_client.post('todos', json=new_todo)
            assert post_res.status_code == 422

        def test_create_with_id_being_numerical_string(self, todo_client: BaseApiClient):
            """
            Verify that a request with ID being '123'
            """
            new_todo = {
                'id': '123',
                'title': 'Learn Pytest',
                'completed': False,
            }

            post_res = todo_client.post('todos', json=new_todo)
            assert post_res.status_code == 201

            # Verify if the response comply with Todo model.
            created_todo = Todo(**post_res.json())
            assert created_todo.id == int(new_todo['id'])
            assert created_todo.title == new_todo['title']
            assert created_todo.completed is new_todo['completed']

    class TestVariousTitle:
        def test_create_without_title(self):
            """
            Verify that a request without title results in
            """
            pass

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


class TestTodoErrors:
    """Test error cases"""

    def test_create_todo_duplicate_id(self, todo_client: BaseApiClient, managed_todo_id: int):
        """
        Verify that creating a Todo with an existing ID returns 400.
        """
        new_todo = {'id': managed_todo_id, 'title': 'Original', 'completed': False}
        
        # 1. Create the first one
        res1 = todo_client.post('todos', json=new_todo)
        assert res1.status_code == 201

        # 2. Try to create again with the same ID
        res2 = todo_client.post("todos", json=new_todo)
        assert res2.status_code == 400
        assert res2.json()['detail'] == 'ID already exists'

    @pytest.mark.parametrize('missing_field', ['id', 'title'])
    def test_create_todo_validation_error(self, todo_client: BaseApiClient, missing_field: str):
        """
        Verify that missing required fields returns 422 (FastAPI default).
        """
        todo_data = {'id': 200, 'title': 'Test', 'completed': False}
        # Remove a required field
        del todo_data[missing_field]
        
        invalid_todo = todo_data
        res = todo_client.post('todos', json=invalid_todo)
        assert res.status_code == 422

    def test_delete_non_existent_todo(self, todo_client: BaseApiClient):
        """
        Verify that deleting a non-existent Todo returns 404.
        """
        res = todo_client.delete('todos/99999')
        assert res.status_code == 404
        assert res.json()['detail'] == 'Todo not found'
