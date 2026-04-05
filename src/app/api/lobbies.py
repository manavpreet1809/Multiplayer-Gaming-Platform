from fastapi import Depends, HTTPException, Request, Form, status
from src.app.services.authServices import get_current_user
from models.Game import Game
from models.GameStatus import GameStatus
from models.Visibility import Visibility
from db.GameRepository import GameRepository
from db.mongo import db
from db.ConnectionManager import manager

lobbies = db["games"]

# Create game endpoint
@router.post("/create")
async def game_create(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    visibility: Annotated[int, Form()],
    player_count: Annotated[int, Form()]
):
    # Make sure player is not in a game
    if get_current_game(current_user) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is already in a game.",
            headers={}
        )

    # Instantiate game and send it to DB
    game = Game(current_user, visibility, player_count)
    game_id = await GameRepository.createGame(game)

    # Return the game_id to the front-end; they will send a request to create a WebSocket
    return { "success": True, "game_id": game_id }

# Joining public games
@router.post("/join/{game_id}", status_code = status.HTTP_200_OK)
async def game_join_public(
    game_id: str,
    current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    # Make sure the player is not already in a game
    if get_current_game(current_user) is not None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "User is already in a game"
        )

    game = await GameRepository.getGame(game_id)

    # Make sure the game actually exists
    if game is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Game not found"
        )

    # Make sure the game is public
    if game.visibility != Visibility.PUBLIC:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Game is private"
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

    # If all checks pass, return the game_id to the front-end
    # They will send a request to create a WebSocket
    return { "success": True, "game_id": game_id }
