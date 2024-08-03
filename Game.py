"""Game class implementation."""
import chess as ch

import ChessEngine as Ce

MAX_DEPTH = 3


class Game:
    """Chess engine wrapper class."""

    def __init__(self, color: ch.Color) -> None:
        """
        Initialize the Main class with a chess board.

        Args:
        ----
            board (Optional[ch.Board]): The chess board to be used for the game.
            color (ch.Color): The color the engine is playing.

        """
        self.engine = Ce.Engine(MAX_DEPTH, color)

    def play_human_move(self, move: str) -> None:
        """Handle the human player's move."""
        self.engine.add_move(move)

    def undo_human_move(self) -> None:
        """Handle the human player's undo move."""
        self.engine.undo_move()
        self.engine.undo_move()

    def play_engine_move(self) -> None:
        """
        Handle the engine's move.

        Args:
        ----
            max_depth (int): The maximum search depth for the engine.
            color (ch.Color): The color the engine is playing.

        """
        best_move = self.engine.get_best_move()
        if best_move is not None:
            self.engine.add_move(best_move.uci())
