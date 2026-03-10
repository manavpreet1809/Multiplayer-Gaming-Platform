from Visibility import Visibility
from GameStatus import GameStatus
from GameSettings import GameSettings
from GameState import GameState

class Game:
    def __init__(self):
        self.game_id = "uuid" #TODO Make sure this actually gets a unique ID; hook up to server (STUB)
        self.lobby_code = "abcd" #TODO generate 4-letter code
        self.visibility = Visibility.PUBLIC #TODO enumeration
        self.status = GameStatus.WAITING #TODO status
        self.current_player = 123 #TODO presumably the id of the client
        self.host_player = 12 #TODO host player id
        self.players = [] # Initialize an empty list of players
        self.settings = GameSettings(4, { "test": 123 })
        self.state = GameState() #TODO have a function that creates an empty state here (e.g. self.state = createGameState(self.gameType))
        pass

    def addPlayer(self, id):
        pass #TODO

    def removePlayer(self, id):
        pass #TODO

    def move(self, move):
        pass #TODO

    def nextTurn(self):
        pass #TODO

    def isValid(self, move):
        pass #TODO