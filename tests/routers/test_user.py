from tests.test_main import client


def test_read_users():
    response = client.get("/users")
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


def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200


def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
