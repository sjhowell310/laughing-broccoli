from __future__ import annotations
from farkle_game import Farkle
from fastapi import Body, FastAPI, Request, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.game_state = Farkle()
    yield
    # Optionally clean up resources here


app = FastAPI(lifespan=lifespan)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    # add your prod origin(s) here when ready
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


class FarklePlayer(BaseModel):
    name: str
    score: int = 0


class FarkleHand(BaseModel):
    rolled_hand: list[str]
    active_dice: list[str]
    dice_already_banked: list[str]


class GameState(BaseModel):
    players: list[FarklePlayer] = []
    current_player_name: str | None = None
    currently_active_hand: FarkleHand | None = None


initial_game_state = GameState()


@app.get("/")
async def main_route():
    return {"message": "Hey, It is me Goku"}


def get_game_state(request: Request) -> Farkle:
    """Dependency that returns the global service instance."""
    return request.app.state.game_state


@app.get("/game/configure")
async def configure_game_state(
    num_players: int = 2,
    order_dice: bool = False,
    score_limit: int = 10000,
    score_threshold: int = 500,
    player_specify_set: bool = False,
    game: Farkle = Depends(get_game_state),
) -> GameState:
    game.configure_game(
        num_players=num_players,
        order_dice=order_dice,
        score_limit=score_limit,
        score_threshold=score_threshold,
        player_specify_set=player_specify_set,
        initial_game_state=initial_game_state,
    )
    return game._get_game_state()


@app.get("/game/reset")
def reset(game: Farkle = Depends(get_game_state)):
    game = Farkle()
    return {"status": "reset done"}


@app.get("/game/state")
async def get_game_contents(game: Farkle = Depends(get_game_state)) -> GameState:
    return game._get_game_state()


@app.post("/game/add_player")
async def add_game_player(player_name: str, game: Farkle = Depends(get_game_state)):
    game.add_player(player_name=player_name)
    return game._get_game_state()


@app.post("/game/roll_dice")
async def roll_n_dice(n: int, game: Farkle = Depends(get_game_state)):
    return game.get_dice_roll(n)
