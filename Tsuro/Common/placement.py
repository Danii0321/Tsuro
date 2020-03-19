import json
from abc import ABC

from Common.board import Position
from Common.constants import Color, Rotation
from Common.errors import InvalidPlacementError
from Common.tiles import Port, Tile


class Placement(ABC):
    def __init__(self, index, rotation, color, x, y):
        self.index = index
        try:
            self.rotation = Rotation(rotation)
            self.color = Color(color)
        except ValueError as e:
            raise InvalidPlacementError(str(e))
        if x < 0 or x > 9:
            raise InvalidPlacementError(f"x must be 0..9, got {x}")
        if y < 0 or y > 9:
            raise InvalidPlacementError(f"y must be 0..9, got {y}")
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Placement<{self.index}, {self.rotation}, {self.color}, x={self.x}, y={self.y}>"

    def build_tile(self):
        return Tile.Builder.build(self.index, rotation=self.rotation)

    @property
    def position(self):
        return Position(self.x, self.y)

    @property
    def is_initial(self):
        return False

    def to_json(self):
        placement_type = "INITIAL" if self.is_initial else "INTERMEDIATE"
        return {
            "placement_type": placement_type,
            "index": self.index,
            "rotation": self.rotation.value,
            "color": self.color.value,
            "x": self.x,
            "y": self.y,
        }


class IntermediatePlacement(Placement):
    pass


class InitialPlacement(Placement):
    def __init__(self, index, rotation, color, x, y, port):
        super().__init__(index, rotation, color, x, y)

        try:
            self.port = Port[port]  
        except KeyError as e:
            raise InvalidPlacementError(str(e))

    @property
    def is_initial(self):
        return True

    def to_json(self):
        json = super().to_json()
        # initial placements have an extra field, `port` - add it
        json["port"] = self.port.name
        return json


class PlacementFactory:
    @classmethod
    def create(cls, placement):
        if len(placement) == 6:
            index, rotation, color, port, x, y = placement
            return InitialPlacement(index, rotation, color, x, y, port)
        elif len(placement) == 5:
            color, index, rotation, x, y = placement
            return IntermediatePlacement(index, rotation, color, x, y)
        else:
            raise InvalidPlacementError(f"{json.dumps(placement)} is not a valid placement")

    @classmethod
    def json_to_placement(cls, json):
        if json["placement_type"] == "INITIAL":
            # fmt: off
            return InitialPlacement(
                json["index"],
                json["rotation"],
                json["color"],
                json["x"],
                json["y"],
                json["port"]
            )
            # fmt: on
        elif json["placement_type"] == "INTERMEDIATE":
            # fmt: off
            return IntermediatePlacement(
                json["index"],
                json["rotation"],
                json["color"],
                json["x"],
                json["y"]
            )
            # fmt: on
