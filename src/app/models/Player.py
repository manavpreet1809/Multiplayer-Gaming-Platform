from ConnectionStatus import ConnectionStatus
from PlayerRole import PlayerRole

#TODO: This class appears to be used by Game to track players
class Player:
    def __init__(self):
        self.player_id = 21 #TODO stub imported from db
        self.name = "test" #TODO stub imported from db
        self.game_id = 124124 #TODO current game id
        self.connection_status = ConnectionStatus.DISCONNECTED #TODO connection status, prob set by another method
        self.role = PlayerRole.SPECTATOR #TODO player role, prob set by another method
        pass

    def reconnect(self):
        pass #TODO

    def disconnect(self):
        pass #TODO