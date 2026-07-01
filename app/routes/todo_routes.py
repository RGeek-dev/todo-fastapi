# app/routes/todo_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.controllers import todo_controller

# APIRouter is FastAPI's express.Router()
router = APIRouter(
    prefix="/todos",
    tags=["Todos"]  # Groups endpoints in the auto-generated /docs UI
)

@router.get("/", response_model=list[TodoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    return todo_controller.get_all(db)

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return todo_controller.get_one(todo_id, db)

@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    return todo_controller.create(payload, db)

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    return todo_controller.update(todo_id, payload, db)

@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return todo_controller.delete(todo_id, db)