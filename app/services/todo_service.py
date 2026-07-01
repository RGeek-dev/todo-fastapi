# app/services/todo_service.py

from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

def get_all_todos(db: Session) -> list[Todo]:
    return db.query(Todo).order_by(Todo.created_at.desc()).all()

def get_todo_by_id(db: Session, todo_id: int) -> Todo | None:
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(db: Session, payload: TodoCreate) -> Todo:
    # model_dump() converts the Pydantic schema to a plain dict —
    # like calling .toObject() on a Mongoose doc, or zod.parse() returning a plain object.
    new_todo = Todo(**payload.model_dump())
    db.add(new_todo)
    db.commit()          # Writes to Postgres and ends the transaction
    db.refresh(new_todo) # Re-fetches the row — populates server-generated fields
                         # like 'id' and 'created_at' that didn't exist before commit
    return new_todo

def update_todo(db: Session, todo_id: int, payload: TodoUpdate) -> Todo | None:
    todo = get_todo_by_id(db, todo_id)
    if not todo:
        return None

    # exclude_unset=True only includes fields the client actually sent.
    # Without this, optional fields with None defaults would overwrite existing values.
    # Equivalent to: const updates = Object.fromEntries(Object.entries(body).filter(([,v]) => v !== undefined))
    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(todo, field, value)  # Like: todo[field] = value in JS

    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int) -> bool:
    todo = get_todo_by_id(db, todo_id)
    if not todo:
        return False
    db.delete(todo)
    db.commit()
    return True