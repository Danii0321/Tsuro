# Rules Interface

The Rules object will represent the referee of the game and enforce the rules of the game. It will make sure that player moves are valid and can be executed.

# Fields

- current_board, This field will be provided by the board. It will be the 2d list of tiles representing the board and where tiles are currently placed and which spots are empty.
- player_locations, This field will also be provided by the board. It will be some sort of list or map of players (implementation can vary). It should distinguish what players are still in the game and what their locations are.
- current_players_turn, Tells which players turn is up to execute a move
- is_game_over, is the game over

# Methods

Methods described show general functionality. Implementation can vary and some methods could encompass multiple functionalities described.

- is_move_valid(), checks if the move a player submits is valid and is able to be executed
- is_tile_on_board(), checks if the given move places a tile within the board boundaries 
- is_board_space_occupied(), checks if a current board space is occupied and if a tile can be placed
- is_tile_played_valid(), checks if the tile played is a valid tile that the player was given at some point in the game i.e the player has to have the current tile at the time of playing the tile
- is_tile_rotation_legal(), checks if a tile rotation is valid
- is_player_space_occupied(), checks if a port on the board is occupied by another player
- is_players_turn(), checks if the given player is the player who's turn it is to execute a move
- is_player_out_of_bounds(), checks if the player is out of bounds, thus ending the players game as a loss
- is_game_over(), checks if the game is over, i.e. are all the players off the board except one (winner)? Is there a tie (two players exit the board at the same time)?
- eject_player(), if a player is unresponsive or if they attempt to break the rules the player is ejected from the tournament