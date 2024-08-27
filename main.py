"""Chess api main module."""

from typing import Literal, Optional, Annotated

from chess import Move, WHITE, BLACK
from fastapi import FastAPI, Query
from ChessEngine import get_best_move

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"Hello": "World"}


Color = Literal["white", "black"]


@app.get("/move/{depth}")
async def get_move(
    depth: int,
    color: Annotated[Color, Query(None, description="The color of the player to move")],
    fen: Annotated[
        str,
        Query(None, description="The FEN string representing the chess board state"),
    ],
) -> Optional[Move]:
    """Play a move for the user and get the engine move."""
    chess_color = WHITE if color == "white" else BLACK
    return get_best_move(fen, chess_color, depth)
