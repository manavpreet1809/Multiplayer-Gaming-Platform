from typing import Optional, List
from app.modules.gameEngine import GameEngine
from app.models.tictactoe.TicTacToeBoard import TicTacToeBoard
from app.models.tictactoe.TicTacToeMove import TicTacToeMove
from app.models.tictactoe.TicTacToePosition import TicTacToePosition


class TicTacToeEngine(GameEngine):

    def createInitialState(self, players: List[str]) -> dict:
        return {
            "board": TicTacToeBoard(),
            "players": players,
            "currentPlayer": players[0],
            "moves": 0
        }

    def validateMove(self, state: dict, move: TicTacToeMove) -> bool:

        if state is None or move is None:
            return False

        if "board" not in state or "currentPlayer" not in state:
            return False

        board = state["board"]

        if not hasattr(move, "position") or move.position is None:
            return False

        pos = move.position

        if not (0 <= pos.row < 3 and 0 <= pos.col < 3):
            return False

        if pos.row > 2 or pos.col > 2:
            return False

        cell = board.getCell(pos)
        if cell is not None:
            return False

        if board.getCell(pos) is not None:
            return False

        return True

    def applyMove(self, state: dict, move: TicTacToeMove) -> dict:
        if state is None or move is None:
            return state

        board = state["board"]
        pos = move.position
        player = state["currentPlayer"]


        if board.getCell(pos) is None:
            board.setCell(pos, player)

        state["moves"] += 1

        players = state["players"]


        if player == players[0]:
            state["currentPlayer"] = players[1]
        else:
            state["currentPlayer"] = players[0]

        return state

    def _symbolMap(self, state: dict) -> dict:
        """Build a mapping from player names to 'X'/'O'.

        The first player is always 'X', the second is 'O'.
        """
        players = state["players"]
        return {players[0]: "X", players[1]: "O"}

    def serializeState(self, state: dict) -> dict:
        """Convert internal state to a JSON-serializable dict for the frontend.

        Handles:
        - 2D grid → flat 9-element array
        - Player names → "X"/"O" symbols
        """
        sym = self._symbolMap(state)
        current = sym[state["currentPlayer"]]
        return {
            "board": state["board"].toList(sym),
            "currentPlayer": current,
            "players": {sym[p]: p for p in state["players"]},
            "moves": state["moves"],
        }

    def deserializeMove(self, move_dict: dict, state: dict = None):
        """Convert a frontend move (cell index 0-8) to an internal TicTacToeMove."""
        index = move_dict["index"]
        row = index // 3
        col = index % 3
        return TicTacToeMove(TicTacToePosition(row, col))

    def evaluateEnd(self, state: dict) -> Optional[dict]:
        board = state["board"].grid

        # rows
        for row in board:
            if row[0] is not None and row[0] == row[1] == row[2]:
                return {"isOver": True, "result": "win", "winner": row[0]}

        # columns
        for col in range(3):
            if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
                return {"isOver": True, "result": "win", "winner": board[0][col]}

        # diagonals
        if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
            return {"isOver": True, "result": "win", "winner": board[0][0]}

        if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
            return {"isOver": True, "result": "win", "winner": board[0][2]}

        # draw
        if state["moves"] == 9:
            return {"isOver": True, "result": "draw"}

        return None

    def serializeEndResult(self, end_result: dict, state: dict = None) -> dict:
        """Convert evaluateEnd() output to a JSON-serializable dict.

        Maps the raw player-name winner to the "X"/"O" symbol so the
        frontend adapter can determine win/loss/draw relative to the local player.
        """
        if end_result is None:
            return None
        sym = self._symbolMap(state)
        serialized = dict(end_result)
        if "winner" in serialized and serialized["winner"] is not None:
            serialized["winner"] = sym.get(serialized["winner"], serialized["winner"])
        return serialized