from Visibility import Visibility
from GameStatus import GameStatus
from GameSettings import GameSettings
from GameState import GameState
from LobbyCode import LobbyCode

class Game:
    def __init__(self, current_player, visibility, max_players, status):
        self.lobby_code = LobbyCode.generate()
        self.host_player = current_player.user_id # TODO: user_id does not exist yet
        self.players = [current_player.user_id]
        self.visibility = visibility
        self.maxPlayers = max_players
        self.status = status
        self.state = GameState() # TODO: Game state
        self.move_history = {} # TODO: Move history

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