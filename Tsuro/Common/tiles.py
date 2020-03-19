import enum
import json
from copy import deepcopy

from Common.constants import Direction, OutOfBounds, Rotation
from Common.errors import InvalidTileError
from Common.utils import get_static_path


class Port(enum.Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7

    @classmethod
    def rotated_by(cls, port, rotation):
        return Port((port.value + rotation.value / 90 * 2) % 8)

    @property
    def neighbor(self):
        return {
            Port.A: Port.F,
            Port.B: Port.E,
            Port.C: Port.H,
            Port.D: Port.G,
            Port.E: Port.B,
            Port.F: Port.A,
            Port.G: Port.D,
            Port.H: Port.C,
        }[self]

    @property
    def direction(self):
        return {
            Port.A: Direction.NORTH,
            Port.B: Direction.NORTH,
            Port.C: Direction.EAST,
            Port.D: Direction.EAST,
            Port.E: Direction.SOUTH,
            Port.F: Direction.SOUTH,
            Port.G: Direction.WEST,
            Port.H: Direction.WEST,
        }[self]


class Connection:
    def __init__(self, port1, port2):
        self.port1 = port1
        self.port2 = port2
        self._ports = (port1, port2)

    def __repr__(self):
        return f"({self.port1}, {self.port2})"

    def rotate_by(self, rotation):
        self.port1 = Port.rotated_by(self.port1, rotation)
        self.port2 = Port.rotated_by(self.port2, rotation)
        self._ports = (self.port1, self.port2)


class Tile:
    DEFAULT_PORTS = [Port.A, Port.B, Port.C, Port.D, Port.E, Port.F, Port.G, Port.H]
    NUMBER_OF_TILES = 35

    class Builder:
        TILES_FILE = get_static_path("tiles.json")

        @classmethod
        def build(cls, index, rotation=Rotation.NONE):
            if index < 0 or index >= Tile.NUMBER_OF_TILES:
                raise InvalidTileError(f"No such tile with index {index}")

            with open(cls.TILES_FILE) as f:
                tile_connections = json.load(f)

            # construct the tile
            connections = (
                Connection(Port[port_a], Port[port_b])
                for port_a, port_b in tile_connections[index]
            )
            tile = Tile(index=index, connections=connections)

            # rotate the tile
            if rotation is not Rotation.NONE:
                tile.rotate_by(rotation)

            return tile

    def __init__(self, index, connections):
        """
        Constructs a tile.

        :param index: the index of the tile being constructed
        :param connections: the connections for this tile at its base rotation
        """
        # rotation, index, and connections should not be modifiable, these are
        # set by the builder to avoid tampering with the tile representation
        self.__index = index
        self.__connections = set(connections)
        self.__rotation = Rotation.NONE
        self.x = None
        self.y = None

    def __repr__(self):
        conns = " ".join(str(c) for c in self.__connections)
        return f"Tile<index={self.index}, {conns}>"

    def __eq__(self, other):
        return isinstance(other, Tile) and self.index == other.index

    def __hash__(self):
        return hash(self.index)

    @property
    def rotation(self):
        return self.__rotation

    @property
    def index(self):
        return self.__index

    @property
    def connections(self):
        return deepcopy(self.__connections)

    def get_exit_port(self, entry_port):
        for c in self.__connections:
            if c.port1 is entry_port:
                return c.port2
            elif c.port2 is entry_port:
                return c.port1

    def rotate_by(self, rotation):
        for c in self.__connections:
            c.rotate_by(rotation)
        self.__rotation = Rotation((self.__rotation.value + rotation.value) % 360)

    def readonly(self):
        return ReadOnlyTile(tile=self)


class ReadOnlyTile:
    def __init__(self, tile):
        self.__tile = tile

    def __repr__(self):
        return "ReadOnly" + self.__tile.__repr__()

    def get_exit_port(self, entry_port):
        return self.__tile.get_exit_port(entry_port)

    @property
    def rotation(self):
        return self.__tile.rotation

    @property
    def index(self):
        return self.__tile.index

    @property
    def connections(self):
        return self.__tile.connections

    @property
    def x(self):
        return self.__tile.x

    @property
    def y(self):
        return self.__tile.y

    def rotate_by(self, rotation):
        """
        Rotates the tile.

        Players *are* permitted to modify tiles by rotating them. It is the
        only allowed mutation on a :class:`ReadOnlyTile`.
        """
        self.__tile.rotate_by(rotation)

    def get_json(self):
        # because it would be equal to the array index. maybe we should not
        # send a 2D array but reconstruct it from a list of board tiles and
        # their x- y- coords
        # fmt: off
        return {
            "index": self.index,
            "rotation": self.rotation.value,
            "x": self.x,
            "y": self.y,
        }
        # fmt: on

    # convert a respresentation of the tile to a Tile
    @classmethod
    def json_to_tile(self, json):
        # we have a tile index, rotation
        tile = Tile.Builder.build(json["index"], Rotation(json["rotation"]))
        tile.x = json["x"]
        tile.y = json["y"]
        return tile
