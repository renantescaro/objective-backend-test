from fastapi.testclient import TestClient

from app.main.main import app

client = TestClient(app)

# TODO: mock database


def test_get_account_without_id():
    response = client.get("/conta")
    assert response.status_code == 422


def test_create_account_without_json():
    response = client.post(
        "/conta",
        headers={},
        json={},
    )
    assert response.status_code == 422


def test_create_account_without_params():
    response = client.post(
        "/conta",
        headers={},
        json={},
    )
    assert response.status_code == 422
