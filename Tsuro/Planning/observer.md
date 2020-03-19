# Observer Interface

The observer receives the game state and renders the tiles, board and players for the user.

# Fields
- The game state- This can be represented by the board, tiles and a list of players, exact implementation is up to the implementer. As long as these objects and there corresponding locations are known and relayed rendering the current game state shouldn't prove to be a problem.

# Methods
- render_tile(tile)- Renders a given tile image (examples can be found in 1/tile-1.png tile-2.png and tile-3.png)
- render_board()- renders the current game state board with the tiles, call render_tile for where each tile is present
- render_players()- renders each player on the corresponding port and tile in the game state