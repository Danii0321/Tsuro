import json
import logging
import socket
import sys

from Common.board import ReadOnlyBoard
from Common.constants import ClientMessage, Color, PlayerState, ServerMessage
from Common.tiles import Port, ReadOnlyTile
from Player.player import Player
from Player.strategy import Dumb, Second


log = logging.getLogger(__name__)


def start_client(host, port, name, strategy):
    client = Client(host, port, name, strategy)
    client.run_game()


class Client:
    def __init__(self, host, port, player_name, strategy_name):
        self.host = host
        self.port = port
        self.player_name = player_name
        self.strategy_name = strategy_name

    def run_game(self):
        log.info("started run game")
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            soc.connect((self.host, self.port))
            log.info("connected")
        except:
            log.error("Connection error")
            sys.exit()
        is_active = True
        strategy = None
        if self.strategy_name.lower() == "dumb":
            strategy = Dumb()
        elif self.strategy_name.lower() == "second":
            strategy = Second()
        player = Player(self.player_name, strategy)
        while is_active:
            data = soc.recv(5120).decode("utf8")
            if not data:
                exit(code=0)
            server_message = json.loads(data)

            try:
                msg_type = ServerMessage(server_message["type"])
            except ValueError:
                log.error(f"{server_message['type']} is not a valid message type")
                continue

            if msg_type is ServerMessage.ASK_FOR_PLAYER_INFO:
                # server should ask for join then send join request
                # fmt: off
                soc.sendall(
                    json.dumps(
                        {
                            "type": ClientMessage.JOIN.value,
                            "name": self.player_name,
                            "strategy": self.strategy_name,
                        }
                    ).encode("utf8")
                )
                # fmt: on
            if msg_type is ServerMessage.ASK_FOR_MOVE:
                # convert the json board into a Board
                # convert the json tiles into Tiles
                board = server_message["board"]
                real_board = ReadOnlyBoard.json_to_board(board)
                # player.receive_gamestate(real_board)

                # a list of tiles, call json to tile on each
                real_tiles = [ReadOnlyTile.json_to_tile(tile) for tile in server_message["tiles"]]

                player.receive_tiles(real_tiles)
                move = player.next_move()

                # fmt: off
                soc.sendall(
                    json.dumps(
                        {
                            "type": ClientMessage.MOVE_REQUEST.value,
                            **move.to_json()
                        }
                    ).encode("utf8")
                )
                # fmt: on

            if msg_type is ServerMessage.RECEIVE_COLOR:
                player.receive_color(Color(server_message["color"]))

            if msg_type is ServerMessage.MOVE_ACCEPTED:
                player.receive_move_success()

            if msg_type is ServerMessage.EJECTED:
                player.receive_move_failure(server_message["reason"])

            if msg_type is ServerMessage.RECEIVE_GAME_STATE:
                # their own message type and the interface for player should
                # support receiving them
                player.tile = (
                    ReadOnlyTile.json_to_tile(server_message["tile"])
                    if server_message["tile"] is not None
                    else None
                )
                player.port = (
                    Port[server_message["port"]] if server_message["port"] is not None else None
                )
                player.receive_gamestate(
                    ReadOnlyBoard.json_to_board(server_message["board"]),
                    PlayerState[server_message["state"]],
                    server_message["players"],
                )

        # soc.send(b"--quit--")
