"""Hermes Retail backend main module."""

import re
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Query

from ai import get_response

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"Hello": "World"}


class ChessPiece(str, Enum):
    """Chess piece enumeration."""

    KING = "K"
    QUEEN = "Q"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    PAWN = "P"
    PAWN_WITH_PASSANT = "PP"


@app.get("/route/k-moves")
async def get_k_moves(
    board: Annotated[
        list[list[ChessPiece]],
        "Current state of the chess board",
    ],
    k_moves: Annotated[
        int,
        Query(
            title="k moves",
            description="Number of moves to find",
        ),
    ],
) -> list[str]:
    """Find the best k moves for the current state of the chess board."""
    # Convert the board state to a human-readable format
    board_state = "\n".join(
        " ".join(piece.value if piece else "." for piece in row) for row in board
    )

    # Create the user message for the AI query
    user_message = (
        f"Given the current state of the chess board:\n{board_state}\n\n"
        f"Return the best {k_moves} moves in standard chess notation. Only list the moves, nothing else."
    )

    # Get the response from the AI
    response = get_response(user_message)

    # Post-process the response to ensure only valid chess moves are returned
    if response:
        # Regular expression pattern to match standard chess notation moves
        move_pattern = re.compile(
            r"([KQBNRP]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?|O-O(?:-O)?)",
        )
        moves = move_pattern.findall(response)
        return moves[:k_moves]

    return []
