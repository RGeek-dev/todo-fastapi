from pydantic import BaseModal, Field
from typing import Optional


class TodoBase(BaseModal):
    title: str = Field(...,min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=1000)
    completed: bool


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModal):
    title: Optional[str] = Field(None, min_length=1, max_length=255)