class TsuroError(Exception):
    """Base exception class for the package."""


class InvalidBoardError(TsuroError):
    """Raised when a :class:`Common.board.Board` is in an invalid state."""


class InvalidPlacementError(TsuroError):
    """Raised when a tile placement is invalid."""


class InvalidTileError(TsuroError):
    """Raised when a :class:`Common.tiles.Tile` is invalid."""


class InvalidGameError(TsuroError):
    """Raise when the configuration of a game is invalid."""
