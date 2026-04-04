from fastapi import APIRouter, Depends, HTTPException, Request, Form
from src.app.services.authServices import get_current_user
from models.Game import Game
from db.GameRepository import GameRepository
from mongo import db

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
    return game_id


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
    return game_id


@router.post("/leave")
def game_leave(
    current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    current_game = get_current_game(current_user)

    # Make sure player is in a game
    if current_game is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not in a game.",
            headers={}
        )

    # If the host leaves, disband the lobby
    if is_host(current_user):
        kill_the_entire_lobby(current_game)
    else:
        # Just remove the user from the lobby
        lobbies.update_one({ "_id": current_game }, { "$pull": { "players": current_user.user_id } })

    return "success"

@router.post("/kick")
def game_kick(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    target_id
):
    current_game = get_current_game(current_user)

    # Make sure player is in a game
    if current_game is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not in a game.",
            headers={}
        )

    # Make sure player is the host
    if not is_host(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to kick.",
            headers={}
        )

    # Make sure target player is in the game
    if target_id not in current_game.players:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Target user is not in the game.",
            headers={}
        )

    # Remove user from lobby
    lobbies.update_one({ "_id": current_game }, { "$pull": { "players": target_id } })
    return "success"
    

    