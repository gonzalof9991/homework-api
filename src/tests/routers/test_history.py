from src.tests.test_main import client


def test_read_histories():
    response = client.get("/histories/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_history():
    response = client.post(
        "/history/1",
        headers={"Content-Type": "application/json"},
        json={
            "title": "Test",

        }
    )
    assert response.status_code == 200
    assert response.json().get("title") == "Test"


def test_read_history():
    response = client.get("/history/1")
    assert response.status_code == 200


def test_update_history():
    response = client.put(
        "/history/1",
        headers={"Content-Type": "application/json"},
        json={
            "title": "Test v2",
            "owner_id": 1,
            "tasks": [2, 3]
        }
    )
    assert response.status_code == 200


def test_delete_history():
    response = client.delete("/history/1")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "History deleted successfully"
    }
