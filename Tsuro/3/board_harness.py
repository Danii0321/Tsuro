import json
import sys

from Common.board import Board
from Common.constants import OutOfBounds
from Common.errors import InvalidPlacementError, TsuroError
from Common.placement import InitialPlacement, IntermediatePlacement, PlacementFactory


def get_results(inputs):
    """
    Performs placements and returns their results.
    """
    board = Board()

    placements = [PlacementFactory.create(x) for x in inputs]
    players = set([p.color for p in placements])

    initial_placements = [p for p in placements if isinstance(p, InitialPlacement)]

    board = Board()
    board.add_initial_placements(initial_placements)

    board.add_intermediate_placements(
        [p for p in placements if isinstance(p, IntermediatePlacement)]
    )

    starting_locations = {(p.x, p.y, p.port) for p in initial_placements}
    result = []
    for tile in board.tiles:
        for exit_port, player in tile.players.items():
            if player is not None:
                neighbor = tile.neighbor_by_port(exit_port)
                if neighbor is OutOfBounds:
                    if (tile.x, tile.y, exit_port) in starting_locations:
                        result.append([player.value, " collided"])
                    else:
                        result.append([player.value, " exited"])
                else:
                    result.append([player.value, tile.index, tile.rotation.value, tile.x, tile.y])

                players.remove(player)

    for player in players:
        result.append([player.value, " never played"])

    return result


if __name__ == "__main__":
    try:
        inputs = json.loads(sys.stdin.read())
        results = get_results(inputs)
    except (json.JSONDecodeError, TsuroError) as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(code=1)

    print(json.dumps(results))
