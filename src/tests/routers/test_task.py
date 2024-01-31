from src.tests.test_main import client


def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    response = client.post(
        "/histories/1/tasks/",
        headers={"Content-Type": "application/json"},
        json={
            "title": "Caminar v5",
            "minutes_expected": 20,
            "categories": [
                1
            ],
            "alert_id": 1,
            "expiration_date": "2024-01-06"
        }
    )
    assert response.status_code == 200
    assert response.json().get("title") == "Caminar v5"
    assert response.json().get("minutes_expected") == 20
    assert response.json().get("alert_id") == 1
    assert response.json().get("expiration_date") == "2024-01-06"


def test_read_task():
    response = client.get("/task/1")
    assert response.status_code == 200


def test_update_task():
    response = client.put(
        "/task/1",
        headers={"Content-Type": "application/json"},
        json={
            "title": "Caminar v5",
            "minutes_expected": 20,
            "categories": [
                1
            ],
            "alert_id": 1,
            "expiration_date": "2024-01-06"
        }
    )
    assert response.status_code == 200


def test_delete_task():
    response = client.delete("/task/1")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Task deleted successfully"
    }
