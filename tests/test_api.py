from fastapi.testclient import TestClient

from backend.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


def test_commands_exist():
    with TestClient(app) as client:
        response = client.get("/api/commands")
        assert response.status_code == 200
        assert any(item["command"] == "show ip route" for item in response.json())


def test_search_ospf():
    with TestClient(app) as client:
        response = client.get("/api/search?q=ospf")
        assert response.status_code == 200
        assert response.json()
