import tkinter as tk
from tkinter import messagebox
import chess
import time

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game with Timer")
        self.root.geometry("800x600")

        # Initial setup for the game
        self.board = chess.Board()

        # Initialize timers and player names
        self.player1_time = 300  # Default 5 minutes
        self.player2_time = 300
        self.current_player = "Player 1"

        # Create initial game screen (Welcome Screen)
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Creates the welcome screen to enter player names and timer limit."""
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.pack(pady=20)

        self.player1_label = tk.Label(self.welcome_frame, text="Enter Player 1 Name:")
        self.player1_label.pack()
        self.player1_entry = tk.Entry(self.welcome_frame)
        self.player1_entry.pack()

        self.player2_label = tk.Label(self.welcome_frame, text="Enter Player 2 Name:")
        self.player2_label.pack()
        self.player2_entry = tk.Entry(self.welcome_frame)
        self.player2_entry.pack()

        self.timer_label = tk.Label(self.welcome_frame, text="Enter Timer Limit (in minutes):")
        self.timer_label.pack()
        self.timer_entry = tk.Entry(self.welcome_frame)
        self.timer_entry.pack()

        self.start_button = tk.Button(self.welcome_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        """Start the game after getting player names and timer limit."""
        player1_name = self.player1_entry.get() or "Player 1"
        player2_name = self.player2_entry.get() or "Player 2"
        timer_limit = self.timer_entry.get()
        
        if timer_limit.isdigit():
            self.player1_time = int(timer_limit) * 60
            self.player2_time = int(timer_limit) * 60
        else:
            self.player1_time = self.player2_time = 300

        self.player1_name = player1_name
        self.player2_name = player2_name

        self.welcome_frame.pack_forget()
        self.create_game_ui()

    def create_game_ui(self):
        """Create the main UI for the chess game."""
        self.timer_frame = tk.Frame(self.root)
        self.timer_frame.pack()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(expand=True, fill=tk.BOTH)
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack()

        self.player1_timer_label = tk.Label(self.timer_frame, text="Player 1: 05:00", font=("Arial", 16))
        self.player1_timer_label.pack(side=tk.LEFT, padx=20)
        self.player2_timer_label = tk.Label(self.timer_frame, text="Player 2: 05:00", font=("Arial", 16))
        self.player2_timer_label.pack(side=tk.RIGHT, padx=20)

        self.status_label = tk.Label(self.status_frame, text=f"Current Turn: {self.player1_name}", font=("Arial", 16))
        self.status_label.pack(side=tk.LEFT)

        self.draw_button = tk.Button(self.status_frame, text="Propose Draw", command=self.propose_draw)
        self.draw_button.pack(side=tk.RIGHT)

        self.cells = {}
        self.create_board()

        # Timer
        self.last_update_time = time.time()
        self.update_timer()

        # Selected piece for movement
        self.selected_square = None

    def create_board(self):
        """Create the chessboard grid with buttons, maintaining consistent colors and size."""
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                square = chess.square(col, 7 - row)
                button = tk.Button(
                    self.board_frame,
                    bg=color,
                    relief="flat",
                    command=lambda sq=square: self.on_square_click(sq),
                    font=("Arial", 12)  # Fixed font size for consistency
                    )
                button.grid(row=row, column=col, sticky="nsew")
                self.cells[square] = {"button": button, "color": color}

    # Configure rows and columns to maintain consistent size
        for i in range(8):
            self.board_frame.grid_rowconfigure(i, weight=1, minsize=50)  # Set a minimum row height
            self.board_frame.grid_columnconfigure(i, weight=1, minsize=50)  # Set a minimum column width

        self.update_board()


    def update_board(self):
        """Update the pieces displayed on the board with consistent colors."""
        for square, cell in self.cells.items():
            button = cell["button"]
            piece = self.board.piece_at(square)
            text = f"{'W' if piece and piece.color else 'B' if piece else ''}{piece.symbol().upper() if piece else ''}"
            button.config(text=text, bg=cell["color"])


        # Check if the king is in check
        king_square = self.board.king(self.board.turn)
        if self.board.is_attacked_by(not self.board.turn, king_square):
        # Highlight the king's square
            self.cells[king_square]["button"].config(bg="red")
        else:
        # Reset the king's square color
            self.cells[king_square]["button"].config(bg=self.cells[king_square]["color"])

    def on_square_click(self, square):
        """Handle a square click event."""
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and ((self.board.turn and piece.color) or (not self.board.turn and not piece.color)):
                self.selected_square = square
                self.highlight_moves(square)
        else:
            move = chess.Move(from_square=self.selected_square, to_square=square)

            # Handle pawn promotion
            if (
                self.board.piece_at(self.selected_square).piece_type == chess.PAWN
                and chess.square_rank(square) in [0, 7]
            ):
                self.pawn_promotion(square)  # Handle the promotion
            elif move in self.board.legal_moves:
                self.board.push(move)
                self.switch_turn()

            self.selected_square = None
            self.clear_highlights()
            self.update_board()

        if self.board.is_game_over():
            self.end_game()


    def highlight_moves(self, square):
        """Highlight the valid moves for the selected piece."""
        legal_moves = [move for move in self.board.legal_moves if move.from_square == square]
        for move in legal_moves:
            target_square = move.to_square
            self.cells[target_square]["button"].config(bg="green")

    def clear_highlights(self):
        """Clear all highlighted squares."""
        for cell in self.cells.values():
            button = cell["button"]
            button.config(bg=cell["color"])

    def switch_turn(self):
        """Switch the current player's turn and update the timer."""
        self.current_player = self.player2_name if self.board.turn else self.player1_name
        self.status_label.config(text=f"Last Played by: {self.current_player}")
        self.last_update_time = time.time()

    def update_timer(self):
        """Update the timers for both players."""
        current_time = time.time()
        elapsed = current_time - self.last_update_time

        if self.board.turn:
            self.player1_time -= elapsed
        else:
            self.player2_time -= elapsed

        self.last_update_time = current_time

        self.player1_timer_label.config(text=f"Player 1: {int(self.player1_time // 60):02}:{int(self.player1_time % 60):02}")
        self.player2_timer_label.config(text=f"Player 2: {int(self.player2_time // 60):02}:{int(self.player2_time % 60):02}")

        if self.player1_time <= 0 or self.player2_time <= 0:
            self.end_game()

        self.root.after(50, self.update_timer)

    def pawn_promotion(self, square):
        """Handle pawn promotion with a custom popup for selection."""
        promotion_window = tk.Toplevel(self.root)
        promotion_window.title("Pawn Promotion")
        tk.Label(promotion_window, text="Choose a piece for promotion:").pack(pady=10)

        def promote_to(piece_type):
            self.board.push(chess.Move(self.selected_square, square, promotion=piece_type))
            promotion_window.destroy()
            self.update_board()
            self.switch_turn()

        promotion_choices = {
            "Queen": chess.QUEEN,
            "Rook": chess.ROOK,
            "Bishop": chess.BISHOP,
            "Knight": chess.KNIGHT
        }

        for name, piece_type in promotion_choices.items():
            tk.Button(
                promotion_window, text=name,
                command=lambda pt=piece_type: promote_to(pt)
            ).pack(padx=10, pady=5)

        promotion_window.transient(self.root)
        promotion_window.grab_set()
        self.root.wait_window(promotion_window)

    def propose_draw(self):
        """Handle the 'Draw' button press to propose a draw."""
        response = messagebox.askyesno("Draw Proposal", f"{self.current_player} proposes a draw. Do you accept?")
        if response:
            self.end_game()

    def end_game(self):
        """Handle end of game scenario."""
        if self.board.is_checkmate():
            messagebox.showinfo("Game Over", f"{self.current_player} wins by checkmate!")
        elif self.board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate! The game is a draw.")
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Game Over", "Insufficient material! The game is a draw.")
        elif self.player1_time <= 0 or self.player2_time <= 0:
            messagebox.showinfo("Game Over", f"{self.current_player} loses on time!")

        # Reset the game or quit
        reset_choice = messagebox.askyesno("Restart?", "Do you want to start a new game?")
        if reset_choice:
            self.restart_game()
        else:
            self.root.quit()

    def restart_game(self):
        """Restart the game with a new board and reset timers."""
        self.board.reset()
        self.player1_time = 300
        self.player2_time = 300
        self.current_player = "Player 1"
        self.update_board()
        self.update_timer()
        self.status_label.config(text=f"Last Played By: {self.current_player}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()