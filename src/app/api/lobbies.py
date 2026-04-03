from fastapi import APIRouter, Depends, HTTPException, Request
from src.app.services.authServices import get_current_user
from models.Game import Game
from db.GameRepository import GameRepository

# All endpoints here are prefixed with /game
router = APIRouter(prefix="/game", tags=["game"])

# Create game endpoint
@router.post("/create")
async def game_create(
    current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    # TODO: Check if user is in-game already (validation pipeline)

    # Instantiate game and send it to DB
    game = Game(current_user)
    game_id = await GameRepository.createGame(game)

    # Return the game_id to the client; they will send a request to create a WebSocket
    return game_id


@router.post("/join/${game_id}")
def game_join(
    game_id,
    current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    # TODO: Check if user is in-game already (validation pipeline)
    # TODO: Check if game is full (validation pipeline)

    # Return the game_id to the client; they will send a request to create a WebSocket
    return game_id


@router.post("/leave/{game_id}")
def game_leave(
    current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    # TODO: Check if user is in-game (validation pipeline)
    # TODO: Check if user is host
    pass
