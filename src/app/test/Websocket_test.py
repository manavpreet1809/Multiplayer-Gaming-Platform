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


