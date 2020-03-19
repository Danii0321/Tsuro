import json
import logging
from abc import ABC, abstractmethod

from Common.constants import ClientMessage, ServerMessage
from Common.logging import XSERVER_LOGGER_NAME
from Common.placement import PlacementFactory
from Common.utils import receive_input
from Player.strategy import Dumb


log = logging.getLogger(__name__)
xserver_log = logging.getLogger(XSERVER_LOGGER_NAME)


class AbstractPlayer(ABC):
    def __init__(self, name, age=0, strategy=None):
        self._initialize()
        self.name = name
        self.age = age
        self.strategy = Dumb() if strategy is None else strategy

    def __repr__(self):
        return f"Player<{self.name}>"

    def _initialize(self):
        # the player's color
        self.color = None
        # the player's current tile and port
        self.tile = None
        self.port = None
        # the tiles currently in the player's hand
        self.tile_hand = []
        # the player's current state
        self.state = None
        # read only copies of the board and other players
        self.board = None
        self.players = None

    @abstractmethod
    def receive_game_end(self, results):
        pass

    @abstractmethod
    def receive_move_success(self):
        pass

    @abstractmethod
    def receive_move_failure(self, msg):
        pass

    @abstractmethod
    def next_move(self):
        pass

    @abstractmethod
    def receive_tiles(self, tiles):
        pass

    @abstractmethod
    def receive_gamestate(self, board, state, players):
        pass

    @abstractmethod
    def receive_color(self, color):
        pass


class ProxyPlayer(AbstractPlayer):
    def __init__(self, name, age, connection, buffer_size):
        super().__init__(name, age)
        self.connection = connection
        self.MAX_BUFFER_SIZE = buffer_size

    def receive_game_end(self, results):
        self._send_msg(
            ServerMessage.GAME_END,
            results={
                r: [(p.to_json(), s.name) for p, s in results] for r, results in results.items()
            },
        )

    def receive_move_success(self):
        self._send_msg(ServerMessage.MOVE_ACCEPTED)

    def receive_move_failure(self, msg):
        self._send_msg(ServerMessage.EJECTED, reason=msg)

    def next_move(self):
        self._send_msg(
            ServerMessage.ASK_FOR_MOVE,
            board=self.board,
            tiles=[t.get_json() for t in self.tile_hand],
        )
        msg = self._recv_msg()

        try:
            msg_type = ClientMessage(msg["type"])
        except ValueError:
            log.error(f"{msg['type']} is not a valid message type")
            return None

        if msg_type is not ClientMessage.MOVE_REQUEST:
            log.error(f"Expected {ClientMessage.MOVE_REQUEST.value}, got {msg_type.value}")
            return None

        return PlacementFactory.json_to_placement(msg)

    def receive_tiles(self, tiles):
        self.tile_hand = tiles

    def receive_gamestate(self, board, state, players):
        self.board = board.get_json()
        self.state = state.name
        player_jsons = [player.to_json() for player in players]
        self._send_msg(
            ServerMessage.RECEIVE_GAME_STATE,
            board=self.board,
            players=player_jsons,
            state=self.state,
            # them like this, this info should prob be received by a
            # function on player
            tile=self.tile.readonly().get_json() if self.tile is not None else None,
            port=self.port.name if self.port is not None else None,
        )

    def receive_color(self, color):
        self.color = color.value
        self._send_msg(ServerMessage.RECEIVE_COLOR, color=color.value)

    def _recv_msg(self):
        msg = receive_input(self.connection, self.MAX_BUFFER_SIZE)
        xserver_log.info(f"<< {self.color} {msg}")
        return msg

    def _send_msg(self, msg_type: ServerMessage, **msg_contents):
        """
        Sends a message to the client over the socket.

        :param msg_type: the message type, e.g., ASK_FOR_MOVE
        :param msg: optional, the contents of the message (excluding `type`)
        """
        # Add the key `type` to the message contents and serialize it to a JSON
        # string. (Overwrites the key `type` in the contents if it exists.)
        msg_str = json.dumps({**msg_contents, "type": msg_type.value})
        self.connection.sendall(msg_str.encode("utf-8"))
        xserver_log.info(f">> {self.color} {msg_str}")

    def to_json(self):
        return {
            "color": self.color,
            "tile": self.tile.readonly().get_json() if self.tile is not None else None,
            "port": self.port.name if self.port is not None else None,
            "state": self.state,
        }


class Player(AbstractPlayer):
    def receive_game_end(self):
        pass

    def receive_move_success(self):
        log.info(f"{self.color.value} moved successfully")

    def receive_move_failure(self, message):
        log.error(message)

    def next_move(self):
        self._next_move = self.strategy.next_move(self, self.board)
        return self._next_move

    def receive_tiles(self, tiles):
        tile_idxs = ", ".join(str(t.index) for t in tiles)
        log.info(f"{self.color.value} receiving tiles: {tile_idxs}")
        self.tile_hand = tiles

    def receive_gamestate(self, board, state, players):
        self.board = board
        self.state = state

    def receive_color(self, color):
        self.color = color
