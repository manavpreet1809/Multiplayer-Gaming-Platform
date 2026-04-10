import random
import string

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.main import app
from app.api import games as games_api


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


def _create_game(client: TestClient, access_token: str, game_type: str = "chess") -> dict:
    create_res = client.post(
        "/games/create",
        headers=_auth_headers(access_token),
        json={"game_type": game_type, "visibility": "public"},
    )
    assert create_res.status_code == 200, create_res.text
    return create_res.json()


def _create_started_game(client: TestClient):
    host, host_token, _ = _register_and_login(client, prefix="host")
    p2, p2_token, _ = _register_and_login(client, prefix="p2")

    created = _create_game(client, host_token, game_type="chess")
    game_id = created["game_id"]

    join_res = client.post(f"/games/{game_id}/join", headers=_auth_headers(p2_token))
    assert join_res.status_code == 200, join_res.text

    start_res = client.post(f"/games/{game_id}/start", headers=_auth_headers(host_token))
    assert start_res.status_code == 200, start_res.text

    return host, host_token, p2, p2_token, game_id


def _expect_closed_with_code(ws, code: int):
    with pytest.raises(WebSocketDisconnect) as exc_info:
        ws.receive_json()
    assert exc_info.value.code == code


def test_game_ws_requires_token():
    with TestClient(app) as client:
        with client.websocket_connect("/games/ws/any-game") as ws:
            _expect_closed_with_code(ws, 4001)


def test_game_ws_rejects_invalid_token():
    with TestClient(app) as client:
        with client.websocket_connect("/games/ws/any-game?token=not-a-valid-jwt") as ws:
            _expect_closed_with_code(ws, 4001)


def test_game_ws_returns_4004_when_game_not_found():
    with TestClient(app) as client:
        _, token, _ = _register_and_login(client)

        with client.websocket_connect(f"/games/ws/missing-game?token={token}") as ws:
            _expect_closed_with_code(ws, 4004)


def test_game_ws_waiting_game_sends_lobby_payload():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        created = _create_game(client, host_token, game_type="chess")

        with client.websocket_connect(f"/games/ws/{created['game_id']}?token={host_token}") as ws:
            first = ws.receive_json()

    assert first["type"] == "lobby"
    assert first["data"]["game_id"] == created["game_id"]


def test_game_ws_started_game_sends_state_payload():
    with TestClient(app) as client:
        _, host_token, _, _, game_id = _create_started_game(client)

        with client.websocket_connect(f"/games/ws/{game_id}?token={host_token}") as ws:
            first = ws.receive_json()

    assert first["type"] == "state"
    assert "state" in first


def test_game_ws_rejects_move_when_game_not_in_progress():
    with TestClient(app) as client:
        _, host_token, _ = _register_and_login(client, prefix="host")
        created = _create_game(client, host_token, game_type="chess")

        with client.websocket_connect(f"/games/ws/{created['game_id']}?token={host_token}") as ws:
            _ = ws.receive_json()  # initial lobby payload
            ws.send_json({"type": "move", "move": {"index": 0}})
            err = ws.receive_json()

    assert err == {"type": "error", "error": "Game not in progress"}


def test_game_ws_rejects_move_when_not_your_turn():
    with TestClient(app) as client:
        _, _, _, p2_token, game_id = _create_started_game(client)

        with client.websocket_connect(f"/games/ws/{game_id}?token={p2_token}") as ws:
            _ = ws.receive_json()  # initial state payload
            ws.send_json({"type": "move", "move": {"index": 0}})
            err = ws.receive_json()

    assert err == {"type": "error", "error": "Not your turn"}


def test_game_ws_rejects_invalid_move_format_for_active_player():
    with TestClient(app) as client:
        _, host_token, _, _, game_id = _create_started_game(client)

        with client.websocket_connect(f"/games/ws/{game_id}?token={host_token}") as ws:
            _ = ws.receive_json()  # initial state payload
            ws.send_json({"type": "move", "move": {"bad": "shape"}})
            err = ws.receive_json()

    assert err["type"] == "error"
    assert "Invalid move format" in err["error"]


