from unittest import TestCase
from unittest.mock import patch

from Common.constants import Direction, OutOfBounds
from Common.tiles import Port, Tile
from Common.utils import get_tile


class TestTile(TestCase):
    def test_has_neighbors(self):
        t = Tile()
        self.assertFalse(t.has_neighbors)
        t = Tile(north=OutOfBounds)
        self.assertFalse(t.has_neighbors)
        t = Tile(north=Tile())
        self.assertTrue(t.has_neighbors)

    def test_is_on_edge(self):
        t = Tile()
        self.assertFalse(t.is_on_edge)
        t = Tile(north=OutOfBounds)
        self.assertTrue(t.is_on_edge)

    @patch("Common.tiles.Tile._move_players")
    def test_set_neighbor_with_two_tiles(self, mock):
        t1, t2 = Tile(), Tile()
        t1.set_neighbor(t2, Direction.NORTH)
        self.assertIs(t1.north, t2)
        self.assertIs(t2.south, t1)
        mock.assert_called_with(Direction.NORTH)

    @patch("Common.tiles.Tile._move_players")
    def test_set_neighbor_with_out_of_bounds(self, mock):
        t1, t2 = Tile(), OutOfBounds
        t1.set_neighbor(t2, Direction.NORTH)
        self.assertIs(t1.north, OutOfBounds)
        mock.assert_not_called()

    @patch("Common.tiles.Tile._move_players")
    def test_set_neighbor_with_none(self, mock):
        t1, t2 = Tile(), None
        t1.set_neighbor(t2, Direction.NORTH)
        self.assertIsNone(t1.north)
        mock.assert_not_called()

    def test_move_players(self):
        tile = get_tile(10)
        tile.players[Port.C] = "blue"
        tile.east = get_tile(12)
        tile._move_players(Direction.EAST)
        self.assertIsNone(tile.players[Port.C])
        self.assertEqual(tile.east.players[Port.B], "blue")
