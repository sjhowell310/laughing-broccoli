from __future__ import annotations
from farkle_game import Farkle
from fastapi import Body, FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
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

@app.get("/game/start")
async def start_game_contents(
    num_players: int = 2,
    order_dice: bool = False,
    score_limit: int = 10000,
    score_threshold: int = 500,
    player_specify_set: bool = False 
    ) -> GameState:
    global game
    game = Farkle(num_players=num_players,
                  order_dice=order_dice,
                  score_limit=score_limit,
                  score_threshold=score_threshold,
                  player_specify_set=player_specify_set,
                  initial_game_state=initial_game_state)
    return game._get_game_state()

@app.post("/game/add_player")
async def add_game_player(
    player_name: str
):
    game.add_player(player_name=player_name)
    return game._get_game_state()

@app.post("/game/roll_dice")
async def roll_n_dice(
    n: int
):
    return game.get_dice_roll(n)
