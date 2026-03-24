from typing import List, Optional

from src.app.models.tictactoe.TicTacToePosition import TicTacToePosition


class TicTacToeBoard:
    def __init__(self):
        self.grid: List[List[Optional[str]]] = [
            [None for _ in range(3)] for _ in range(3)
        ]

    def getCell(self, position: TicTacToePosition) -> Optional[str]:
        return self.grid[position.row][position.col]

    def setCell(self, position: TicTacToePosition, value: str):
        self.grid[position.row][position.col] = value

    def isFull(self) -> bool:
        return all(cell is not None for row in self.grid for cell in row)