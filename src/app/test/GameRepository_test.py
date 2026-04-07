import asyncio
import os
import sys
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/db")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/models")))

import GamesRepository as games_repo_module


@pytest.fixture
def fake_collection(monkeypatch):
	collection = SimpleNamespace(
		insert_one=AsyncMock(),
		find_one=AsyncMock(),
		update_one=AsyncMock(),
	)
	monkeypatch.setattr(games_repo_module, "games_collection", collection)
	return collection


def test_create_game_inserts_document_and_returns_game_id(fake_collection):
	game = SimpleNamespace(game_id="g-123", to_dict=lambda: {"_id": "g-123", "lobby_code": "ABCD"})

	result = asyncio.run(games_repo_module.GameRepository.createGame(game))

	assert result == "g-123"
	fake_collection.insert_one.assert_awaited_once()
	inserted_doc = fake_collection.insert_one.await_args.args[0]
	assert inserted_doc["_id"] == "g-123"
	assert inserted_doc["lobby_code"] == "ABCD"
	assert isinstance(inserted_doc["createdAt"], datetime)


def test_get_game_returns_none_when_not_found(fake_collection):
	fake_collection.find_one.return_value = None

	game = asyncio.run(games_repo_module.GameRepository.getGame("missing"))

	assert game is None
	fake_collection.find_one.assert_awaited_once_with({"_id": "missing"})


def test_get_game_maps_document_to_game_instance(fake_collection, monkeypatch):
	class FakeGame:
		def __init__(self, game_id, lobby_code, visibility, status, host_id):
			self.game_id = game_id
			self.lobby_code = lobby_code
			self.visibility = visibility
			self.status = status
			self.host_id = host_id
			self.player_ids = None
			self.active_player_id = None
			self.state = None
			self.move_history = None

	class FakeGameState:
		@staticmethod
		def from_dict(data):
			return {"state_loaded": data}

	monkeypatch.setattr(games_repo_module, "Game", FakeGame)
	monkeypatch.setattr(games_repo_module, "GameState", FakeGameState)

	fake_collection.find_one.return_value = {
		"_id": "g-1",
		"lobby_code": "ABCD",
		"visibility": "PUBLIC",
		"status": "WAITING",
		"host_id": "host-1",
		"player_ids": ["p1", "p2"],
		"active_player_id": "p1",
		"current_state": {"board": []},
		"move_history": [{"move": 1}],
	}

	game = asyncio.run(games_repo_module.GameRepository.getGame("g-1"))

	assert game.game_id == "g-1"
	assert game.lobby_code == "ABCD"
	assert game.player_ids == ["p1", "p2"]
	assert game.active_player_id == "p1"
	assert game.state == {"state_loaded": {"board": []}}
	assert game.move_history == [{"move": 1}]


def test_get_game_uses_defaults_for_missing_optional_fields(fake_collection, monkeypatch):
	class FakeGame:
		def __init__(self, game_id, lobby_code, visibility, status, host_id):
			self.game_id = game_id
			self.lobby_code = lobby_code
			self.visibility = visibility
			self.status = status
			self.host_id = host_id

	class FakeGameState:
		@staticmethod
		def from_dict(data):
			return {"loaded": data}

	monkeypatch.setattr(games_repo_module, "Game", FakeGame)
	monkeypatch.setattr(games_repo_module, "GameState", FakeGameState)

	fake_collection.find_one.return_value = {
		"_id": "g-2",
		"lobby_code": "WXYZ",
		"visibility": "PRIVATE",
		"status": "IN_PROGRESS",
		"host_id": "host-2",
	}

	game = asyncio.run(games_repo_module.GameRepository.getGame("g-2"))

	assert game.player_ids == []
	assert game.active_player_id is None
	assert game.state == {"loaded": None}
	assert game.move_history == []


def test_update_player_membership_calls_update_with_expected_payload(fake_collection):
	asyncio.run(games_repo_module.GameRepository.updatePlayerMembership("g-3", ["p1", "p2"]))

	fake_collection.update_one.assert_awaited_once()
	query, update_doc = fake_collection.update_one.await_args.args
	assert query == {"_id": "g-3"}
	assert update_doc["$set"]["player_ids"] == ["p1", "p2"]
	assert isinstance(update_doc["$set"]["updated_at"], datetime)


def test_update_game_state_calls_update_with_state_and_move_entry(fake_collection):
	new_state = {"board": [["X"]]}
	move_entry = {"player_id": "p1", "action": "make_move"}

	asyncio.run(games_repo_module.GameRepository.updateGameState("g-4", new_state, move_entry))

	fake_collection.update_one.assert_awaited_once()
	query, update_doc = fake_collection.update_one.await_args.args
	assert query == {"_id": "g-4"}
	assert update_doc["$set"]["current_state"] == new_state
	assert isinstance(update_doc["$set"]["updated_at"], datetime)
	assert update_doc["$push"]["move_history"] == move_entry


def test_create_game_propagates_insert_errors(fake_collection):
	fake_collection.insert_one.side_effect = RuntimeError("db write failed")
	game = SimpleNamespace(game_id="g-err", to_dict=lambda: {"_id": "g-err"})

	with pytest.raises(RuntimeError, match="db write failed"):
		asyncio.run(games_repo_module.GameRepository.createGame(game))
