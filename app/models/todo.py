# app/models/todo.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class Todo(Base):
    # __tablename__ is mandatory — SQLAlchemy uses this as the actual Postgres table name
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)

    # func.now() calls Postgres's NOW() on insert — server-side default.
    # This differs from Python's datetime.utcnow (client-side) —
    # server_default is more reliable across timezones and deployments.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())