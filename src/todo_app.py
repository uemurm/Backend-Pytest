from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict

import models
import database

# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# --- Pydantic Models (Schema) ---
# Used for request/response validation
class TodoSchema(BaseModel):
    id: int = Field(ge=0)   # Greater than or Equal to 0.
    title: str
    completed: bool = False

    model_config = ConfigDict(from_attributes=True)

# --- API Endpoints ---

@app.get("/todos", response_model=list[TodoSchema])
def get_todos(db: Session = Depends(database.get_db)):
    # Fetch all todos from the database
    todos = db.query(models.Todo).all()
    return todos

@app.post("/todos", status_code=201, response_model=TodoSchema)
def create_todo(todo: TodoSchema, db: Session = Depends(database.get_db)):
    # Check if ID already exists
    existing_todo = db.query(models.Todo).filter(models.Todo.id == todo.id).first()
    if existing_todo:
        raise HTTPException(status_code=400, detail="ID already exists")

    # Create new DB model instance
    db_todo = models.Todo(
        id=todo.id,
        title=todo.title,
        completed=todo.completed
    )
    
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo) # Refresh to get any default values from DB
    
    return db_todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(database.get_db)):
    # Find the todo
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return None
