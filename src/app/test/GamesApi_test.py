import random
import string

from fastapi.testclient import TestClient

from app.main import app


def _random_suffix(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def _auth_headers(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}


def _register_and_login(client: TestClient, prefix: str = "user", password: str = "MyPassword1!"):
    username = f"{prefix}_{_random_suffix()}"
    email = f"{username}@example.com"

    reg_res = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "email": email,
        },
    )
    assert reg_res.status_code == 201, reg_res.text

    login_res = client.post(
        "/auth/login",
        data={"username": username, "password": password},
    )
    assert login_res.status_code == 200, login_res.text

    tokens = login_res.json()
    return username, tokens["access_token"], tokens["refresh_token"]


def _create_game(client: TestClient, access_token: str, game_type: str = "chess", visibility: str = "public") -> dict:
    res = client.post(
        "/games/create",
        headers=_auth_headers(access_token),
        json={"game_type": game_type, "visibility": visibility},
    )
    assert res.status_code == 200, res.text
    return res.json()


def test_create_game_requires_auth():
    with TestClient(app) as client:
        response = client.post(
            "/games/create",
            json={"game_type": "chess", "visibility": "public"},
        )

    assert response.status_code == 401


def test_create_game_invalid_type_returns_400():
    with TestClient(app) as client:
        _, access_token, _ = _register_and_login(client)

        response = client.post(
            "/games/create",
            headers=_auth_headers(access_token),
            json={"game_type": "checkers", "visibility": "public"},
        )

    assert response.status_code == 400
    assert "game_type" in response.json()["detail"]


def test_create_game_success_returns_summary():
    with TestClient(app) as client:
        username, access_token, _ = _register_and_login(client)

        data = _create_game(client, access_token, game_type="chess", visibility="public")

    assert data["host_id"] == username
    assert data["game_type"] == "chess"
    assert data["player_count"] == 1
    assert data["max_players"] == 2
    assert data["player_ids"] == [username]
    assert isinstance(data["game_id"], str)
    assert isinstance(data["lobby_code"], str)


def test_list_games_hides_private_lobbies_from_non_host():
    with TestClient(app) as client:
        host, host_token, _ = _register_and_login(client, prefix="host")
        _, other_token, _ = _register_and_login(client, prefix="other")

        private_game = _create_game(client, host_token, game_type="chess", visibility="private")

        other_list = client.get("/games", headers=_auth_headers(other_token))
        host_list = client.get("/games", headers=_auth_headers(host_token))

    assert other_list.status_code == 200
    assert host_list.status_code == 200

    other_ids = {g["game_id"] for g in other_list.json()}
    host_ids = {g["game_id"] for g in host_list.json()}

    assert private_game["game_id"] not in other_ids
    assert private_game["game_id"] in host_ids
    assert host == private_game["host_id"]


def test_list_games_excludes_in_progress_lobbies():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        _, p2_token, _ = _register_and_login(client, prefix="p2")

        created = _create_game(client, host_token, game_type="chess", visibility="public")
        game_id = created["game_id"]

        join_res = client.post(f"/games/{game_id}/join", headers=_auth_headers(p2_token))
        assert join_res.status_code == 200, join_res.text

        start_res = client.post(f"/games/{game_id}/start", headers=_auth_headers(host_token))
        assert start_res.status_code == 200, start_res.text

        list_res = client.get("/games", headers=_auth_headers(host_token))

    assert list_res.status_code == 200
    listed_ids = {g["game_id"] for g in list_res.json()}
    assert game_id not in listed_ids


def test_list_games_applies_game_type_filter():
    with TestClient(app) as client:
        _, token, _ = _register_and_login(client)

        chess_game = _create_game(client, token, game_type="chess")
        _create_game(client, token, game_type="tictactoe")

        chess_only = client.get("/games", headers=_auth_headers(token), params={"game_type": "chess"})

    assert chess_only.status_code == 200
    payload = chess_only.json()
    assert payload
    assert all(g["game_type"] == "chess" for g in payload)
    assert chess_game["game_id"] in {g["game_id"] for g in payload}


def test_join_by_code_returns_404_for_unknown_code():
    with TestClient(app) as client:
        _, token, _ = _register_and_login(client)

        res = client.post(
            "/games/join/code",
            headers=_auth_headers(token),
            json={"lobby_code": "ZZZZ"},
        )

    assert res.status_code == 404
    assert res.json()["detail"] == "Lobby not found"


