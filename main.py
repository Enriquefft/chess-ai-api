"""Chess api main module."""

from typing import Annotated, Optional

from fastapi import FastAPI, Query

from ChessEngine import get_best_move

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"Hello": "World"}


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
) -> Optional[str]:
    """Get the best engine move in ICI format."""
    best_move = get_best_move(fen, depth)
    return best_move.uci() if best_move is not None else None
