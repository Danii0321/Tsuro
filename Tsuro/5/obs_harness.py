import json
import sys

from Admin import observer
from Admin.referee import Referee
from Common.constants import OutOfBounds
from Common.errors import InvalidPlacementError, TsuroError
from Common.placement import PlacementFactory
from Common.tiles import Tile
from Player.player import Player
from Player.strategy import Predetermined


# input -m obs_harness.py -i obs_tests/test1
# input format:  [color, tile-index, rotation, x, y, port], tile-index, tile-index, tile-index
# intermediate format: [ [color, tile-index, rotation, x, y], tile-index, tile-index ]
def render_results(inputs):
    """
    Performs placements and returns their results.
    """
    placements = [PlacementFactory.create(x) for x in inputs]

    players = []
    for i, placement in enumerate(placements):
        p = Player(name=str(i))
        p.color = placement.color
        players.append(p)

    ref = Referee(players)

    ref.add_placements(placements)

    return observer.render_board(ref.board, ref.players)


def render_intermediate(inputs, requested):
    placements = [PlacementFactory.create(x) for x in inputs + [requested[0]]]

    players = []
    for i, placement in enumerate(placements):
        p = Player(name=str(i))
        p.color = placement.color
        players.append(p)

    ref = Referee(players)
    ref.add_placements(placements[:-1])
    next_move = placements[-1]
    ref.players_by_color[next_move.color].tile_hand = [
        Tile.Builder.build(i).readonly() for i in requested[1:]
    ]
    ref.players_by_color[next_move.color].strategy = Predetermined(next_move)
    ref.turn_index = ref.turn_order.index(ref.players_by_color[next_move.color])

    return observer.render_board(ref.board, ref.players, ref.turn)


if __name__ == "__main__":
    try:
        inputs = json.loads(sys.stdin.read())
        if isinstance(inputs[-1][0], list):
            im = render_intermediate(inputs[:-1], inputs[-1])
        else:
            im = render_results(inputs)

        im.save("./tsuro.png", "PNG")

    except (json.JSONDecodeError, TsuroError) as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(code=1)
