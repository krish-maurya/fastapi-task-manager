from fastapi.testclient import TestClient


def test_register_and_login(client: TestClient):
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": "user1@example.com", "password": "Password123", "role": "user"},
    )
    assert register_response.status_code == 201
    assert register_response.json()["email"] == "user1@example.com"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "user1@example.com", "password": "Password123"},
    )
    assert login_response.status_code == 200
    body = login_response.json()
    assert "access_token" in body
    assert "refresh_token" in body


def test_refresh_token(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={"email": "user2@example.com", "password": "Password123", "role": "user"},
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "user2@example.com", "password": "Password123"},
    )

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": login_response.json()["refresh_token"]},
    )
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()
