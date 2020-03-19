# Player Interface

The player interface represents the player in the Tsuro game.

# Fields

- Player location - the current location of the player, what port the player's avatar is on
- Board state - the board grid, where tiles are placed and what spots are empty
- Opponent locations - a list of locations where enemy players are located
- Tiles - what tiles the player has currently available
- Is game over - boolean saying whether or not the game is over
- WL record - what the player's win loss record is
- Is player dead - boolean saying whether or not the player is dead i.e. off the board or collided with another player
- Is player's turn - boolean indicating if it's the current player's turn

# Methods

- place_tile(location, orientation) - places a tile at a given location with a given orientation
- get_board_state() - gets the current state from the board class
- get_opponent_locations() - gets the current locations of the enemy players
- get_new_tile() - requests a new tile from the referee to add to the player's playable tiles list
- determine_move() - determines what the player's next move will be by examining empty spaces and enemy locations, will then call place_tile()
- end_game() - ends the game for the player, changes booleans for game over to true and changes the players win loss record accordingly
