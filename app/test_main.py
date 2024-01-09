from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .main import app
from .sql_app import models
from .sql_app.dependencies import get_db

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

models.Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    yield db
    db.close()


app.dependency_overrides[get_db] = override_get_db


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_get_alerts():
    response = client.get("/alert/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_user():
    response = client.post(
        "/users",
        headers={"Content-Type": "application/json"},
        json={
            "first_name": "Gonzalo",
            "last_name": "Falfán",
            "username": "Gonzalo",
            "email": "go@gmail.com",
            "password": "1234"
        }
    )
    assert response.status_code == 200
