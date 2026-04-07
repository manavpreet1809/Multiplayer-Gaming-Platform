from typing import Optional, List
from src.app.modules.gameEngine import GameEngine
from src.app.models.tictactoe.TicTacToeBoard import TicTacToeBoard
from src.app.models.tictactoe.TicTacToeMove import TicTacToeMove
from src.app.models.tictactoe.TicTacToePosition import TicTacToePosition


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
        board = state["board"]
        pos = move.position
        player = state["currentPlayer"]

        board.setCell(pos, player)
        state["moves"] += 1

        players = state["players"]
        state["currentPlayer"] = players[1] if player == players[0] else players[0]

        return state

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