def test_game_ws_chat_broadcasts_to_room_and_trims_whitespace():
    with TestClient(app) as client:
        host, host_token, _ = _register_and_login(client, prefix="host")
        _, p2_token, _ = _register_and_login(client, prefix="p2")
        created = _create_game(client, host_token, game_type="chess")

        join_res = client.post(f"/games/{created['game_id']}/join", headers=_auth_headers(p2_token))
        assert join_res.status_code == 200, join_res.text

        with client.websocket_connect(f"/games/ws/{created['game_id']}?token={host_token}") as ws1:
            with client.websocket_connect(f"/games/ws/{created['game_id']}?token={p2_token}") as ws2:
                _ = ws1.receive_json()
                _ = ws2.receive_json()

                ws1.send_json({"type": "chat", "text": "   hello room   "})
                msg1 = ws1.receive_json()
                msg2 = ws2.receive_json()

    expected = {"type": "chat", "sender": host, "text": "hello room"}
    assert msg1 == expected
    assert msg2 == expected


def test_game_ws_disconnect_broadcasts_player_disconnected():
    with TestClient(app) as client:
        host, host_token, _ = _register_and_login(client, prefix="host")
        _, p2_token, _ = _register_and_login(client, prefix="p2")
        created = _create_game(client, host_token, game_type="chess")

        join_res = client.post(f"/games/{created['game_id']}/join", headers=_auth_headers(p2_token))
        assert join_res.status_code == 200, join_res.text

        with client.websocket_connect(f"/games/ws/{created['game_id']}?token={host_token}") as ws1:
            with client.websocket_connect(f"/games/ws/{created['game_id']}?token={p2_token}") as ws2:
                _ = ws1.receive_json()
                _ = ws2.receive_json()

                ws1.close()
                msg = ws2.receive_json()

    assert msg == {"type": "player_disconnected", "player_id": host}


def test_global_chat_ws_requires_token():
    with TestClient(app) as client:
        with client.websocket_connect("/games/chat/global") as ws:
            _expect_closed_with_code(ws, 4001)


def test_global_chat_ws_sends_history_and_broadcasts_messages():
    with TestClient(app) as client:
        u1, t1, _ = _register_and_login(client, prefix="u1")
        _, t2, _ = _register_and_login(client, prefix="u2")

        games_api._global_chat[:] = [
            {"type": "chat", "sender": "seed", "text": f"seed-{i}"}
            for i in range(60)
        ]

        with client.websocket_connect(f"/games/chat/global?token={t1}") as ws1:
            history = ws1.receive_json()
            assert history["type"] == "history"
            assert len(history["messages"]) == 50
            assert history["messages"][0]["text"] == "seed-10"
            assert history["messages"][-1]["text"] == "seed-59"

            with client.websocket_connect(f"/games/chat/global?token={t2}") as ws2:
                history2 = ws2.receive_json()
                assert history2["type"] == "history"

                ws1.send_json({"type": "chat", "text": "   hi all   "})
                m1 = ws1.receive_json()
                m2 = ws2.receive_json()

    expected = {"type": "chat", "sender": u1, "text": "hi all"}
    assert m1 == expected
    assert m2 == expected


def test_global_chat_ws_caps_history_to_200_messages():
    with TestClient(app) as client:
        _, token, _ = _register_and_login(client, prefix="seed")

        games_api._global_chat[:] = [
            {"type": "chat", "sender": "seed", "text": f"seed-{i}"}
            for i in range(200)
        ]

        with client.websocket_connect(f"/games/chat/global?token={token}") as ws:
            _ = ws.receive_json()  # history
            ws.send_json({"type": "chat", "text": "new-message"})
            msg = ws.receive_json()

    assert msg["type"] == "chat"
    assert len(games_api._global_chat) == 200
    assert games_api._global_chat[0]["text"] == "seed-1"
    assert games_api._global_chat[-1]["text"] == "new-message"
