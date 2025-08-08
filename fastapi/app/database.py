import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Get DB URL from env or fallback
DB_URL = os.getenv("DATABASE_URL", "postgresql://veesion:secret@localhost:5432")

# Create engine
engine = create_engine(DB_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()
