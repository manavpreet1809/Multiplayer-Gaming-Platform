from fastapi import Depends, HTTPException, Request, Form, status
from services.authServices import get_current_user
from models.Game import Game
from models.GameStatus import GameStatus
from db.GameRepository import GameRepository
from db.mongo import db
from typing import Annotated

lobbies = db["games"]

# Create game endpoint
@router.post("/games")
async def createGame(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    visibility: Annotated[int, Form()],
    player_count: Annotated[int, Form()]
):
    # Make sure the player is not already in a game
    if current_user.current_game is not None: # TODO: current_game is not implemented
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "User is already in a game"
        )

    # Instantiate game and send it to the DB
    game = Game(current_user, visibility, player_count, GameStatus.WAITING)
    game_id = await GameRepository.createGame(game)

    # Return the game_id to the front-end; they will send a request to create a WebSocket
    # The lobby code is also returned for the user (regardless of the private/public setting)
    # TODO: The WebSocket should only accept if the player is inside the game in the DB
    return { "success": True, "game_id": game_id, "lobby_code": game.lobby_code }

# Joining games 
@router.post("/join/{lobby_code}", status_code = status.HTTP_200_OK)
async def joinGame(
    lobby_code: str,
    current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    # Make sure the player is not already in a game
    if current_user.current_game is not None: # TODO: current_game is not implemented
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "User is already in a game"
        )

    # The difference between private and public lobbies is that private ones don't reveal their code
    # Public lobbies will store it in their "Join" button

    # Attempt to get a game by the given code
    game = await GameRepository.getGameByCode(lobby_code)

    # Make sure the game actually exists
    if game is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Game not found"
        )

    # Make sure the game has not started yet
    if game.status != GameStatus.WAITING:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Game has already started or finished"
        )

    # Make sure the lobby is not full
    if len(game.player_ids) == game.max_players: # TODO: max_players is not implemented
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Game is full"
        )

    # If all checks passed, add the player 
    game.player_ids.append(current_user.user_id) # TODO: user_id is not implemented
    await GameRepository.updatePlayerMembership(game.game_id, game.player_ids)

    # Return the game_id to the front-end; they will use it to request a WebSocket
    # TODO: The WebSocket should only accept if the player is inside the game in the DB
    return { "success": True, "game_id": game.game_id }