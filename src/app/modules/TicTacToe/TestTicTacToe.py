from src.app.modules.TicTacToe.TicTacToeEngine import TicTacToeEngine
from src.app.models.tictactoe.TicTacToeMove import TicTacToeMove
from src.app.models.tictactoe.TicTacToePosition import TicTacToePosition


def print_board(board):
    for row in board:
        print(row)
    print()


engine = TicTacToeEngine()

print("=== TEST 1: BASIC WIN ===")
state = engine.createInitialState(["X", "O"])

moves = [(0,0),(1,0),(0,1),(1,1),(0,2)]

for row, col in moves:
    move = TicTacToeMove(TicTacToePosition(row, col))
    if engine.validateMove(state, move):
        state = engine.applyMove(state, move)
        print_board(state["board"].grid)
        result = engine.evaluateEnd(state)
        if result:
            print("Result:", result)
            break
    else:
        print("Invalid move")

print("\n=== TEST 2: INVALID MOVE ===")
state = engine.createInitialState(["X", "O"])

move = TicTacToeMove(TicTacToePosition(0,0))
engine.applyMove(state, move)

# try same move again
print("Should be False:", engine.validateMove(state, move))


print("\n=== TEST 3: DRAW ===")
state = engine.createInitialState(["X", "O"])

moves = [
    (0,0),(0,1),(0,2),
    (1,1),(1,0),(1,2),
    (2,1),(2,0),(2,2)
]

for row, col in moves:
    move = TicTacToeMove(TicTacToePosition(row, col))
    if engine.validateMove(state, move):
        state = engine.applyMove(state, move)
        result = engine.evaluateEnd(state)
        if result:
            print_board(state["board"].grid)
            print("Result:", result)
            break


print("\n=== TEST 4: OUT OF BOUNDS ===")
state = engine.createInitialState(["X", "O"])

move = TicTacToeMove(TicTacToePosition(3,3))
print("Should be False:", engine.validateMove(state, move))


print("\n=== TEST 5: PLAYER SWITCH ===")
state = engine.createInitialState(["X", "O"])

move1 = TicTacToeMove(TicTacToePosition(0,0))
state = engine.applyMove(state, move1)

print("Next player should be O:", state["currentPlayer"])

move2 = TicTacToeMove(TicTacToePosition(1,1))
state = engine.applyMove(state, move2)

print("Next player should be X:", state["currentPlayer"])