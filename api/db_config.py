from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.settings import settings

# # Use SQLite in-memory for tests, otherwise PostgreSQL
# DATABASE_URL = (
#     "sqlite://"
#     if settings.ENV == "test"
#     else f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# )

# Use SQLite in-memory for tests, otherwise PostgreSQL
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# # Database engine
# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
# )

# Database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()