from app.models.Visibility import Visibility
from app.models.GameStatus import GameStatus
from app.models.GameSettings import GameSettings
from app.models.GameState import GameState

# TODO: This is more of a Lobby class; create a Game class for the games themselves, and move some fields there
class Game:
    def __init__(self):
        self.game_id = "uuid" # TODO Assigned by database (Stub: DB)
        self.lobby_code = "abcd" # TODO generate 4-letter code (skip for now)
        self.visibility = Visibility.PUBLIC # TODO provided by player, expected through POST or PUT
        self.status = GameStatus.WAITING # Initialized to WAITING
        self.host_player = 12 # TODO: ID of host
        self.players = [] # Initialize an empty list of players
        self.settings = GameSettings(4, { "test": 123 }) # TODO expected through POST or PUT
        self.state = GameState() # TODO have a function that creates an empty state here (e.g. self.state = createGameState(self.gameType))
        pass

    def addPlayer(self, id):
        self.players.append(id) # TODO: make sure the ID is valid (the api is probably checking this so we assume a valid ID here)

    def removePlayer(self, id):
        try:
            self.players.remove(id)
        except ValueError as e:
            pass #TODO ID not found or something went wrong

    def move(self, move):
        pass #TODO

    def nextTurn(self):
        pass #TODO

    def isValid(self, move):
        pass #TODO