from collections import defaultdict
from operator import attrgetter
from typing import DefaultDict, Dict, List, Set, Tuple

from Common import rules
from Common.board import Board
from Common.constants import Color, OutOfBounds, PlayerState
from Common.errors import InvalidGameError
from Common.placement import Placement
from Common.tiles import Port, Tile
from Common.utils import get_coordinates_in_direction
from Player.player import Player


class Referee:
    MIN_PLAYERS = 3
    MAX_PLAYERS = 5

    def __init__(self, players: List, rules=rules.ALL.copy()):
        if not (self.MIN_PLAYERS <= len(players) <= self.MAX_PLAYERS):
            raise InvalidGameError(f"Invalid number of players {len(players)}")

        self.players: List[Player] = players
        self.rules: List[rules.Rule] = rules

        self._assign_turn_order()
        self._assign_colors()
        self._initialize()

    @property
    def turn(self):
        """
        The player whose turn it is based on the turn order.
        """
        return self.turn_order[self.turn_index]

    def run_turn(self):
        """
        Runs a turn of a game of Tsuro.
        :return: true if the turn was run, false if the game is over
        :rtype: bool
        """
        if len(self.active) == 0:
            for player in self.players:
                player.receive_game_end(self.dead)

            return False

        for player in self.players:
            player.receive_gamestate(
                self.board.readonly(),
                self.player_states[player],
                self.players,
            )

        self._change_player_turn()
        self._give_player_tiles(self.turn)

        # prompt the player for their next move, submit it if valid
        next_move = self._ask_for_move()
        if next_move is not None:
            self._submit_move(next_move)
            self._update_player_states()

        return True

    def add_placements(self, placements: List[Placement]):
        """
        Adds placements manually, from a test harness.
        """
        for placement in placements:
            self._submit_move(placement)

    def _assign_turn_order(self):
        """Assigns turn order, initializes turn index, sets round number."""
        self.turn_order: List[Player] = sorted(self.players, key=attrgetter("age"))
        # turn index and round are both negative when the game hasn't started
        self.turn_index, self.round = -1, -1

    def _assign_colors(self):
        """Assigns players a color by their turn order."""
        self.players_by_color: Dict[Color, Player] = {}
        for color, player in zip(Color, self.turn_order):
            if player.color is not None:
                self.players_by_color[player.color] = player
                continue
            player.receive_color(color)
            self.players_by_color[color] = player

    def _initialize(self):
        """Initializes instance variables."""
        # list of players still active in the game
        self.active: List[Player] = self.players.copy()
        self.player_states: Dict[Player, PlayerState] = {
            p: PlayerState.ALIVE for p in self.players
        }
        # players that died in each round and the reasons
        self.dead: DefaultDict[int, List[Tuple[Player, PlayerState]]] = defaultdict(list)
        # card indices valid for the current turn, assigned to each player
        self.player_cards: DefaultDict[Player, List[int]] = defaultdict(list)
        # a set of player starting positions, for detecting collisions
        self.start_positions: Set[Tuple[Tile, Port]] = set()
        # the game board
        self.board = Board()
        # the number of tiles to give the player on each turn
        self.tile_hand_amount = 3
        # the ne
        self.next_tile_index = 0

    def _change_player_turn(self):
        """
        Changes the turn.

        Skips any dead players. Assumes at least one player is not dead.
        """
        self._increment_turn()
        current_round = self.round

        # if the next player in the turn order has died, skip them
        while self.turn not in self.active:
            self._increment_turn()

    def _give_player_tiles(self, player: Player):
        """Gives the player whose turn it is their hand."""
        new_hand_indices = []
        for i in range(self.tile_hand_amount):
            new_hand_indices.append(self.next_tile_index)
            self.next_tile_index = (self.next_tile_index + 1) % Tile.NUMBER_OF_TILES

        self.player_cards[self.turn] = new_hand_indices
        self.turn.receive_tiles([Tile.Builder.build(i).readonly() for i in new_hand_indices])

    def _ask_for_move(self):
        """
        Prompts the player for their next move.

        Ejects the player if they request an illegal move.

        :return: the next move, if valid, otherwise, `None`
        :rtype: Optional[Placement]
        """
        next_move = self.turn.next_move()

        if next_move is None:
            self.turn.receive_move_failure("Did not submit a move")
            self._inactivate_player(self.turn, PlayerState.EJECTED)
            return None

        if next_move.index not in self.player_cards[self.turn]:
            # ejects player from game for playing a tile not in their hand
            self.turn.receive_move_failure("Played a tile not found in hand")
            self._inactivate_player(self.turn, PlayerState.EJECTED)
            return None

        for rule in self.rules:
            is_valid, message = rule.is_valid(next_move, self.board.readonly(), self.turn)
            if not is_valid:
                # ejects player from game for an illegal move
                self.turn.receive_move_failure(message)
                self._inactivate_player(self.turn, PlayerState.EJECTED)
                return None

        return next_move

    def _submit_move(self, next_move: Placement):
        """Submits the player's next move to the board."""
        tile = next_move.build_tile()
        self.board.add_tile(tile, next_move.x, next_move.y)
        self.turn.receive_move_success()

        player = self.players_by_color[next_move.color]
        player.tile = tile
        if next_move.is_initial:
            self.start_positions.add((tile, next_move.port))
            player.port = tile.get_exit_port(next_move.port)
        else:
            player.port = tile.get_exit_port(player.port.neighbor)

    def _increment_turn(self):
        """
        Increments the turn index.

        When the end of the turn order has been reached, resets the index to 0
        and increments the round number. After the first round, decreases the
        number of tiles in the player's hand to 2.
        """
        self.turn_index = (self.turn_index + 1) % len(self.players)

        if self.turn_index == 0:
            self.round += 1

        if self.round == 1:
            self.tile_hand_amount = 2

    def _inactivate_player(self, player, reason):
        """Removes players from the game for the given reason."""
        self.active = [p for p in self.active if p is not player]
        self.dead[self.round].append((player, reason))

    def _update_player_states(self):
        """Updates the states of all active players."""
        for player in self.active:
            state = self._get_player_state(player)
            self.player_states[player] = state
            if state is not PlayerState.ALIVE:
                self._inactivate_player(player, state)

    def _get_player_state(self, player: Player):
        """
        Determines the state of the given player in the game.

        :return: the state of the player
        :rtype: PlayerState
        """
        # short-circuit if the player hasn't made their first move, yet
        if player.tile is None:
            return PlayerState.ALIVE

        adjacent = self.board.get_tile_at(
            *get_coordinates_in_direction(player.tile.x, player.tile.y, player.port.direction)
        )

        if adjacent is not None and adjacent is not OutOfBounds:
            # advance the player onto the adjacent tile and recur
            player.tile = adjacent
            player.port = adjacent.get_exit_port(player.port.neighbor)
            return self._get_player_state(player)

        elif adjacent is OutOfBounds:
            death_tile = (player.tile, player.port)

            if death_tile in self.start_positions:
                # a player has collided if they end at another's start position
                return PlayerState.COLLIDED

            return PlayerState.DEAD

        elif adjacent is None:
            return PlayerState.ALIVE
