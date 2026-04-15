from fastapi.testclient import TestClient

from tests.conftest import register_and_login


def test_user_task_crud_without_delete(client: TestClient):
    tokens = register_and_login(client, "taskuser@example.com", "Password123", role="user")
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Task 1", "description": "Sample"},
        headers=headers,
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    list_response = client.get("/api/v1/tasks", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Task 1 updated", "description": "Updated"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Task 1 updated"

    delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 403


def test_admin_can_delete_task(client: TestClient):
    admin_tokens = register_and_login(client, "admin@example.com", "Password123", role="admin")
    user_tokens = register_and_login(client, "anotheruser@example.com", "Password123", role="user")

    user_headers = {"Authorization": f"Bearer {user_tokens['access_token']}"}
    admin_headers = {"Authorization": f"Bearer {admin_tokens['access_token']}"}

    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Delete me", "description": "To be deleted"},
        headers=user_headers,
    )
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=admin_headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully"
