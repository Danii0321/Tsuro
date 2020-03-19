from unittest import TestCase
from unittest.mock import call, patch

from Common.board import Board
from Common.constants import Color, Direction, OutOfBounds
from Common.errors import InvalidBoardError
from Common.placement import InitialPlacement, IntermediatePlacement
from Common.tiles import Port, Tile
from Common.utils import get_tile


class TestBoard(TestCase):
    def test_neighboring_tiles_raises_error(self):
        with self.assertRaises(InvalidBoardError):
            t1 = Tile()
            t2 = Tile()
            Board(tiles={t1: (0, 0), t2: (0, 1)})

    def test_non_periphery_tile_raises_error(self):
        with self.assertRaises(InvalidBoardError):
            Board(tiles={Tile(): (5, 5)})

    def test_immediate_loss_tile_raises_error(self):
        with self.assertRaises(InvalidBoardError):
            Board(tiles={get_tile(22): (0, 0)})

    @patch("Common.tiles.Tile.set_neighbor")
    def test_add_tile(self, mock):
        board = Board()
        tile = Tile()
        board.add_tile(Tile(), 0, 0)
        self.assertEqual(board.grid[0][0], tile)
        mock.assert_has_calls(
            [
                call(OutOfBounds, Direction.NORTH),
                call(None, Direction.SOUTH),
                call(None, Direction.EAST),
                call(OutOfBounds, Direction.WEST),
            ]
        )

    def test_add_tile_out_of_bounds_raises_error(self):
        with self.assertRaises(InvalidBoardError):
            Board().add_tile(Tile(), 10000, 10000)

    def test_add_tile_moves_token(self):
        board = Board()
        board.add_initial_placements([InitialPlacement(10, 0, "blue", 0, 0, "A")])
        self.assertIs(board.grid[0][0].players[Port.D], Color.BLUE)

        board.add_intermediate_placements([IntermediatePlacement(7, 0, "blue", 1, 0)])
        self.assertIsNone(board.grid[0][0].players[Port.D])
        self.assertIs(board.grid[1][0].players[Port.B], Color.BLUE)
