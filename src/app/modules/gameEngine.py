from abc import ABC, abstractmethod
from typing import List, Optional

class GameEngine(ABC):

    @abstractmethod
    def createInitialState(self, players: List[str]) -> dict:
        pass

    @abstractmethod
    def validateMove(self, state: dict, move: dict) -> bool:
        pass

    @abstractmethod
    def applyMove(self, state: dict, move: dict) -> dict:
        pass

    @abstractmethod
    def evaluateEnd(self, state: dict) -> Optional[dict]:
        pass