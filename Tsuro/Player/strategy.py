from abc import ABC, abstractmethod

from Common import rules
from Common.constants import OutOfBounds, Rotation
from Common.placement import InitialPlacement, IntermediatePlacement
from Common.tiles import Port
from Common.utils import get_coordinates_in_direction, revolve


class Strategy(ABC):
    @abstractmethod
    def next_move(self, player, board):
        pass


class Dumb(Strategy):
    def next_move(self, player, board):
        if player.tile is None:
            for x, y in revolve(10, True):
                port = None
                for p in Port:
                    coords = get_coordinates_in_direction(x, y, p.direction)
                    if board.get_tile_at(*coords) is OutOfBounds:
                        port = p
                        break

                tile = player.tile_hand[2]
                placement = InitialPlacement(
                    tile.index, tile.rotation.value, player.color.value, x, y, port.name
                )

                if all(r.is_valid(placement, board, player) for r in rules.ALL):
                    return placement

        else:
            x, y = get_coordinates_in_direction(
                player.tile.x, player.tile.y, player.port.direction
            )
            tile = player.tile_hand[0]
            return IntermediatePlacement(tile.index, tile.rotation.value, player.color.value, x, y)


class Second(Strategy):
    def next_move(self, player, board):
        if player.tile is None:
            for x, y in revolve(10, False):
                port = None
                for p in Port:
                    coords = get_coordinates_in_direction(x, y, p.direction)
                    if board.get_tile_at(*coords) is OutOfBounds:
                        port = p
                        break

                tile = player.tile_hand[2]
                placement = InitialPlacement(
                    tile.index, tile.rotation.value, player.color.value, x, y, port.name
                )

                if all(r.is_valid(placement, board, player) for r in rules.ALL):
                    return placement

            else:
                x, y = get_coordinates_in_direction(
                    player.tile.x, player.tile.y, player.port.direction
                )
                for i in range(1, -1, -1):
                    tile = player.tile_hand[i]
                    for j in range(4):
                        placement = IntermediatePlacement(
                            tile.index, tile.rotation.value, player.color.value, x, y
                        )
                        if all(r.is_valid(placement, board, player) for r in rules.ALL):
                            return placement
                        tile.rotate_by(Rotation.ONE)
                tile = player.tile_hand[1]
                return IntermediatePlacement(
                    tile.index, tile.rotation.value, player.color.value, x, y
                )


class Predetermined(Strategy):
    def __init__(self, placement):
        self.placement = placement

    def next_move(self, player, board):
        return self.placement
