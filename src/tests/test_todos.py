import json
import pytest
from app.api import crud


def test_create_todo(test_app, monkeypatch):
    test_request_payload = {"title": "something", "description": "something else"}
    test_response_payload = {"id": 1, "title": "something", "description": "something else"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/todos/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_todo_invalid_json(test_app):
    response = test_app.post("/todos/", data=json.dumps({"title": "something"}))
    assert response.status_code == 422

    response = test_app.post("/todos/", data=json.dumps({"title": "1", "description": "2"}))
    assert response.status_code == 422


def test_read_todo(test_app, monkeypatch):
    test_data = {"id": 1, "title": "something", "description": "something else"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_todo_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo Not Found"

    response = test_app.get("/todos/0")
    assert response.status_code == 422


def test_read_all_todos(test_app, monkeypatch):
    test_data = [
        {"title": "something", "description": "something else", "id": 1},
        {"title": "someone", "description": "someone else", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/todos/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_todo(test_app, monkeypatch):
    test_update_data = {"title": "someone", "description": "someone else", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/todos/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)

def test_update_todo_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/todos/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_todo(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/todos/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_todo_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/todos/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo Not Found"

    response = test_app.delete("/todos/0/")
    assert response.status_code == 422