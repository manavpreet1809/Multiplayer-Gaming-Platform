from Visibility import Visibility
from GameStatus import GameStatus
from GameSettings import GameSettings
from GameState import GameState
from LobbyCode import LobbyCode

class Game:
    def __init__(self, current_player):
        self.lobby_code = LobbyCode.generate()
        self.status = GameStatus.WAITING
        self.host_player = current_player.user_id # TODO: This field does not exist yet
        self.players = [current_player.user_id]
        self.visibility = Visibility.PUBLIC # TODO: Should be provided as input
        self.maxPlayers = 4 # TODO: Should be provided as input
        self.settings = GameSettings(4, { "test": 123 }) # TODO: No clue what this is, might have maxPlayers on it
        self.state = GameState() # TODO: Empty game state
        self.move_history = {} # TODO

    def toDict(self):
        return {
            "lobby_code": self.lobby_code,
            "status": self.status,
            "host_player": self.host_player,
            "players": self.players,
            "state": self.state.to_dict(),
            "move_history": self.move_history
        }
    
    @staticmethod
    def fromDict(data):
        if not data: return GameState()
        return GameState(
            data.get("_id"),
            data.get("lobby_code"),
            data.get("status"),
            data.get("host_player"),
            data.get("players"),
            data.get("state"),
            data.get("move_history")
        )

    def addPlayer(self, user_id):
        self.players.insert(user_id) # TODO: make sure the ID is valid

    def removePlayer(self, user):
        try:
            self.players.remove(user_id)
        except ValueError as e:
            pass #TODO ID not found or something went wrong

    def move(self, move):
        pass #TODO

    def nextTurn(self):
        pass #TODO

    def isValid(self, move):
        pass #TODO