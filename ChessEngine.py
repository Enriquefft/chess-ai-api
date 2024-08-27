"""Module for interacting with the chess."""

import secrets
from typing import Optional, cast

import chess

OPENING_PHASE_LIMIT = 10


def evaluate_board(board: chess.Board, color: chess.Color) -> float:
    """
    Evaluate the board using various heuristics.

    Args:
    ----
        board (chess.Board): The current state of the chess board.
        color (chess.Color): The color to evaluate the board for.

    Returns:
    -------
        float: The evaluation score of the board.

    """

    def square_res_points(square: chess.Square) -> float:
        piece_value = 0
        piece = board.piece_type_at(square)
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

        return piece_value if board.color_at(square) == color else -piece_value

    def mate_opportunity() -> float:
        if not board.legal_moves:
            return -999 if board.turn == color else 999
        return 0

    def opening() -> float:
        if board.fullmove_number < OPENING_PHASE_LIMIT:
            modifier = 1 / 30 * board.legal_moves.count()
            return modifier if board.turn == color else -modifier
        return 0

    score = sum(square_res_points(square) for square in chess.SQUARES)
    score += mate_opportunity()
    score += opening()
    score += 0.001 * secrets.randbelow(1000) / 1000.0

    return score


def minimax(
    board: chess.Board,
    depth: int,
    max_depth: int,
    color: chess.Color,
    candidate: Optional[float] = None,
) -> float | Optional[chess.Move]:
    """
    Run the minimax algorithm with alpha-beta pruning.

    Args:
    ----
        board (chess.Board): The current state of the chess board.
        depth (int): The current search depth.
        max_depth (int): The maximum depth to search.
        color (chess.Color): The color of the player to move.
        candidate (Optional[float]): The candidate score to compare against.

    Returns:
    -------
        Union[float, chess.Move]: The best move or the evaluation score.

    """
    if depth == max_depth or not board.legal_moves:
        return evaluate_board(board, color)

    move_list = list(board.legal_moves)
    new_candidate = float("-inf") if depth % 2 != 0 else float("inf")
    best_move = None

    for move in move_list:
        board.push(move)
        value = cast(float, minimax(board, depth + 1, max_depth, color, new_candidate))

        if depth % 2 != 0:  # Maximizing (engine's turn)
            if value > new_candidate:
                if depth == 1:
                    best_move = move
                new_candidate = value
        elif value < new_candidate:
            new_candidate = value

        if candidate is not None and (
            (value < candidate and depth % 2 == 0)
            or (value > candidate and depth % 2 != 0)
        ):
            board.pop()
            break

        board.pop()

    return new_candidate if depth > 1 else best_move



def get_best_move(
    board_fen: str,
    color: chess.Color,
    max_depth: int,
) -> Optional[chess.Move]:
    """
    Get the best move for a given board state, color, and search depth.

    Args:
    ----
        board_fen (str): The current state of the chess board in fen format.
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        color (chess.Color): The color of the player to move.
        max_depth (int): The maximum depth to search.

    Returns:
    -------
        Optional[chess.Move]: The best move determined by the function.


    """
    board = chess.Board(fen=board_fen)
    return cast(chess.Move, minimax(board, 1, max_depth, color))
