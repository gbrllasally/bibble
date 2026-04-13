from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_multiple_verses_and_prayer() -> None:
    payload = {
        "user_id": "u1",
        "message": "Aku cemas dan takut dengan masa depanku dan pekerjaan.",
        "include_long_passages": True,
    }
def test_chat_returns_recommendations() -> None:
    payload = {"user_id": "u1", "message": "Aku cemas dan takut dengan masa depanku."}
    response = client.post("/chat", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "reflection" in body
    assert "closing_prayer" in body
    assert len(body["recommended_verses"]) >= 2
    assert len(body["recommended_verses"]) >= 1
    assert len(body["reading_plan"]) >= 2


def test_home_page_renders() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Reset" in response.text
    assert "Alkitab Teman Hati" in response.text
