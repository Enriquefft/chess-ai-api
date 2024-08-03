"""Chess api main module."""

from typing import Literal, Optional

from chess import BLACK, WHITE, Move
from fastapi import FastAPI, HTTPException

from Game import Game

app = FastAPI()


Color = Literal["white", "black"]

user_games: dict[str, Game] = {}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"Hello": "World"}


@app.get("/start")
async def start(
    user_id: str,
    user_color: Color,
) -> Optional[Move]:
    """Start a new game for the user."""
    ch_color = WHITE if user_color == "white" else BLACK
    user_games[user_id] = Game(ch_color)
    if ch_color == BLACK:
        return user_games[user_id].play_engine_move()
    return None


@app.get("/play")
async def play_user(
    user_id: str,
    move: str,
) -> Move:
    """Play a move for the user and get the engine move."""
    if user_id not in user_games:
        raise HTTPException(status_code=404, detail="User not found")
    user_games[user_id].play_human_move(move)
    bot_move = user_games[user_id].play_engine_move()

    if bot_move is None:
        raise HTTPException(status_code=404, detail="Bot move not found")
    return bot_move
