from abc import ABC, abstractmethod
from typing import Any, List, Optional

class GameEngine(ABC):

    @abstractmethod
    def createInitialState(self, players: List[str]) -> dict:
        pass

    @abstractmethod
    def validateMove(self, state: dict, move: Any) -> bool:
        pass

    @abstractmethod
    def applyMove(self, state: dict, move: Any) -> dict:
        pass

    @abstractmethod
    def evaluateEnd(self, state: dict) -> Optional[dict]:
        pass

    @abstractmethod
    def serializeState(self, state: dict) -> dict:
        pass

    @abstractmethod
    def serializeEndResult(self, end_result: dict, state: dict = None) -> Optional[dict]:
        pass

    @abstractmethod
    def deserializeMove(self, move_dict: dict, state: dict = None):
        pass