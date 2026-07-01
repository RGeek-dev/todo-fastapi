# main.py

from fastapi import FastAPI
from app.config.database import engine, Base
from app.models import todo as todo_model  # Must import to register with Base
from app.routes.todo_routes import router as todo_router

# Run migrations — creates tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="A CRUD Todo API built with FastAPI + PostgreSQL",
    version="1.0.0"
)

# Mount the router — like app.use('/todos', todoRouter) in Express
app.include_router(todo_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Todo API is running"}