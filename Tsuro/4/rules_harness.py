import json
import sys

from Admin.referee import Referee
from Common import rules
from Common.board import Board
from Common.errors import TsuroError
from Common.placement import InitialPlacement, IntermediatePlacement, PlacementFactory
from Player.player import Player


def init_ref(instrs):
    placements = [PlacementFactory.create(x) for x in instrs]
    ref = Referee()
    ref.add_placements(placements)
    return ref


def check_turn(turn, ref):
    color, tile_index, rotation, x, y = turn[0]
    tile_index_2, tile_index_3 = turn[1], turn[2]
    placement = IntermediatePlacement(tile_index, rotation, color, x, y)

    try:
        player = ref.players[placement.color]
    except KeyError as e:
        raise TsuroError(f"{str(e)} did not play an initial placement")

    player.tile_hand = [tile_index, tile_index_2, tile_index_3]

    for rule in rules.ALL:
        is_valid, _ = rule.is_valid(placement, ref.board, player)
        if not is_valid:
            return "illegal"

    return "legal"


if __name__ == "__main__":
    try:
        instrs = json.loads(sys.stdin.read())
        ref = init_ref(instrs[:-1])
        result = check_turn(instrs[-1], ref)
    except (json.JSONDecodeError, TsuroError) as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(code=1)

    print(json.dumps(result))
