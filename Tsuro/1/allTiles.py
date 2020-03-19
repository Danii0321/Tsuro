from itertools import permutations

from Common.render import draw_tile
from Common.tiles import Connection, Tile


def generate_all_tiles():
    port_permutations = []
    for permutation in permutations(Tile.DEFAULT_PORTS):
        stack = list(permutation)

        connections = []
        while stack:
            connections.append(Connection(stack.pop(), stack.pop()))

        port_permutations.append(tuple(sorted(connections)))

    tiles = []
    for permutation in set(port_permutations):
        tile = Tile()
        tile.add_connections(permutation)
        rot1 = Tile.rotated(tile)
        rot2 = Tile.rotated(rot1)
        rot3 = Tile.rotated(rot2)

        if any(t in tiles for t in (tile, rot1, rot2, rot3)):
            continue

        tiles.append(tile)

    return tiles


def main():
    tiles = generate_all_tiles()

    for i, tile in enumerate(tiles):
        print(f"Rendering tile {i+1}...")
        # im = draw_tile(tile)
        # im.save(f"./1/tile-{i+1}.png", "PNG")

    print("Done")
