# This is for testing purposes, to see a progression of how the methods are called and classes interact
# This is back-end stuff, so we are the server receiving requests

from Game import Game
from Player import Player
from Move import Move

# Request to create game

# 1. validate user (check authentication, make sure person is not already in game)
# 2. create an empty game instance, and set the player as leader (TODO: do we need the json, or do we skip this step and go straight to the database?)
# 3. add it to the database, and set the user's current game there as well
# 4. websocket creation?
# 5. send back success/fail

# if straight to database, we could have three mega functions (or actually this works with any approach):
# - Server.createGame(1, ...params) - player id 1 creates game with some params, returns game id
#     INSERT INTO Games(type, leader_id, maxPlayers) -- (adding blank game, with leader and type being foreign keys)
#       VALUES (2, 1, 4)
#     (use Server.connect to add the leader into the game)
# - Server.connect(3, 1) - add to game id 3 the player with id 1 (TODO: need table for join codes)
#     INSERT INTO PlayerGames(game_id, player_id)
#       VALUES (3, 1)
# - Server.disconnect(1) - disconnect player id 1 from game, if exists
#     SELECT * FROM PlayerGames
#       WHERE player.id = 1
# - Server.reconnect(1) - get player id 1's current game, if exists
# - Server.currentGame(1) - get current
#
# note to self: would be better if each functions did exactly one thing with the database

game = Game(user) # TODO: read parameters from the API request, pass those in here (pass in user as well to set leader)
print(vars(game))

# Request to join game

# 1. validate user
# 2. retrieve game from database
# 3. validate fullness, game id, etc.
# 4. add user in to database
# 5. set current game of that user in database
# 6. send back success/fail so page updates 

# Start game

# 1. validate (authentication, game exists, is party leader, etc.)
# 2. if success, send a start signal to every client and the empty board state
# 3. if fail, send an error message to just that user

# Leave game

# 1. validate (authentication, is in-game)
# 2. if success, leave game, update both user and game database (make sure to also update the game, i.e. auto-lose or skip a turn)
# 3. if fail, do nothing and send an error message

# Reconnect

# 1. on request, check the database to see if the user is in an existing game (since websocket will be destroyed)
# 2. if they are, fetch it and reconnect (implies user has a current game in the database)
# 3. otherwise, do nothing