def test_join_by_code_is_case_insensitive():
    with TestClient(app) as client:
        host, host_token, _ = _register_and_login(client, prefix="host")
        joiner, joiner_token, _ = _register_and_login(client, prefix="joiner")

        created = _create_game(client, host_token, game_type="chess")

        join_res = client.post(
            "/games/join/code",
            headers=_auth_headers(joiner_token),
            json={"lobby_code": created["lobby_code"].lower()},
        )

    assert join_res.status_code == 200
    data = join_res.json()
    assert data["game_id"] == created["game_id"]
    assert set(data["player_ids"]) == {host, joiner}


def test_join_by_code_duplicate_request_returns_409_when_lobby_is_full():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        joiner, joiner_token, _ = _register_and_login(client, prefix="joiner")

        created = _create_game(client, host_token, game_type="chess")

        first_join = client.post(
            "/games/join/code",
            headers=_auth_headers(joiner_token),
            json={"lobby_code": created["lobby_code"]},
        )
        second_join = client.post(
            "/games/join/code",
            headers=_auth_headers(joiner_token),
            json={"lobby_code": created["lobby_code"]},
        )

    assert first_join.status_code == 200
    assert second_join.status_code == 409
    assert second_join.json()["detail"] == "Lobby is full"


def test_join_by_code_returns_409_when_lobby_is_full():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        _, p2_token, _ = _register_and_login(client, prefix="p2")
        _, p3_token, _ = _register_and_login(client, prefix="p3")

        created = _create_game(client, host_token, game_type="chess")

        first_join = client.post(
            "/games/join/code",
            headers=_auth_headers(p2_token),
            json={"lobby_code": created["lobby_code"]},
        )
        assert first_join.status_code == 200, first_join.text

        full_join = client.post(
            "/games/join/code",
            headers=_auth_headers(p3_token),
            json={"lobby_code": created["lobby_code"]},
        )

    assert full_join.status_code == 409
    assert full_join.json()["detail"] == "Lobby is full"


def test_join_by_code_returns_409_when_game_started():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        _, p2_token, _ = _register_and_login(client, prefix="p2")
        _, p3_token, _ = _register_and_login(client, prefix="p3")

        created = _create_game(client, host_token, game_type="chess")
        game_id = created["game_id"]

        join_res = client.post(f"/games/{game_id}/join", headers=_auth_headers(p2_token))
        assert join_res.status_code == 200, join_res.text

        start_res = client.post(f"/games/{game_id}/start", headers=_auth_headers(host_token))
        assert start_res.status_code == 200, start_res.text

        late_join = client.post(
            "/games/join/code",
            headers=_auth_headers(p3_token),
            json={"lobby_code": created["lobby_code"]},
        )

    assert late_join.status_code == 409
    assert late_join.json()["detail"] == "Game already started"


