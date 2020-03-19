# Representation of the board

## Board class

The Board is a class that contains both fields with data relevant to the Players, and methods that control the flow of the game.

### Fields

- Grid: a 10 x 10 2D-array, represented by a nested list. The elements of the grid begin as None’s, which will be replaced with Tile objects during the game.
- List of players and positions: a dictionary where the key is a Player, and the value pairing is a fixed tuple of the Tile and the Port that the Player is positioned at.
- Turn: the Player that is to make the next move. This field is updated after a move is made by that Player to be the next Player in the order.
-	Round: what round the game is in. Represented by an integer, and updates after every Player has a turn.

### Methods

- initiate_game() - Game should be started with an empty (None’s) 10 x 10 grid and with the Players on the edge. 
- get_players() - returns the list of Players in this game.
- get_player_position() returns the position of a given player.
- get_current_game_state() - Returns state of the Board.
-	which_players_turn() - returns the Player whose turn it is.
-	get_round_number() – returns what round the game is in
-	give_tiles() – creates and distributes three Tiles to each Player in round one, and two Tiles for every subsequent round.
-	check_valid_move() - validates that the Player's chosen movement is valid.
-	update_game_state() - updates grid according to the most recent valid move. Tile is placed and Player's avatar is moved.
-	player_on_board() - returns bool of whether Player is still on the Board (in the game)
-	is_game_over() – returns a bool of whether game is over. Game is over if one Player left on the board, but there can be ties if multiple players leave the board in the same turn.
-	end_game() – ends a game without a Player needing to reach win condition.

