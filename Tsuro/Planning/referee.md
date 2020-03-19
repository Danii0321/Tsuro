# Referee Interface

This is a representation of the referee or game state manager. The referee should keep track of all elements of the game to enforce the rules and the state of the game. It should pass copies of the objects down to players so they can determine their moves without cheating by mutating the board. Players should request moves to the referee. The referee should then use the rules implementation to check and validate the move. If the move is valid the referee should execute the move and update the board. It should then pass the updated board and game state (positions, tiles, W/L records, game over) to the players.

# Fields

- Players - The referee should keep track of player information to validate with rule checker, how the referee keeps track of player information is up to the implementer.
  - Location
  - Record (W/L)
  - Tiles
  - Player's turn - which player's turn it is to place a tile
  - Turn order - the order in which the player's place tiles
- Board - the state of the board, where tiles are placed
- Is game over
- Rule checker - the current set of rules

# Methods

- update_players() - should update all the player's information
  - give_players_board() - gives the player a copy of the current board so they can't mutate the board and cheat
  - give_players_positions() - gives the players the locations of other players
  - give_player_tile() - give a player a new tile
  - update_turn() - tells which player's turn it is
  - update_record() - updates the player's records (W/L)
- validate_move() - calls the rules validate move to validate a player's requested move
- execute_move() - after the move is validated execute_move() should play the move and place the tile and change the board i.e. move the player and place the tile. The played tile should also be removed from the player's list of tiles.
- change_players_turn() - changes the current player whose turn it is to the next player in the list
- eliminate_player() - if a player makes an illegal move or a player is dead the player is eliminated and removed from the game
- end_game() - ends the game
