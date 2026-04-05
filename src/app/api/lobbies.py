from fastapi import APIRouter, Depends, HTTPException, Request, Form
from src.app.services.authServices import get_current_user
from models.Game import Game
from db.GameRepository import GameRepository
from db.mongo import db
from db.ConnectionManager import manager

lobbies = db["games"]

# All endpoints here are prefixed with /game
router = APIRouter(prefix="/game", tags=["game"])

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

    # Return the game_id to the client; they will send a request to create a WebSocket
    return { "success": True, "game_id": game_id }


@router.post("/join/${game_id}")
def game_join(
    game_id,
    current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    # Make sure player is not in a game
    if get_current_game(current_user) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is already in a game.",
            headers={}
        )

    # Return the game_id to the client; they will send a request to create a WebSocket
    return { "success": True, "game_id": game_id }
