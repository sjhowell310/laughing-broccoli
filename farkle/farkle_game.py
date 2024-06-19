from __future__ import annotations

import argparse
import os
import random
import time
from collections import Counter


class Farkle:
    def __init__(
        self,
        num_players: int,
        order_dice: bool,
        score_limit: int,
        score_threshold: int,
        player_specify_set: bool,
    ):
        self.num_players = num_players or 2
        self.order_dice = order_dice or True
        self.score_limit = score_limit or 10000
        self.score_threshold = score_threshold or 500
        self.player_specify_set = player_specify_set or False
        self.get_players()
        self.play()

    def get_players(self):
        self.names = []
        for i in range(self.num_players):
            is_confirmed = False
            while not is_confirmed:
                name = input(f"Player {i + 1}, enter your name: ")
                response = ""
                while response not in ["y", "n", "\r\n"]:
                    response = input(
                        f"Player {i + 1} name : '{name}'. Is this correct? ",
                    ).lower()
                if response in ["y", "\n"]:
                    self.names.append(name)
                    is_confirmed = True
                else:
                    pass
        self.players = {
            name: {
                "turn_count": 1,
                "score": 0,
                "hand": {},
                "live_dice": 6,
            }
            for name in self.names
        }
        time.sleep(0.5)
        print(f"{len(self.players)} players created!\n{self.names}")

    number_suffixes = {
        item: "th"
        for item in [
            "0",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ]
    }
    number_suffixes.update({"1": "st", "2": "nd"})

    def play_round(self, player_name: str, player: dict):
        time.sleep(0.5)
        print(f"{'-'*os.get_terminal_size().columns}")
        print(
            f"{player_name}'s {player['turn_count']}{self.number_suffixes[str(player['turn_count'])[-1]]} turn!",
        )
        live_dice = 6
        is_round_live = True
        hold_score = 0
        while player["live_dice"] > 0 and is_round_live:
            player["hand"] = self.roll_dice(live_dice)
            live_dice, is_round_live, hold_score = self.choose_score(
                player,
                hold_score,
            )
        player["live_dice"] = 6
        player["turn_count"] += 1

    def roll_dice(self, dice_count: int):
        count: Counter = Counter()
        dice_roll = self.get_dice_roll(dice_count)
        time.sleep(0.5)
        print(f"You rolled {dice_roll}")
        for digit in dice_roll:
            if digit != "-":
                count[digit] += 1
        return count

    def get_dice_roll(self, dice_count: int):
        if self.order_dice:
            return "-".join(sorted([str(random.randint(1, 6)) for _ in range(dice_count)]))
        else:
            return "-".join([str(random.randint(1, 6)) for _ in range(dice_count)])

    def choose_score(self, player: dict, hold_score: int):
        score_sets = self.get_score_sets(player["hand"])
        if len(score_sets) == 0:
            time.sleep(0.5)
            print("No scoring set. Next player!\n")
            return 0, False, 0
        else:
            sorted_sets = sorted(
                score_sets,
                key=lambda x: x["score"],
                reverse=True,
            )
            set_reps = [f"{set['description']} for {set['score']}" for set in sorted_sets]
            print_sets = "\n".join(set_reps)
            time.sleep(0.5)
            print(
                f"Scoring set{'s' if len(print_sets) > 1 else ''} from your hand:\n{print_sets}\n",
            )
            take_count = 0
            while take_count < 1:
                time.sleep(0.5)
                print("You must take at least 1 scoring set from each roll!")
                response = ""
                response_count = 0
                for score_set in sorted_sets:
                    while response not in ["y", "n"]:
                        time.sleep(0.5)
                        response = input(
                            f"Would you like to take: {set_reps[sorted_sets.index(score_set)]}\n",
                        ).lower()
                        response_count += 1
                        if response_count % 3 == 0:
                            time.sleep(0.5)
                            print("response must be either y/n case insensitive")
                    if response in ["y"]:
                        hold_score = hold_score + score_set["score"]
                        player["live_dice"] = player["live_dice"] - score_set["count"]
                        take_count += 1
                    else:
                        pass
                    response = ""
                    response_count = 0

            response = ""
            response_count = 0
            while response not in ["y", "n"]:
                time.sleep(0.5)
                response = input(
                    f"You have {player['live_dice']} dice remaining, would you like to continue rolling?"
                    f" enter [N/n] to bank\nCurrent score: {player['score']}, Unbanked score: {hold_score}\n",
                ).lower()
                response_count += 1
                if response_count % 3 == 0:
                    time.sleep(0.5)
                    print("response must be either y/n case insensitive")
            if response in ["y"]:
                if player["live_dice"] == 0:
                    player["live_dice"] = 6
                return player["live_dice"], True, hold_score
            else:
                if player["score"] < self.score_threshold and hold_score < self.score_threshold:
                    time.sleep(0.5)
                    print(
                        f"First score to be banked must be {self.score_threshold} or above"
                        f", keep rolling until you get there or bust!",
                    )
                    return player["live_dice"], True, hold_score
                else:
                    time.sleep(0.5)
                    print(f"Banking score of {hold_score}.")
                    player["score"] += hold_score
                    time.sleep(0.5)
                    print(f"New score total: {player['score']}")
                    return 0, False, hold_score

    def play(self):
        i = 0
        while not any(player_stats["score"] >= self.score_limit for player_name, player_stats in self.players.items()):
            name = self.names[i % self.num_players]
            self.play_round(name, self.players[name])
            i += 1
        time.sleep(0.5)
        print(
            f"Final Round for players with less than {self.score_limit} points!",
        )
        for player_name, player_stats in {
            player: stats for player, stats in self.players.items() if stats["score"] < self.score_limit
        }.items():
            self.play_round(player_name, player_stats)
        sorted_players = sorted(
            self.players.items(),
            key=lambda x: x[1]["score"],
            reverse=True,
        )
        scores_on_doors = "\n".join(
            [f'{player[0]}: {player[1]["score"]}' for player in sorted_players],
        )
        print(f"""Player scores:\n{scores_on_doors}""")
        print(f"{sorted_players[0][0]} wins!\n")
        quit()

    individual_scores = {"1": 100, "5": 50}
    val_to_words = {
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
    }

    def get_score_sets(self, roll_dict: dict):
        score_sets = []
        if all(count == 2 for count in roll_dict.values()) and len(roll_dict.values()) == 3:
            score_sets.append(
                {
                    "description": "3 pairs",
                    "score": 1500,
                    "count": 6,
                },
            )
        if len(roll_dict.values()) == 6:
            score_sets.append(
                {
                    "description": "straight",
                    "score": 1500,
                    "count": 6,
                },
            )
        for value, count in roll_dict.items():
            if count == 6:
                if value != "1":
                    score = 4000
                else:
                    score = 8000
                score_sets.append(
                    {
                        "description": f"{self.val_to_words[count]} {value}s",
                        "score": score,
                        "count": count,
                    },
                )
                return score_sets  # nothing else to examine if six of a kind
            if count == 5:
                if value != "1":
                    score = 2000
                else:
                    score = 4000
                score_sets.append(
                    {
                        "description": f"{self.val_to_words[count]} {value}s",
                        "score": score,
                        "count": count,
                    },
                )
            if count == 4:
                if value != "1":
                    score = 1000
                else:
                    score = 2000
                score_sets.append(
                    {
                        "description": f"{self.val_to_words[count]} {value}s",
                        "score": score,
                        "count": count,
                    },
                )
            if count == 3:
                if value != "1":
                    score = 100 * int(value)
                else:
                    score = 1000
                score_sets.append(
                    {
                        "description": f"{self.val_to_words[count]} {value}s",
                        "score": score,
                        "count": count,
                    },
                )
            if (
                count in (1, 2)
                and not (all(count == 2 for count in roll_dict.values()) and len(roll_dict.values()) == 3)
                and not len(roll_dict.values()) == 6
            ):
                score = self.individual_scores.get(value, 0)
                if score:
                    for _ in range(count):
                        score_sets.append(
                            {
                                "description": f"One {value}",
                                "score": score,
                                "count": 1,
                            },
                        )
        return score_sets


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-players",
        help="limit of score to which farkle should be played",
        type=int,
    )
    parser.add_argument(
        "--order-dice",
        help="should rolled hand be displayed in a sorted order",
        type=bool,
    )
    parser.add_argument(
        "--score-limit",
        help="limit of score to which farkle should be played",
        type=int,
    )
    parser.add_argument(
        "--score-threshold",
        help="limit of score from which first score can be cashed",
        type=int,
    )
    parser.add_argument(
        "--player-specify-set",
        help="allow players to input the dice they wish to take",
        type=bool,
    )

    args = parser.parse_args()
    Farkle(
        num_players=args.num_players,
        order_dice=args.order_dice,
        score_limit=args.score_limit,
        score_threshold=args.score_threshold,
        player_specify_set=args.player_specify_set,
    )
