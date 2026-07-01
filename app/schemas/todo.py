# app/schemas/todo.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Base fields shared across schemas
class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False

# Schema for POST /todos — what the client sends
class TodoCreate(TodoBase):
    pass  # Inherits all fields from TodoBase, nothing extra needed

# Schema for PUT /todos/:id — all fields optional for partial updates
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None

# Schema for responses — what we send back to the client
class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    # This is the critical config that bridges Pydantic and SQLAlchemy.
    # By default, Pydantic only reads dict keys. SQLAlchemy returns ORM
    # objects (not dicts). 'from_attributes=True' tells Pydantic to read
    # object attributes instead — so todo.id works, not todo['id'].
    model_config = {"from_attributes": True}