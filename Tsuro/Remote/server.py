import json
import logging
import socket
import sys
from threading import Thread

from Admin.referee import Referee
from Common.constants import ClientMessage, ServerMessage
from Common.logging import XSERVER_LOGGER_NAME
from Common.utils import receive_input
from Player.player import ProxyPlayer


log = logging.getLogger(__name__)
xserver_log = logging.getLogger(XSERVER_LOGGER_NAME)


def start_server(host, port):
    server = Server(host, port)
    server.start_server()


class Server:
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.clients = []
        self.accepting_connections = True
        self.players = []
        self.MAX_BUFFER_SIZE = 5120

    def start_server(self):

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
        soc.settimeout(30)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        log.info("Socket created")

        try:
            soc.bind((self.host, self.port))
        except:
            log.error("Bind failed. Error : " + str(sys.exc_info()))
            sys.exit()

        soc.listen(5)  # queue up to 5 requests
        log.info(f"Socket now listening on {self.host}:{self.port}")

        # infinite loop- do not reset for every requests
        while self.accepting_connections and len(self.clients) <= 5:
            try:
                connection, address = soc.accept()
                ip, port = str(address[0]), str(address[1])
                # connection message
                log.info("Connected with " + ip + ":" + port)
                try:
                    Thread(target=self.client_thread, args=(connection, ip, port)).start()
                    self.clients.append((ip, port))

                except:
                    log.exception("Thread did not start.")
            except socket.timeout as e:
                self.accepting_connections = False

        self.run_game()
        soc.close()

    """
        This can be where we prompt the client to give us data?
        This can also be where we process that data and then pass it on to the game
    """

    def run_game(self):

        """
        prompt players for moves in order of their position in the players array
        -their move is determined by their strategies
        -run the game on each player's move until the game ends

        need to have a ref set up
        """
        log.info("running game")
        referee = Referee(self.players)
        while referee.run_turn():
            pass

    def client_thread(self, connection, ip, port):
        msg_str = json.dumps({"type": ServerMessage.ASK_FOR_PLAYER_INFO.value})
        connection.sendall(msg_str.encode("utf8"))
        xserver_log.info(">> {msg_str}")
        # check timeout - they have to respond within a certain amt of time - use select
        # soc.settimeout(30)

        # this will be the decoded json
        client_input = receive_input(connection, self.MAX_BUFFER_SIZE)
        xserver_log.info(f"<< {json.dumps(client_input)}")

        try:
            msg_type = ClientMessage(client_input["type"])
        except ValueError:
            msg_str = json.dumps({"type": ServerMessage.EJECTED.value})
            connection.sendall(msg_str.encode("utf8"))
            log.error(f"{client_input['type']} is not a valid message type")

        if msg_type is ClientMessage.JOIN:
            log.info("Client is sending player data to join game")
            self.players.append(
                ProxyPlayer(
                    client_input["name"], len(self.players), connection, self.MAX_BUFFER_SIZE
                )
            )
