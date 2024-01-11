from src.tests.test_main import client


def test_read_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_category():
    response = client.post(
        "/category/",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Caminar"
        }
    )
    assert response.status_code == 200
    assert response.json().get("name") == "Caminar"
    category = client.get("/category/1")
    assert category.json().get("name") == "Caminar"


def test_read_category():
    response = client.get("/category/1")
    assert response.status_code == 200
    category = client.get("/category/1")
    assert category.json().get("name") == "Caminar"


def test_update_category():
    response = client.put(
        "/category/1",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Caminar"
        }
    )
    assert response.status_code == 200
    category = client.get("/category/1")
    assert category.json().get("name") == "Caminar"


def test_read_categories_by_max():
    response = client.get("/categories/")
    assert response.status_code == 200
    list_categories = response.json()
    assert len(list_categories) == 1


def test_delete_category():
    response = client.delete("/category/1")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Category deleted successfully"
    }
    category = client.get("/category/1")
    assert category.status_code == 404
