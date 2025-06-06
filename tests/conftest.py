from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from app.auth import create_access_token
from app.database import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rivvaste30061205@localhost:5432/test_library_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def db(setup_database):
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        return db

    from app.routers.book import get_db as books_get_db
    from app.routers.readers import get_db as readers_get_db
    from app.routers.borrowed_book import get_db as borrow_get_db

    app.dependency_overrides[books_get_db] = override_get_db
    app.dependency_overrides[readers_get_db] = override_get_db
    app.dependency_overrides[borrow_get_db] = override_get_db

    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def authenticated_client(client, db: Session):
    from app.crud.user import create_user
    from app.schemas.user import UserCreate

    user_data = UserCreate(email="testuser@example.com", password="password")
    user = create_user(db, user_data)

    # Генерируем токен
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )

    client.headers = {"Authorization": f"Bearer {access_token}"}
    return client