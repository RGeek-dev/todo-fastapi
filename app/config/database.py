# app/config/database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # Reads your .env file into os.environ

DATABASE_URL = os.getenv("DATABASE_URL")

# The engine is your connection pool manager.
# It holds persistent connections to Postgres and hands them out on demand.
# This does NOT open a connection immediately — it's lazy.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory that produces individual DB sessions.
# One session = one unit of work (like a transaction scope).
# autocommit=False means you control when changes are written to disk.
# autoflush=False means SQLAlchemy won't emit SQL until you explicitly flush/commit.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the class all your ORM models will inherit from.
# It maintains a registry of all models — SQLAlchemy uses this
# to know which tables exist when you call create_all().
Base = declarative_base()