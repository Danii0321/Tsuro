from enum import Enum


OutOfBounds = object()


class Rotation(Enum):
    NONE = 0
    ONE = 90
    TWO = 180
    THREE = 270


class Color(Enum):
    WHITE = "white"
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Direction(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

    @property
    def opposite(self):
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }[self]


class PlayerState(Enum):
    ALIVE = "is alive"
    DEAD = "died"
    COLLIDED = "collided"
    EJECTED = "was ejected"


class ServerMessage(Enum):
    ASK_FOR_PLAYER_INFO = "ASK_FOR_PLAYER_INFO"
    RECEIVE_COLOR = "RECEIVE_COLOR"
    RECEIVE_GAME_STATE = "RECEIVE_GAME_STATE"
    ASK_FOR_MOVE = "ASK_FOR_MOVE"
    MOVE_ACCEPTED = "MOVE_ACCEPTED"
    EJECTED = "EJECTED"
    GAME_END = "GAME_END"


class ClientMessage(Enum):
    JOIN = "JOIN"
    MOVE_REQUEST = "MOVE_REQUEST"
