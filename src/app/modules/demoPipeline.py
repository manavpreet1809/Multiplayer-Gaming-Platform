# Import the validation pipeline
from app.modules.validationPipeline import ValidationPipeline

# Import necessary chess assets
from app.modules.chess.chessEngine import ChessEngine
from app.models.chess.chessMove import ChessMove
from app.models.chess.chessPosition import ChessPosition

# Import necessary tic-tac-toe assets
from app.modules.TicTacToe.TicTacToeEngine import TicTacToeEngine
from app.models.tictactoe.TicTacToeMove import TicTacToeMove
from app.models.tictactoe.TicTacToePosition import TicTacToePosition

# How to use the chess validation pipeline
def run_chess_pipeline():
    # Not necessary, just for visuals
    print("\n--- Running chess validation pipeline ---")

    engine = ChessEngine()                                # 1. Create an instance of one of the game engines (in this case, ChessEngine)
    pipeline = ValidationPipeline(engine)                 # 2. Create an instance of the validation pipeline, passing in the game engine

    # An example game state
    state = engine.createInitialState(["player1", "player2"])

    # An example playerId
    playerId = "player1"

    # An example game move (note that the piece type here doesn't need to be specified, just the from and to positions themselves)
    move = ChessMove(fromPos=ChessPosition(1, 4), toPos=ChessPosition(3, 4)) # Pawn e4 move (assuming piece is a pawn)

    result = pipeline.processMove(state, playerId, move)  # 3. Use the validation pipeline's processMove method to run the entire pipeline (no need to do anything else).
                                                          # Simply pass the state, playerId and move from the API request

    # Not necessary, just for visuals
    print(
        "--- Finished chess validation pipeline ---\n"
        f'Success: {result["success"]}\n' # See success value
        f'Error: {result["error"]}\n'     # See error value
        f'Result: {result["result"]}\n'   # See result value
    )

# How to use the tic-tac-toe validation pipeline
def run_tictactoe_pipeline():
    pass

# This simulates how FastAPI would use the validation pipeline altogether
def main():
    # Note that main() simply calls each of the functions above.
    # But in reality, all that needs to be done is just following steps 1-3 within the functions above.
    # It then just becomes a matter of determining when/how those steps have to be used in response to FastAPI requests
    run_chess_pipeline()
    run_tictactoe_pipeline()

if __name__ == "__main__":
    main()