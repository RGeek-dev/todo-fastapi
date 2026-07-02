# main.py

import time
import logging
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from app.config.database import engine, Base
from app.models import todo as todo_model
from app.routes.todo_routes import router as todo_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables_with_retry(retries: int = 5, delay: int = 3):
    """
    Retries create_all() if Postgres isn't ready yet.
    The healthcheck in Compose handles most of this, but this is a safety net.
    Like wrapping mongoose.connect() in a retry loop with backoff.
    """
    for attempt in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Database tables created successfully")
            return
        except OperationalError as e:
            logger.warning(f"⏳ DB not ready (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("❌ Could not connect to the database after multiple retries")

app = FastAPI(
    title="Todo API",
    description="A CRUD Todo API built with FastAPI + PostgreSQL",
    version="1.0.0"
)

create_tables_with_retry()

app.include_router(todo_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Todo API is running"}