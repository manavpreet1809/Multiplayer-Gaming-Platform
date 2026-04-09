import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.games import store as games_store


@pytest.fixture(autouse=True)
def clear_games_between_tests():
    games_store.reset_runtime_state()
    yield
    games_store.reset_runtime_state()


def random_string(length=10):
    import random
    import string

    return "".join(random.choices(string.ascii_letters, k=length))


def register_and_token(client, username=None, password="MyPassword1!"):
    username = username or f"user_{random_string()}"
    client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "email": f"{username}@example.com",
        },
    )
    r = client.post("/auth/login", data={"username": username, "password": password})
    assert r.status_code == 200
    return username, r.json()["access_token"]


def test_leaderboard_path_not_shadowed_by_game_id():
    """GET /games/leaderboard must hit the leaderboard handler, not /{game_id}."""
    with TestClient(app) as client:
        _, token = register_and_token(client)
        r = client.get(
            "/games/leaderboard",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        if len(data) > 0:
            row = data[0]
            assert row.get("place") == 1
            assert "tier" in row
            assert "mmr" in row


def test_get_game_forbidden_for_non_participant():
    with TestClient(app) as client:
        _, token_a = register_and_token(client)
        user_b, token_b = register_and_token(client)

        created = client.post(
            "/games/create",
            json={"game_type": "chess", "visibility": "public"},
            headers={"Authorization": f"Bearer {token_a}"},
        )
        assert created.status_code == 200
        game_id = created.json()["game_id"]

        outsider = client.get(
            f"/games/{game_id}",
            headers={"Authorization": f"Bearer {token_b}"},
        )
        assert outsider.status_code == 403

        insider = client.get(
            f"/games/{game_id}",
            headers={"Authorization": f"Bearer {token_a}"},
        )
        assert insider.status_code == 200


def test_create_and_join_game():
    with TestClient(app) as client:
        _, token_a = register_and_token(client)
        user_b, token_b = register_and_token(client)

        created = client.post(
            "/games/create",
            json={"game_type": "tictactoe", "visibility": "public"},
            headers={"Authorization": f"Bearer {token_a}"},
        )
        assert created.status_code == 200
        game_id = created.json()["game_id"]

        joined = client.post(
            f"/games/{game_id}/join",
            headers={"Authorization": f"Bearer {token_b}"},
        )
        assert joined.status_code == 200
        assert user_b in joined.json()["player_ids"]
