## Chess Game with Timer - Readme

This is a Python script for a basic chess game with a timer functionality using the Tkinter library and the chess library.

**Features:**

* Standard chess gameplay with valid moves and piece captures.
* Timer for each player, configurable during game setup.
* Visual representation of the chessboard with colored squares and piece symbols.
* Highlights valid moves for the selected piece.
* Handles pawn promotion with user selection for the promoted piece.
* Allows proposing a draw and displays a message box for the outcome of the game (checkmate, stalemate, insufficient material, or time loss).
* Option to restart the game after it ends.

**Requirements:**

* Python 3.x
* Tkinter library (usually comes pre-installed with Python)
* chess library: `pip install chess`

**Running the Game:**

1. Save the script as `chess_app.py`.
2. Open a terminal or command prompt and navigate to the directory where you saved the script.
3. Run the script using the following command:

```
python chess_app.py
```

**Gameplay:**

1. The game starts with a welcome screen where you can enter player names and a timer limit (in minutes).
2. Click the "Start Game" button to begin the game.
3. The board will be displayed, with the current player's turn indicated.
4. Click on a piece to select it.
5. Valid moves for the selected piece will be highlighted in green.
6. Click on a highlighted square to move the piece.
7. The timer will continue to run for the current player. 
8. If a player runs out of time, the other player wins.
9. You can propose a draw by clicking the "Propose Draw" button.

**Additional Notes:**

* This is a basic implementation and lacks features like castling, en passant, and advanced AI opponents.
* The code is well-commented and structured for readability.
