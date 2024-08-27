"""Chess api main module."""

from typing import Annotated, Literal, Optional

from chess import Move
from fastapi import FastAPI, Query

from ChessEngine import get_best_move

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"Hello": "World"}


Color = Literal["white", "black"]

FEN_REGEX = (
    "^([rnbqkpRNBQKP1-8]{1,8}/){7}[rnbqkpRNBQKP1-8]{1,8} "
    "[bw] [KQkq-]{1,4} [a-h1-8-]{1,2} \\d+ \\d+$"
)


@app.get("/move/{depth}")
async def get_move(
    depth: int,
    fen: Annotated[
        str,
        Query(
            description="The FEN string representing the chess board state",
            pattern=FEN_REGEX,
        ),
    ],
) -> Optional[Move]:
    """Play a move for the user and get the engine move."""
    return get_best_move(fen, depth)
