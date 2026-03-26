#!/bin/bash
# Exports the Chess and Tic-Tac-Toe board components as a shareable zip.
# Run from the frontend/ directory:  bash export-game-assets.sh
#
# Output: game-board-components.zip

set -e

OUTPUT="game-board-components.zip"
TEMP_DIR="game-board-export"

rm -rf "$TEMP_DIR" "$OUTPUT"
mkdir -p "$TEMP_DIR/ChessBoard" "$TEMP_DIR/TicTacToeBoard" "$TEMP_DIR/GameBoardDemo"

# Copy board components
cp src/components/ChessBoard/ChessBoard.js    "$TEMP_DIR/ChessBoard/"
cp src/components/ChessBoard/ChessBoard.css   "$TEMP_DIR/ChessBoard/"
cp src/components/ChessBoard/index.js         "$TEMP_DIR/ChessBoard/"
cp src/components/ChessBoard/README.md        "$TEMP_DIR/ChessBoard/"

cp src/components/TicTacToeBoard/TicTacToeBoard.js    "$TEMP_DIR/TicTacToeBoard/"
cp src/components/TicTacToeBoard/TicTacToeBoard.css   "$TEMP_DIR/TicTacToeBoard/"
cp src/components/TicTacToeBoard/index.js             "$TEMP_DIR/TicTacToeBoard/"
cp src/components/TicTacToeBoard/README.md            "$TEMP_DIR/TicTacToeBoard/"

# Copy demo page
cp src/components/GameBoardDemo/GameBoardDemo.js    "$TEMP_DIR/GameBoardDemo/"
cp src/components/GameBoardDemo/GameBoardDemo.css   "$TEMP_DIR/GameBoardDemo/"
cp src/components/GameBoardDemo/index.js            "$TEMP_DIR/GameBoardDemo/"

# Copy global styles (needed for Roboto font)
cp src/index.css "$TEMP_DIR/"

# Create a quick-start guide
cat > "$TEMP_DIR/SETUP.md" << 'EOF'
# Game Board Components — Quick Setup

## What's included

- **ChessBoard/** — 8x8 chess board with Unicode pieces, file/rank labels, move indicators
- **TicTacToeBoard/** — 3x3 grid with X/O marks, winning-cell highlights
- **GameBoardDemo/** — Interactive demo page to preview both boards
- **index.css** — Global styles (Roboto font import)

## How to use in your React project

1. Copy `ChessBoard/` and `TicTacToeBoard/` into your `src/components/` folder.
2. Make sure `index.css` (or your global stylesheet) imports the Roboto font:
   ```css
   @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
   body { font-family: 'Roboto', sans-serif; }
   ```
3. Import and use:
   ```jsx
   import ChessBoard from './components/ChessBoard';
   import TicTacToeBoard from './components/TicTacToeBoard';
   ```

## Color palette

All components use this palette:
- `#662691` (purple) — primary
- `#BEB8EB` (lavender) — borders, secondary
- `#F56476` (coral) — errors, danger
- `#ADFCF9` (mint) — success, ready
- `#F8F4A6` (yellow) — warnings, highlights

See each component's README.md for the full props reference.
EOF

# Zip it up
if command -v zip &> /dev/null; then
  zip -r "$OUTPUT" "$TEMP_DIR"
elif command -v tar &> /dev/null; then
  tar -czf "${OUTPUT%.zip}.tar.gz" "$TEMP_DIR"
  OUTPUT="${OUTPUT%.zip}.tar.gz"
fi

rm -rf "$TEMP_DIR"

echo ""
echo "Exported to: $OUTPUT"
echo "Share this file with your team members."
