"""Module for interacting with the chess."""

import secrets
from typing import Optional, cast

import chess

OPENING_PHASE_LIMIT = 10


PIECE_VALUES: dict[chess.PieceType, float] = {
    chess.PAWN: 1,
    chess.ROOK: 5.1,
    chess.BISHOP: 3.33,
    chess.KNIGHT: 3.2,
    chess.QUEEN: 8.8,
    chess.KING: 0,
}


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

    def piece_value(square: chess.Square) -> float:
        piece = board.piece_type_at(square)
        value = PIECE_VALUES[piece] if piece else 0
        return value if board.color_at(square) == color else -value

    def mate_opportunity() -> float:
        if not board.legal_moves:
            return -999 if board.turn == color else 999
        return 0

    def opening_modifier() -> float:
        if board.fullmove_number < OPENING_PHASE_LIMIT:
            modifier = 1 / 30 * board.legal_moves.count()
            return modifier if board.turn == color else -modifier
        return 0

    score = sum(piece_value(square) for square in chess.SQUARES)
    score += mate_opportunity()
    score += opening_modifier()
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
                new_candidate = value
                if depth == 1:
                    best_move = move
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
    max_depth: int,
) -> Optional[chess.Move]:
    """
    Get the best move for a given board state and search depth.

    Args:
    ----
        board_fen (str): The current state of the chess board in FEN format.
            A FEN string (e.g.,
            ``rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1``)
            consists of several parts:
            - The board part (:func:`~chess.Board.board_fen()`),
            - The active color (:data:`~chess.Board.turn`),
            - The castling availability (:data:`~chess.Board.castling_rights`),
            - The en passant target square (:data:`~chess.Board.ep_square`),
            - The halfmove clock (:data:`~chess.Board.halfmove_clock`),
            - The fullmove number (:data:`~chess.Board.fullmove_number`).

        max_depth (int): The maximum depth to search.

    Returns:
    -------
        Optional[chess.Move]: The best move determined by the function, or
        `None` if no valid move is found.

    """
    board = chess.Board(fen=board_fen)
    return cast(chess.Move, minimax(board, 1, max_depth, board.turn))
