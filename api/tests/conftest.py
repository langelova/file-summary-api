import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.db_config import Base, get_db
from api.main import app
from api.models import FileMetadata


def populate_test_database(session):
    """
    Populates the test database with initial data.
    """
    file1 = FileMetadata(
        name="file1.txt",
        path="uploaded_files/file1.txt",
        format="txt",
        size=10,
        summary="Short summary 1",
    )
    file2 = FileMetadata(
        name="file2.txt",
        path="uploaded_files/file2.txt",
        format="txt",
        size=20,
        summary="Short summary 2",
    )
    file3 = FileMetadata(
        name="file3.txt",
        path="uploaded_files/file3.txt",
        format="txt",
        size=30,
        summary="Short summary 3",
    )
    session.add_all([file1, file2, file3])
    session.commit()


# Create an SQLite in-memory database for tests
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        populate_test_database(db)
        yield db
    finally:
        db.close()


# Override the dependency in the app
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
