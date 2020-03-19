# Component Descriptions

**Automated players which can be provided by other people should know...**

- Where their piece or token is on the grid (token is represented by a color)
- Where opponent pieces are placed on the grid (info should be relayed from the game software)
- What tiles they have available to play (tiles can be rotated by 90, 180, 270 degrees, cards also have 8 ports 2 on each side of the card). They have a choice between 3 randomized tiles to begin with, and two each round provided by the game software.
- Where the current tiles are placed on the board (info should be relayed from the game software)
- Players should know what information needs to be rendered for the client (this information should be passed down from the "game software")
- Players should know their score and the score of their opponent (number of wins per player) - transmitted from game state

**Game software should know...**

- Which players are connected to the game software
- Information about current tournaments
- Which players are participating in which tournaments
- Past and present games in each tournament. For the past and present game(s), the software should know:
  - Which players are participating in the game (past and present)
  - The game state: if the game has been won, and if so, who has won and who has lost (past and present)
  - Whose turn it is to play (present only)
  - Who has which tiles, and which tiles are still available (present only)
  - Where all the tiles are placed on the board, and which ports on those tiles contain the players' tokens; the software should maintain the game's state and relay it to the players. (The board is made up of 10x10 spaces for tiles) (present only)
- Player ranking in each tournament
- The rules by which players advance to future games in each tournament
- The rules of the game, and maintain them across all players and games

**Communication**

Assuming that the game logic in "game software" is hosted on a server and the clients "automated players" connect to said server, the game software tells which players are going to be playing in the current game. It should then send the board and player locations to each of the players at the end of each turn and when the game is first started. The game software should also declare who's turn it is to play their card. At the beginning, the game generates three tiles for the player to choose from, and each other round it generates two. When it is the given players turn, the player should send a request to the game software server saying what tile they want placed, what rotation they want, and where the tile will be placed. It is then up to the game software server to validate the move according to the rules and execute the move if it is valid. The game server would then send an updated game state to all current players playing. The game server would keep track of who has won and who has lost and relay this information to the players. The game server holding the game state and ensuring valid moves and player position allows for more secure and fair games; where the player can't cheat by manipulating client side versions of the board so the game state doesn't match with other players. At the end of the game, the score of the players will be updated to reflect who has won, and the players will have the option to play another round.

# Implementation

In order to demo Tsuro as quickly as possible to potential clients, the following describes an implementation for a prototype of the application. In this initial version, only the core logic necessary for a working game is included. This specification will be refined iteratively through development or after conversations with the client. After a working prototype of the game logic is delivered, new features can be discussed and prioritized for addition to the project.

### Communication

A client/server protocol should be developed using a language of well-formatted JSON to send and receive information about the game state.

### Tile

##### Fields

An object with fields...
- has information about all of its ports (2 per side)
- has information about the connections between each port
- has information about its rotation

###### Methods

a tile can be rotated or added to the game at a certain position
- rotate_tile(), rotates tile 90, 180, or 270 degrees


### Players

##### Fields

Players should be implemented as a class or object. This object would contain information critical to determining the players next move. The player would have fields that are constantly being updated by the game server at the end of each turn played by a player. The fields would consist of...

- Our player position (posn)
- The tiles they have to choose from each round (list of Tile objects) - sent from the game software
- The move they have selected (a Tile object with chosen rotation and position)
- If they choose to play another round (boolean), at the end of the game the user chooses if they want to continue.

Our player object would then use this information to develop the next move and send this move to the server. Ideally the move would send which card the player is playing in what orientation and in what grid spot to the server.

###### Methods
- get_position(), returns the position of this player at the given moment, used by game software to track players
- choose_tile(), given a list of tiles from the game, the user selects one. They can then rotate the tile and choose where to place it.
- continue_game(), when a game is finished, players can choose if they want to continue playing

### Game Software

##### Fields

The game software should be a class or object that holds all the game logic. The game software object should hold the state of the board and the information of the players to pass on to them later. The fields would consist of...
- For each active game...
   - The board grid, where tiles are placed and where empty spaces are, and the position of all the players (graph).
   - List of players (list of Player objects).
   - Which player's turn (Player) The first player to connect is the first to go then it's the next player to connects turn
   - After each player makes a move, checks if their move is valid and if so the game state (the board grid) is updated.
   - Is the player still "alive"? (boolean), is the player on the board? If not, updates game over boolean to true.
   - Is the game over? (boolean), in this case the game would find which player has won and update the score accordingly.
   - Score of the tournament (dictionary with players and their win loss). This would be preserved and updated after starting a new round.

###### Methods

- initiate_game() Game should be started with an empty board and the players on the edge. Called at the start of the first game and at the start of each new Game.
- get_players(), returns the list of Players in this game.
- get_current_game_state(), Returns most recent game state.
- which_players_turn() returns the Player whose turn it is.
- get_new_tiles(), called each turn to get a list of tiles to provide the player to choose from.
- check_valid_move(), validates that the player's chosen movement is valid.
- update_game_state(), updates board grid according to the most recent valid move. tile is placed and player's token is moved.
- player_on_board(), returns boolean to tell if the player is still playing after their move (are they still on board)?
- is_game_over(), Game ends when there is one player left on the board. There can be ties if multiple players leave the board in the same turn.
- update_score(), updates each player's score if a game is ended and there is a winner.
- get_current_scores(), returns the score of each player.
- end_game(), removes players if they choose not to play any more games after one is completed.