def test_matchmake_rejects_invalid_game_type():
    with TestClient(app) as client:
        _, token, _ = _register_and_login(client)

        response = client.post(
            "/games/matchmake",
            headers=_auth_headers(token),
            json={"game_type": "checkers"},
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid game type"


def test_matchmake_joins_existing_public_lobby_or_creates_if_missing():
    with TestClient(app) as client:
        p1, p1_token, _ = _register_and_login(client, prefix="p1")
        p2, p2_token, _ = _register_and_login(client, prefix="p2")

        first = client.post(
            "/games/matchmake",
            headers=_auth_headers(p1_token),
            json={"game_type": "chess"},
        )
        assert first.status_code == 200, first.text

        second = client.post(
            "/games/matchmake",
            headers=_auth_headers(p2_token),
            json={"game_type": "chess"},
        )

    assert second.status_code == 200
    first_data = first.json()
    second_data = second.json()
    assert second_data["game_id"] == first_data["game_id"]
    assert second_data["player_count"] == 2
    assert set(second_data["player_ids"]) == {p1, p2}


def test_get_game_returns_404_for_missing_id():
    with TestClient(app) as client:
        _, token, _ = _register_and_login(client)

        response = client.get("/games/missing-game-id", headers=_auth_headers(token))

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_join_game_returns_404_for_missing_id():
    with TestClient(app) as client:
        _, token, _ = _register_and_login(client)

        response = client.post("/games/missing-game-id/join", headers=_auth_headers(token))

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_join_game_duplicate_request_returns_409_when_lobby_is_full():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        p2, p2_token, _ = _register_and_login(client, prefix="p2")

        created = _create_game(client, host_token, game_type="chess")
        game_id = created["game_id"]

        first_join = client.post(f"/games/{game_id}/join", headers=_auth_headers(p2_token))
        second_join = client.post(f"/games/{game_id}/join", headers=_auth_headers(p2_token))

    assert first_join.status_code == 200
    assert second_join.status_code == 409
    assert second_join.json()["detail"] == "Lobby is full"


def test_start_game_blocks_non_host():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        _, p2_token, _ = _register_and_login(client, prefix="p2")

        created = _create_game(client, host_token, game_type="chess")
        game_id = created["game_id"]

        join_res = client.post(f"/games/{game_id}/join", headers=_auth_headers(p2_token))
        assert join_res.status_code == 200, join_res.text

        response = client.post(f"/games/{game_id}/start", headers=_auth_headers(p2_token))

    assert response.status_code == 403
    assert response.json()["detail"] == "Only the host can start the game"


def test_start_game_requires_enough_players():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")

        created = _create_game(client, host_token, game_type="chess")

        response = client.post(f"/games/{created['game_id']}/start", headers=_auth_headers(host_token))

    assert response.status_code == 409
    assert response.json()["detail"] == "Not enough players to start"


def test_start_game_success_and_second_start_conflicts():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        _, p2_token, _ = _register_and_login(client, prefix="p2")

        created = _create_game(client, host_token, game_type="chess")
        game_id = created["game_id"]

        join_res = client.post(f"/games/{game_id}/join", headers=_auth_headers(p2_token))
        assert join_res.status_code == 200, join_res.text

        start_res = client.post(f"/games/{game_id}/start", headers=_auth_headers(host_token))
        second_start = client.post(f"/games/{game_id}/start", headers=_auth_headers(host_token))

    assert start_res.status_code == 200
    payload = start_res.json()
    assert payload["status"] == 1
    assert "state" in payload

    assert second_start.status_code == 409
    assert second_start.json()["detail"] == "Game not in waiting state"


def test_leave_game_returns_404_for_missing_id():
    with TestClient(app) as client:
        _, token, _ = _register_and_login(client)

        response = client.post("/games/missing-game-id/leave", headers=_auth_headers(token))

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_leave_game_transfers_host_if_host_leaves_waiting_lobby():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        p2, p2_token, _ = _register_and_login(client, prefix="p2")

        created = _create_game(client, host_token, game_type="chess")
        game_id = created["game_id"]

        join_res = client.post(f"/games/{game_id}/join", headers=_auth_headers(p2_token))
        assert join_res.status_code == 200, join_res.text

        leave_res = client.post(f"/games/{game_id}/leave", headers=_auth_headers(host_token))
        assert leave_res.status_code == 200, leave_res.text

        game_res = client.get(f"/games/{game_id}", headers=_auth_headers(p2_token))

    assert game_res.status_code == 200
    game_data = game_res.json()
    assert game_data["host_id"] == p2
    assert game_data["player_count"] == 1


def test_leave_game_deletes_lobby_when_last_player_leaves():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")

        created = _create_game(client, host_token, game_type="chess")
        game_id = created["game_id"]

        leave_res = client.post(f"/games/{game_id}/leave", headers=_auth_headers(host_token))
        assert leave_res.status_code == 200, leave_res.text

        get_res = client.get(f"/games/{game_id}", headers=_auth_headers(host_token))

    assert get_res.status_code == 404


def test_leave_game_marks_in_progress_game_as_finished():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        _, p2_token, _ = _register_and_login(client, prefix="p2")

        created = _create_game(client, host_token, game_type="chess")
        game_id = created["game_id"]

        join_res = client.post(f"/games/{game_id}/join", headers=_auth_headers(p2_token))
        assert join_res.status_code == 200, join_res.text

        start_res = client.post(f"/games/{game_id}/start", headers=_auth_headers(host_token))
        assert start_res.status_code == 200, start_res.text

        leave_res = client.post(f"/games/{game_id}/leave", headers=_auth_headers(p2_token))
        assert leave_res.status_code == 200, leave_res.text

        game_res = client.get(f"/games/{game_id}", headers=_auth_headers(host_token))

    assert game_res.status_code == 200
    assert game_res.json()["status"] == 2
