from fastapi.testclient import TestClient

from app.main import app


def test_cors_preflight_allows_localhost_origin():
    with TestClient(app) as client:
        response = client.options(
            "/auth/login",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_cors_preflight_allows_loopback_origin_with_port():
    with TestClient(app) as client:
        response = client.options(
            "/games/create",
            headers={
                "Origin": "http://127.0.0.1:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "authorization,content-type",
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"


def test_cors_preflight_rejects_untrusted_origin():
    with TestClient(app) as client:
        response = client.options(
            "/auth/login",
            headers={
                "Origin": "https://evil.example",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
