import pytest
import asyncio
import os
import sys
from unittest.mock import AsyncMock
from datetime import datetime as real_datetime, timezone
from fastapi.testclient import TestClient

# Add the parent directory to the path to import ConnectionManager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/models")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/db")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.db.ConnectionManager import ConnectionManager
import server as websocket_server

@pytest.fixture
def connection_manager():
    '''Fixture to provide a fresh instance of ConnectionManager for each test.'''
    return ConnectionManager()


def _mock_websocket():
    '''Helper function to create a mock websocket with async methods for testing.'''
    ws = AsyncMock()
    ws.accept = AsyncMock()
    ws.send_json = AsyncMock()
    return ws


def test_connect_accepts_and_stores_connection(connection_manager):
    '''
    Tests that when a player connects, their websocket is accepted and 
    stored in the connection manager under the correct game and player ID.
    '''

    game_id = "game1"
    player_id = "player1"
    websocket = _mock_websocket()

    asyncio.run(connection_manager.connect(game_id, player_id, websocket))

    websocket.accept.assert_awaited_once()
    assert game_id in connection_manager.active_connections
    assert connection_manager.active_connections[game_id][player_id] is websocket


def test_connect_stores_multiple_players_in_same_game(connection_manager):
    '''
    Tests that multiple players can connect to the same game and their websockets are stored correctly.
    '''
    game_id = "game1"
    ws1 = _mock_websocket()
    ws2 = _mock_websocket()

    asyncio.run(connection_manager.connect(game_id, "player1", ws1))
    asyncio.run(connection_manager.connect(game_id, "player2", ws2))

    assert set(connection_manager.active_connections[game_id].keys()) == {"player1", "player2"}

def test_disconnect_removes_only_target_player(connection_manager):
    '''
    Tests that when a player disconnects, only their websocket is removed from the connection manager, 
    and other players in the same game are unaffected.
    '''
    game_id = "game1"
    ws1 = _mock_websocket()
    ws2 = _mock_websocket()

    asyncio.run(connection_manager.connect(game_id, "player1", ws1))
    asyncio.run(connection_manager.connect(game_id, "player2", ws2))

    connection_manager.disconnect(game_id, "player1")

    assert "player1" not in connection_manager.active_connections[game_id]
    assert connection_manager.active_connections[game_id]["player2"] is ws2


def test_disconnect_removes_game_bucket_when_last_player_leaves(connection_manager):
    '''
    Tests that when the last player in a game disconnects, 
    the entire game bucket is removed from the connection manager.
    '''

    game_id = "game1"
    ws = _mock_websocket()

    asyncio.run(connection_manager.connect(game_id, "player1", ws))
    connection_manager.disconnect(game_id, "player1")

    assert game_id not in connection_manager.active_connections


def test_disconnect_missing_game_or_player_is_noop(connection_manager):
    '''
    Tests that if disconnect is called with a game ID or player ID that doesn't exist,
    it does not raise an error and does not affect existing connections.
    '''
    game_id = "game1"
    ws = _mock_websocket()

    asyncio.run(connection_manager.connect(game_id, "player1", ws))

    connection_manager.disconnect("missing-game", "player1")
    connection_manager.disconnect(game_id, "missing-player")

    assert game_id in connection_manager.active_connections
    assert "player1" in connection_manager.active_connections[game_id]

def test_broadcast_sends_to_all_players_in_game(connection_manager):
    '''
    Tests that when a message is broadcast to a game, all connected players in that game receive the message.
    '''

    game_id = "game1"
    message = {"event": "game_state_update", "payload": {"turn": 3}}
    ws1 = _mock_websocket()
    ws2 = _mock_websocket()

    asyncio.run(connection_manager.connect(game_id, "player1", ws1))
    asyncio.run(connection_manager.connect(game_id, "player2", ws2))

    asyncio.run(connection_manager.broadcast(game_id, message))

    ws1.send_json.assert_awaited_once_with(message)
    ws2.send_json.assert_awaited_once_with(message)


def test_broadcast_only_targets_requested_game(connection_manager):
    '''
    Tests that when a message is broadcast to a specific game, 
    only players in that game receive the message,
    and players in other games do not receive it.
    '''

    ws_game1 = _mock_websocket()
    ws_game2 = _mock_websocket()
    message = {"event": "ping"}

    asyncio.run(connection_manager.connect("game1", "player1", ws_game1))
    asyncio.run(connection_manager.connect("game2", "player2", ws_game2))

    asyncio.run(connection_manager.broadcast("game1", message))

    ws_game1.send_json.assert_awaited_once_with(message)
    ws_game2.send_json.assert_not_awaited()


def test_broadcast_missing_game_is_no_op(connection_manager):
    '''
    Tests that if broadcast is called with a game ID that doesn't exist, 
    it does not raise an error and does not affect existing connections.
    '''
    asyncio.run(connection_manager.broadcast("missing-game", {"event": "no_op"}))

    assert connection_manager.active_connections == {}


class _FakeState:
    def __init__(self, current_player="player1"):
        self.current_player = current_player

    def to_dict(self):
        return {"current_player": self.current_player}


