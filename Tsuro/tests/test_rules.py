from unittest import TestCase

from Common.board import Board
from Common.constants import Color, Rotation
from Common.placement import InitialPlacement, IntermediatePlacement
from Common.rules import (
    FirstMoveCheckNeighbors,
    FirstMoveOnBorder,
    FirstMoveOutsidePort,
    UnoccupiedSpace,
)
from Common.tiles import Port
from Common.utils import get_tile
from Player.player import Player


def dummy_placement(x=0, y=0, index=0):
    return IntermediatePlacement(get_tile(index), Rotation.NONE.value, Color.WHITE.value, x, y)


class TestUnoccupiedSpace(TestCase):
    def setUp(self):
        self.board = Board()
        self.board.add_tile(get_tile(0), x=0, y=0, rotation=0)
        self.player = Player()
        self.rule = UnoccupiedSpace()

    def test_valid(self):
        placement = dummy_placement(x=1, y=1)
        is_valid, msg = self.rule.is_valid(placement, self.board, Player())
        self.assertTrue(is_valid)

    def test_invalid(self):
        placement = dummy_placement(x=0, y=0)
        is_valid, msg = self.rule.is_valid(placement, self.board, Player())
        self.assertFalse(is_valid)
        self.assertEqual(msg, UnoccupiedSpace.ERROR_MSG)


class TestFirstMoveOnBorder(TestCase):
    def setUp(self):
        self.board = Board()
        self.player = Player()
        self.rule = FirstMoveOnBorder()

    def test_invalid(self):
        placement = dummy_placement(x=5, y=5)
        is_valid, msg = self.rule.is_valid(placement, self.board, self.player)
        self.assertFalse(is_valid)
        self.assertEqual(msg, FirstMoveOnBorder.ERROR_MSG)

    def test_valid(self):
        valid_coordinates = (
            (1, 0),  # north
            (1, Board.SIZE - 1),  # south
            (Board.SIZE - 1, 1),  # east
            (0, 1),  # west
            (0, 0),  # corner
        )

        for x, y in valid_coordinates:
            with self.subTest(x=x, y=y):
                placement = dummy_placement(x=x, y=y)
                is_valid, _ = self.rule.is_valid(placement, self.board, self.player)
                self.assertTrue(is_valid)


class TestFirstMoveCheckNeighbors(TestCase):
    def setUp(self):
        self.board = Board()
        self.board.add_tile(get_tile(0), x=5, y=5, rotation=0)
        self.player = Player()
        self.rule = FirstMoveCheckNeighbors()

    def test_valid(self):
        placement = dummy_placement(x=1, y=1)
        is_valid, _ = self.rule.is_valid(placement, self.board, self.player)
        self.assertTrue(is_valid)

    def test_invalid(self):
        invalid_coordinates = (
            (5, 4),  # north
            (5, 6),  # south
            (4, 5),  # east
            (6, 5),  # west
        )

        for x, y in invalid_coordinates:
            with self.subTest(x=x, y=y):
                placement = dummy_placement(x=x, y=y)
                is_valid, msg = self.rule.is_valid(placement, self.board, self.player)
                self.assertFalse(is_valid)
                self.assertEqual(msg, FirstMoveCheckNeighbors.ERROR_MSG)


class TestFirstMoveOutsidePort(TestCase):
    def setUp(self):
        self.board = Board()
        self.player = Player()
        self.rule = FirstMoveOutsidePort()

    def test_valid(self):
        placement = InitialPlacement(
            get_tile(0), Rotation.NONE.value, Color.WHITE.value, 0, 0, Port.A.value
        )
        is_valid, _ = self.rule.is_valid(placement, self.board, self.player)
        self.assertTrue(is_valid)

    def test_invalid(self):
        placement = InitialPlacement(
            get_tile(0), Rotation.NONE.value, Color.WHITE.value, 0, 0, Port.C.value
        )
        is_valid, msg = self.rule.is_valid(placement, self.board, self.player)
        self.assertFalse(is_valid)
        self.assertEqual(msg, FirstMoveOutsidePort.ERROR_MSG)
