from Common.constants import OutOfBounds
from Common.tiles import ReadOnlyTile
from Common.utils import get_or_default


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Position<{self.x}, {self.y}>"


class Board:
    SIZE = 10

    def __init__(self):
        self.grid = [[None for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]
        self.tiles = set()
        self.players = {}
        self.turn = None
        self.round = 0

    def set_players(self, players):
        temp = {}
        for player in players:
            temp[player.color] = player.tile
        self.players = temp

    def add_tile(self, tile: ReadOnlyTile, x: int, y: int):
        """
        Places the tile at the given coordinates.
        
        :param tile: the :class:`Tile` to place
        :param x: the x-coordinate of the tile to be placed, must be in the
            valid range for the board
        :param y: the y-coordinate of the tile to be placed, must be in the
            valid range for the board
        """
        self.grid[y][x] = tile
        self.tiles.add(tile)
        tile.x, tile.y = x, y

    def get_tile_at(self, x: int, y: int):
        """
        :return: Tile instance, None, or OutOfBounds
        """
        return get_or_default(get_or_default(self.grid, y, default=[]), x, default=OutOfBounds)

    def readonly(self):
        return ReadOnlyBoard(board=self)


class ReadOnlyBoard:
    def __init__(self, board):
        self.__board = board
        self.SIZE = board.SIZE

    def get_tile_at(self, x: int, y: int):
        """
        :return: ReadOnlyTile instance, None, or OutOfBounds
        """
        tile = self.__board.get_tile_at(x, y)
        if tile is not None and tile is not OutOfBounds:
            tile = tile.readonly()
        return tile

    def get_json(self):
        # only readonlytile has a get json method right now
        return [
            [tile.readonly().get_json() if tile is not None else None for tile in row]
            for row in self.__board.grid
        ]

    @classmethod
    def json_to_board(self, json):
        board = Board()
        board.grid = [
            [ReadOnlyTile.json_to_tile(tile) if tile is not None else None for tile in row]
            for row in json
        ]
        return board.readonly()
