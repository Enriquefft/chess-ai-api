import random
from typing import Optional, cast

import chess

OPENING_PHASE_LIMIT = 10

class Engine:
    def __init__(self, max_depth: int, color: chess.Color)-> None:
        """
        Initialize the chess engine.

        Args:
        ----
            board (chess.Board): The chess board.
            max_depth (int): Maximum search depth.
            color (chess.Color): The color of the engine's pieces.

        """
        self.board = chess.Board()
        self.color = color
        self.max_depth = max_depth

    def add_move(self, move: str) -> chess.Move:
        """Add a move to the board."""
        return self.board.push_san(move)
    def undo_move(self) -> chess.Move:
        """Undo the last move."""
        return self.board.pop()



    def get_best_move(self) -> Optional[chess.Move]:
        """
        Get the best move for the engine.

        Returns
        -------
            Optional[chess.Move]: The best move determined by the engine.

        """
        return cast(chess.Move, self.engine(None, 1))

    def eval_function(self) -> float:
        """
        Evaluate the board using various heuristics.

        Returns
        -------
            float: The evaluation score of the board.

        """
        compt = 0
        # Sums up the material values
        for square in chess.SQUARES:
            compt += self.square_res_points(square)
        compt += self.mate_opportunity() + self.opening() + 0.001 * random.random()
        return compt

    def mate_opportunity(self) -> float:
        """
        Check for mate opportunities.

        Returns
        -------
            float: Mate opportunity score.

        """
        if not self.board.legal_moves:
            return -999 if self.board.turn == self.color else 999
        return 0

    def opening(self) -> float:
        """
        Encourages development in the opening phase of the game.

        Returns
        -------
            float: Opening development score.

        """
        if self.board.fullmove_number < OPENING_PHASE_LIMIT:
            modifier = 1 / 30 * self.board.legal_moves.count()
            return modifier if self.board.turn == self.color else -modifier
        return 0

    def square_res_points(self, square: chess.Square) -> float:
        """
        Return the Hans Berliner's system value of the resident piece at the given square.

        Args:
        ----
            square (chess.Square): The square to evaluate.

        Returns:
        -------
            float: The value of the resident piece.

        """
        piece_value = 0
        piece = self.board.piece_type_at(square)
        if piece == chess.PAWN:
            piece_value = 1
        elif piece == chess.ROOK:
            piece_value = 5.1
        elif piece == chess.BISHOP:
            piece_value = 3.33
        elif piece == chess.KNIGHT:
            piece_value = 3.2
        elif piece == chess.QUEEN:
            piece_value = 8.8

        return piece_value if self.board.color_at(square) == self.color else -piece_value

    def engine(self, candidate: Optional[float], depth: int) -> float| Optional[chess.Move]:
        """
        run the minimax algorithm with alpha-beta pruning.

        Args:
        ----
            candidate (Optional[float]): The candidate score to compare against.
            depth (int): The current search depth.

        Returns:
        -------
            Union[float, chess.Move]: The best move or the evaluation score.

        """
        # Reached max depth of search or no possible moves
        if depth == self.max_depth or not self.board.legal_moves:
            return self.eval_function()

        # Get list of legal moves of the current position
        move_list = list(self.board.legal_moves)

        # Initialize new candidate
        new_candidate = float("-inf") if depth % 2 != 0 else float("inf")
        best_move = None

        # Analyze board after deeper moves
        for move in move_list:
            # Play move
            self.board.push(move)

            # Get value of move (by exploring the repercussions)
            value = cast(float, self.engine(new_candidate, depth + 1))

            # Basic minimax algorithm
            if depth % 2 != 0:  # Maximizing (engine's turn)
                if value > new_candidate:
                    if depth == 1:
                        best_move = move
                    new_candidate = value
            elif value < new_candidate:
                new_candidate = value

            # Alpha-beta pruning cuts
            if candidate is not None and (
                (value < candidate and depth % 2 == 0) or (value > candidate and depth % 2 != 0)
            ):
                self.board.pop()
                break

            # Undo last move
            self.board.pop()

        # Return result
        return new_candidate if depth > 1 else best_move
