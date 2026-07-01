# app/controllers/todo_controller.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.services import todo_service

def get_all(db: Session):
    return todo_service.get_all_todos(db)

def get_one(todo_id: int, db: Session):
    todo = todo_service.get_todo_by_id(db, todo_id)
    if not todo:
        # HTTPException is FastAPI's equivalent of res.status(404).json({message: '...'})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo

def create(payload: TodoCreate, db: Session):
    return todo_service.create_todo(db, payload)

def update(todo_id: int, payload: TodoUpdate, db: Session):
    todo = todo_service.update_todo(db, todo_id, payload)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo

def delete(todo_id: int, db: Session):
    success = todo_service.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    # Return 204 No Content — FastAPI needs an explicit Response object for this
    from fastapi import Response
    return Response(status_code=status.HTTP_204_NO_CONTENT)