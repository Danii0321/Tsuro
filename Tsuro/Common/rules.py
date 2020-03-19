from abc import ABC, abstractmethod

from Common.constants import Direction, OutOfBounds, Rotation
from Common.utils import get_coordinates_in_direction


class InvalidMoveError(Exception):
    pass


class Rule(ABC):
    @abstractmethod
    def is_valid(self, next_move, board, player):
        pass


class UnoccupiedSpace(Rule):
    """All tiles being placed cannot be placed on an occupied space."""

    ERROR_MSG = "space occupied"

    def is_valid(self, next_move, board, player):
        if board.get_tile_at(next_move.x, next_move.y) is None:
            return True, None
        else:
            return False, self.ERROR_MSG


class WillPlayerSurvive(Rule):
    ERROR_MSG = "player does not survive"

    def is_valid(self, next_move, board, player):
        # has the player at the exit port
        tile = next_move.build_tile() if player.tile is None else player.tile
        port = tile.get_exit_port(next_move.port) if player.port is None else player.port

        if self._will_survive(tile, next_move.x, next_move.y, port.neighbor, board):
            # short circuit if the player's move is valid
            return True, None

        x, y = get_coordinates_in_direction(tile.x, tile.y, port.direction)

        # otherwise, figure out if they have any survivable moves
        if any(
            self._will_survive(t, x, y, port.neighbor, board) for t in self._possible_tiles(player)
        ):
            return False, self.ERROR_MSG

        # there are no survivable moves, allow this one
        return True, None

    def _possible_tiles(self, player):
        for t in player.tile_hand:
            for _ in Rotation:
                t.rotate_by(Rotation.ONE)
                yield t

    def _will_survive(self, tile, x, y, entry_port, board):
        exit_port = tile.get_exit_port(entry_port)
        next_x, next_y = get_coordinates_in_direction(x, y, exit_port.direction)
        next_tile = board.get_tile_at(next_x, next_y)

        if next_tile is OutOfBounds:
            # the player moves off the board
            return False
        elif next_tile is None:
            # the player reaches an unoccupied space on the board
            return True
        else:
            return self._will_survive(next_tile, next_x, next_y, exit_port.neighbor, board)


class FirstMoveOnBorder(Rule):
    """First move must be placed on border."""

    ERROR_MSG = "not_on_border"

    def is_valid(self, next_move, board, player):
        if next_move.is_initial and not (
            next_move.x == 0
            or next_move.x == board.SIZE - 1
            or next_move.y == 0
            or next_move.y == board.SIZE - 1
        ):
            return False, self.ERROR_MSG

        return True, None


class FirstMoveCheckNeighbors(Rule):
    """First move cannot have neighbors."""

    ERROR_MSG = "has neighbor"

    def is_valid(self, next_move, board, player):
        if next_move.is_initial:
            for direction in Direction:
                tile = board.get_tile_at(
                    *get_coordinates_in_direction(next_move.x, next_move.y, direction)
                )
                if tile is not OutOfBounds and tile is not None:
                    return False, self.ERROR_MSG

        return True, None


class FirstMoveOutsidePort(Rule):
    """Player must begin on an exterior port."""

    ERROR_MSG = "port not on outside edge"

    def is_valid(self, next_move, board, player):
        if next_move.is_initial:
            tile = board.get_tile_at(
                *get_coordinates_in_direction(next_move.x, next_move.y, next_move.port.direction)
            )

            if tile is not OutOfBounds:
                return False, self.ERROR_MSG

        return True, None


class IntermediateCheckPlacement(Rule):
    ERROR_MSG = "not adjacent to occupied port"

    def is_valid(self, next_move, board, player):
        if not next_move.is_initial:
            correct_x, correct_y = get_coordinates_in_direction(
                player.tile.x, player.tile.y, player.port.direction
            )

            if next_move.x != correct_x or next_move.y != correct_y:
                return False, self.ERROR_MSG

        return True, None


class InitialPlacementFirstOnly(Rule):
    """
    Player may only use initial placement once.

    This rule ensures that only initial placements can be used the first round
    of the game, and checks that only intermediate placements are used
    thereafter.
    """

    ERROR_MSG = "initial placements are first round only"

    def is_valid(self, next_move, board, player):
        if (
            player.tile is None
            and not next_move.is_initial
            or player.tile is not None
            and next_move.is_initial
        ):
            return False, self.ERROR_MSG
        return True, None


ALL = [
    # before other rules, ensure that when an initial placement is used, the
    # player has no tile, and vice-versa
    InitialPlacementFirstOnly(),
    # these rules are applicable to all placements
    UnoccupiedSpace(),
    WillPlayerSurvive(),
    # these rules are applicable to initial placements only
    FirstMoveOnBorder(),
    FirstMoveCheckNeighbors(),
    FirstMoveOutsidePort(),
    # these rules are applicable to intermediate placements only
    IntermediateCheckPlacement(),
]
