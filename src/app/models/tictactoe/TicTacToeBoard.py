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

    def toList(self, symbol_map: dict = None) -> list:
        """Serialize to a flat 9-element list for the frontend.

        Args:
            symbol_map: optional dict mapping player names to "X"/"O".
                        e.g. {"Alice": "X", "Bob": "O"}
                        If None, cell values are returned as-is.
        """
        flat = []
        for row in self.grid:
            for cell in row:
                if cell is None:
                    flat.append(None)
                elif symbol_map and cell in symbol_map:
                    flat.append(symbol_map[cell])
                else:
                    flat.append(cell)
        return flat