class Move:
    def __init__(self):
        self.move_id = "id" #TODO
        self.game_id = "uuid" #TODO inherit
        self.player_id = "abcd" #TODO inherit
        self.action = 123 #TODO WebsocketMessage(event, payload, timestamp) (prob internal)
        pass

    def reconnect(self, id):
        pass #TODO

    def disconnect(self, id):
        pass #TODO