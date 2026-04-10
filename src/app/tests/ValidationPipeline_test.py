from enum import Enum

from app.modules.validationPipeline import ValidationPipeline


class Color(Enum):
    WHITE = "white"
    BLACK = "black"


class FakeEngine:
    def __init__(self):
        self.should_validate = True
        self.new_state = None
        self.raw_result = None
        self.serialized_result = None
        self.in_check = False
        self.has_legal = True
        self.raise_on_check_eval = False

    def validateMove(self, state, move):
        return self.should_validate

    def applyMove(self, state, move):
        return self.new_state

    def evaluateEnd(self, new_state):
        return self.raw_result

    def serializeEndResult(self, raw_result, new_state):
        return self.serialized_result

    def findKing(self, board, active_color):
        if self.raise_on_check_eval:
            raise RuntimeError("boom")
        return "kpos"

    def isSquareAttacked(self, board, king_pos, opponent):
        return self.in_check

    def hasAnyLegalMove(self, state, active_color):
        return self.has_legal


def test_process_move_rejects_not_your_turn_for_active_color_state():
    engine = FakeEngine()
    pipeline = ValidationPipeline(engine)
    state = {
        "activeColor": "white",
        "players": {"white": "p1", "black": "p2"},
        "board": [],
    }

    out = pipeline.processMove(state, "p2", {"x": 1})

    assert out["success"] is False
    assert out["error"] == "not your turn"
    assert out["state"] is None
    assert out["result"] is None


def test_process_move_illegal_move_defaults_for_non_chess_state_shape():
    engine = FakeEngine()
    engine.should_validate = False
    pipeline = ValidationPipeline(engine)
    state = {"currentPlayer": "p1"}

    out = pipeline.processMove(state, "p1", {"x": 1})

    assert out["success"] is False
    assert out["error"] == "illegal move"


def test_process_move_illegal_move_reports_checkmate():
    engine = FakeEngine()
    engine.should_validate = False
    engine.in_check = True
    engine.has_legal = False
    pipeline = ValidationPipeline(engine)

    state = {
        "activeColor": "white",
        "players": {"white": "p1", "black": "p2"},
        "board": [],
    }

    out = pipeline.processMove(state, "p1", {"x": 1})

    assert out["success"] is False
    assert out["error"] == "checkmate"


def test_process_move_success_sets_check_status_when_king_attacked():
    engine = FakeEngine()
    engine.should_validate = True
    engine.new_state = {
        "activeColor": "white",
        "players": {"white": "p1", "black": "p2"},
        "board": [],
    }
    engine.raw_result = None
    engine.in_check = True
    pipeline = ValidationPipeline(engine)

    out = pipeline.processMove(
        {
            "activeColor": "white",
            "players": {"white": "p1", "black": "p2"},
            "board": [],
        },
        "p1",
        {"x": 1},
    )

    assert out["success"] is True
    assert out["error"] is None
    assert out["status"] == "check"


def test_process_move_success_checkmate_result_overrides_status():
    engine = FakeEngine()
    engine.should_validate = True
    engine.new_state = {
        "activeColor": "white",
        "players": {"white": "p1", "black": "p2"},
        "board": [],
    }
    engine.in_check = True
    engine.raw_result = {"raw": True}
    engine.serialized_result = {"isOver": True, "reason": "checkmate"}
    pipeline = ValidationPipeline(engine)

    out = pipeline.processMove(
        {
            "activeColor": "white",
            "players": {"white": "p1", "black": "p2"},
            "board": [],
        },
        "p1",
        {"x": 1},
    )

    assert out["success"] is True
    assert out["status"] == "checkmate"
    assert out["result"]["reason"] == "checkmate"


def test_process_move_check_eval_failures_fall_back_to_illegal_move():
    engine = FakeEngine()
    engine.should_validate = False
    engine.raise_on_check_eval = True
    pipeline = ValidationPipeline(engine)

    state = {
        "activeColor": "white",
        "players": {"white": "p1", "black": "p2"},
        "board": [],
    }

    out = pipeline.processMove(state, "p1", {"x": 1})

    assert out["success"] is False
    assert out["error"] == "illegal move"


def test_opponent_color_supports_strings_and_enums():
    assert ValidationPipeline._opponent_color("white") == "black"
    assert ValidationPipeline._opponent_color("black") == "white"
    assert ValidationPipeline._opponent_color(Color.WHITE) == Color.BLACK
    assert ValidationPipeline._opponent_color(Color.BLACK) == Color.WHITE
