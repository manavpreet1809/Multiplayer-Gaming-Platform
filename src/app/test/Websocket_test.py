import pytest
import asyncio
import os
import sys
from unittest.mock import AsyncMock

# Add the parent directory to the path to import ConnectionManager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.db.ConnectionManager import ConnectionManager

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