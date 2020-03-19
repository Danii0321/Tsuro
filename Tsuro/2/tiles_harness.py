#!/usr/bin/env python3
import json
import sys

from Common.json import MultipleJSONDecodeError, load_multiple
from Common.tiles import Tile
from Common.utils import get_tile


if __name__ == "__main__":
    try:
        # load the input from stdin and validate it
        objs = list(load_multiple(sys.stdin.read()))

    except MultipleJSONDecodeError as e:
        # print the error and exit with a status code of 1
        print(str(e))
        exit(code=1)

    for tile_num, deg, port in objs:
        t = get_tile(tile_num)

        # rotate the tile by the degrees specified
        t2 = Tile.rotated(t, deg)

        # now, given the port the player is on, return its partner
        p = t2.get_partner(port)

        output = ["if ", port, " is the entrance, ", p.name, " is the exit."]
        print(json.dumps(output))
