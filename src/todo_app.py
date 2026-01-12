from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define Pydantic model for request/response validations.
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

# In-memory DB, which clears when the server restarts.
todos_db: list[Todo] = []

@app.get("/todos", response_model=list[Todo])
def get_todos():
    return todos_db

@app.post("/todos", status_code=201, response_model=Todo)
def create_todo(todo: Todo):
    # Check if the ID already exists.
    for t in todos_db:
        if t.id == todo.id:
            raise HTTPException(status_code=400, detail="ID already exists")
    
    todos_db.append(todo)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            todos_db.pop(index)
            return None

    raise HTTPException(status_code=404, detail="Todo not found")
