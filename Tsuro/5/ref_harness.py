import json
import sys

from Admin.referee import Referee
from Common import rules
from Common.constants import Color, PlayerState
from Common.errors import TsuroError
from Player.player import Player


def run_game(names):
    players = [Player(name=name, age=i) for i, name in enumerate(names)]
    ref = Referee(players=players)

    while ref.run_turn():
        pass

    overall_losers, overall_winners = [], []
    for round_number in reversed(sorted(ref.dead.keys())):
        results = ref.dead[round_number]

        winners = []
        for player, reason in results:
            (overall_losers if reason is PlayerState.EJECTED else winners).append(player.name)

        if winners:
            overall_winners.append(winners)

    return {"losers": overall_losers, "winners": overall_winners}


if __name__ == "__main__":
    try:
        names = json.loads(sys.stdin.read())
        result = run_game(names)
    except (json.JSONDecodeError, TsuroError) as e:
        raise e
        print(f"Error: {e}", file=sys.stderr)
        exit(code=1)

    print(json.dumps(result))
