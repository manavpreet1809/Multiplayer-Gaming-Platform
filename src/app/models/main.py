# This is for testing purposes, to see a progression of how the methods are called and classes interact
# This is back-end stuff, so we are the server receiving requests

from Game import Game
from Player import Player
from Move import Move

# Server receives request from player to create game

game = Game() # TODO: Map/dictionary/list to store active games
print(vars(game))