class _FakeGame:
    def __init__(self, player_ids=None, current_player="player1", is_valid=True):
        self.player_ids = player_ids or ["player1", "player2"]
        self.state = _FakeState(current_player=current_player)
        self._is_valid = is_valid
        self.moves = []

    def isValid(self, _payload):
        return self._is_valid

    def move(self, payload):
        self.moves.append(payload)

    def toDict(self):
        return {
            "players": self.player_ids,
            "state": self.state.to_dict(),
            "move_count": len(self.moves),
        }


class _FakeDatetime:
    @staticmethod
    def uctnow():
        return real_datetime(2026, 1, 1, tzinfo=timezone.utc)


@pytest.fixture
def websocket_client(monkeypatch):
    websocket_server.manager.active_connections.clear()
    monkeypatch.setattr(websocket_server, "datetime", _FakeDatetime)
    with TestClient(websocket_server.app) as client:
        yield client
    websocket_server.manager.active_connections.clear()


def test_websocket_game_not_found_returns_error(websocket_client, monkeypatch):
    async def fake_get_game(_game_id):
        return None

    monkeypatch.setattr(websocket_server.GameRepository, "getGame", fake_get_game)

    with websocket_client.websocket_connect("/ws/game/game1?player_id=player1") as ws:
        ws.send_json({"event": "make_move", "payload": {"x": 1}})
        data = ws.receive_json()

    assert data == {"event": "error", "message": "Game not found"}


def test_websocket_rejects_non_participant(websocket_client, monkeypatch):
    game = _FakeGame(player_ids=["player2"], current_player="player2", is_valid=True)

    async def fake_get_game(_game_id):
        return game

    monkeypatch.setattr(websocket_server.GameRepository, "getGame", fake_get_game)

    with websocket_client.websocket_connect("/ws/game/game1?player_id=player1") as ws:
        ws.send_json({"event": "make_move", "payload": {"x": 1}})
        data = ws.receive_json()

    assert data == {"event": "move_rejected", "reason": "Not a participant"}


def test_websocket_rejects_wrong_turn(websocket_client, monkeypatch):
    game = _FakeGame(player_ids=["player1", "player2"], current_player="player2", is_valid=True)

    async def fake_get_game(_game_id):
        return game

    monkeypatch.setattr(websocket_server.GameRepository, "getGame", fake_get_game)

    with websocket_client.websocket_connect("/ws/game/game1?player_id=player1") as ws:
        ws.send_json({"event": "make_move", "payload": {"x": 1}})
        data = ws.receive_json()

    assert data == {"event": "move_rejected", "reason": "Not your turn"}


def test_websocket_rejects_invalid_move(websocket_client, monkeypatch):
    game = _FakeGame(player_ids=["player1"], current_player="player1", is_valid=False)

    async def fake_get_game(_game_id):
        return game

    monkeypatch.setattr(websocket_server.GameRepository, "getGame", fake_get_game)

    with websocket_client.websocket_connect("/ws/game/game1?player_id=player1") as ws:
        ws.send_json({"event": "make_move", "payload": {"x": 1}})
        data = ws.receive_json()

    assert data == {"event": "move_rejected", "reason": "Invalid move"}


def test_websocket_valid_move_updates_state_and_broadcasts(websocket_client, monkeypatch):
    game = _FakeGame(player_ids=["player1", "player2"], current_player="player1", is_valid=True)
    update_calls = []

    async def fake_get_game(_game_id):
        return game

    async def fake_update(game_id, new_state, move_entry):
        update_calls.append((game_id, new_state, move_entry))

    monkeypatch.setattr(websocket_server.GameRepository, "getGame", fake_get_game)
    monkeypatch.setattr(websocket_server.GameRepository, "updateGameState", fake_update)

    with websocket_client.websocket_connect("/ws/game/game1?player_id=player1") as ws1:
        with websocket_client.websocket_connect("/ws/game/game1?player_id=player2") as ws2:
            payload = {"x": 3, "y": 4}
            ws1.send_json({"event": "make_move", "payload": payload})
            msg1 = ws1.receive_json()
            msg2 = ws2.receive_json()

    assert msg1["event"] == "game_state_update"
    assert msg2["event"] == "game_state_update"
    assert update_calls
    assert update_calls[0][0] == "game1"
    assert update_calls[0][1] == {"current_player": "player1"}
    assert update_calls[0][2]["player_id"] == "player1"
    assert update_calls[0][2]["action"] == "make_move"
    assert update_calls[0][2]["payload"] == payload


def test_websocket_disconnect_broadcasts_player_disconnected(websocket_client, monkeypatch):
    game = _FakeGame(player_ids=["player1", "player2"], current_player="player1", is_valid=True)

    async def fake_get_game(_game_id):
        return game

    async def fake_update(_game_id, _new_state, _move_entry):
        return None

    monkeypatch.setattr(websocket_server.GameRepository, "getGame", fake_get_game)
    monkeypatch.setattr(websocket_server.GameRepository, "updateGameState", fake_update)

    with websocket_client.websocket_connect("/ws/game/game1?player_id=player1") as ws1:
        with websocket_client.websocket_connect("/ws/game/game1?player_id=player2") as ws2:
            ws1.close()
            data = ws2.receive_json()

    assert data == {"event": "player_disconnected", "player_id": "player1"}