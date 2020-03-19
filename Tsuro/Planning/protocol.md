# Message Definitions

The client and server communicate by sending messages over a TCP socket. Every message is a JSON object containing at least the key `type`. This key specifies the type of message, which defines the expected structure.

Below follows definitions for each message type.

## Server Messages

**ASK_FOR_PLAYER_INFO**

Sent when a client has connected to the server to received the client's name and strategy and the
client is connected to the game.

    {
      "type": "ASK_FOR_PLAYER_INFO"
    }

**RECEIVE_COLOR**

Sent when a client been assigned a color by the server.

    {
      "type": "RECEIVE_COLOR",
      "color": "white"
    }

**ASK_FOR_MOVE**

Sent to prompt the player for their move. Provides the current gamestate
and the player's hand.

    {
      "type": "ASK_FOR_MOVE",
      "board": [
        [TILE-OR-NULL, ...], ...
      ],
      "tiles": [TILE-OR-NULL, TILE-OR-NULL, TILE-OR-NULL?]
    }

Where `TILE-OR-NULL` is one of `null` or:

    {"index": 0, "rotation": 90, "x": 1, "y": 1}

**MOVE_ACCEPTED**

Sent when the player's move is accepted.

    {
      "type": "MOVE_ACCEPTED"
    }

**EJECTED**

Sent when the client has been ejected from the game for making an illegal
move.

    {
      "type": "EJECTED",
      "reason": "First move must be on the border."
    }

**GAME_END**

Sent when the game ends, includes the ranking of winners and any losers.

    {
      "type": "GAME_END",
      "results": {
        0: [(PLAYER, PLAYER-STATE), ...],
        ...
      }
    }

Where `PLAYER` is:

    {
        "color": self.color,
        "tile": {"index": 0, "rotation": 90, "x": 1, "y": 1}
        "port": "H",
        "state": "ALIVE"
    }

and `PLAYER-STATE` is one of `ALIVE`, `DEAD`, `COLLIDED`, `EJECTED`.

## Client Messages

**JOIN**

Sent by the player to inform the server of its name and desired strategy.

    {
      "type": "JOIN",
      "name": "player one",
      "strategy": "dumb"
    }

**MOVE_REQUEST**

Sent to inform the server of the requested move. Placement type is one of
`INITIAL` or `INTERMEDIATE` and `port` is required when the placement type is
`INITIAL`.

Initial placement:

    {
      "type": "MOVE_REQUEST",
      "placement_type": "INITIAL"
      "index": 10,
      "rotation": 90,
      "color": "red",
      "x": 0,
      "y": 0,
      "port": "A"
    }

Intermediate placement:

    {
      "type": "MOVE_REQUEST",
      "placement_type": "INTERMEDIATE"
      "index": 10,
      "rotation": 90,
      "color": "red",
      "x": 0,
      "y": 0,
    }

Protocol Definition:

               Server                        Client                        User
    +------------+------------------------------+---------------------------+
    |                         PER CONNECTING CLIENT                         |
    |------------+------------------------------+---------------------------+
    | CONNECT    |                              |                           |
    |            |                              |<--------------------------| Start client with
    |            |                              |                           | name and strategy
    |            | Open TCP conn.               |                           |
    |            |<-----------------------------|                           |
    |            |                              |                           |
    |            | Send ASK_FOR_PLAYER_INFO     |                           |
    |            |=============================>|                           |
    |            |                              |                           |
    |            | Send JOIN                    |                           |
    |            |<-----------------------------|                           |
    |            |                              |                           |
    +------------+------------------------------+---------------------------+
    |                         WAIT FOR ALL PLAYERS                          |
    |                             OR 30s, THEN                              |
    |                      TO ALL AT THE START OF GAME                      |
    |------------+------------------------------+---------------------------+
    |            |                              |                           |
    |            | Send RECEIVE_COLOR to all    |                           |
    |            |=============================>|                           |
    |            |                              |                           |
    +------------+------------------------------+---------------------------+
    |                     TO ALL AT THE START OF THE TURN                   |
    |------------+------------------------------+---------------------------+
    |            |                              |                           |
    |            | Send RECEIVE_GAME_STATE      |                           |
    |            |=============================>|                           |
    |            |                              |                           |
    +------------+------------------------------+---------------------------+
    |                 TO THE PLAYER WITH THE CURRENT TURN                   |
    |------------+------------------------------+---------------------------+
    |            |                              |                           |
    |            | Send ASK_FOR_MOVE            |                           |
    |            |=============================>|                           |
    |            |                              |                           |
    |            | Send MOVE_REQUEST            |                           |
    |            |<-----------------------------|                           |
    |            |                              |                           |
    |            | Send MOVE_ACCEPTED, or       |                           |
    |            | EJECTED and close conn       |                           |
    |            |=============================>|                           |
    |            |                              |                           |
    +------------+------------------------------+---------------------------+
    |                        AT THE END OF THE GAME                         |
    |------------+------------------------------+---------------------------+
    |            |                              |                           |
    |            | Send GAME_END                |                           |
    |            |=============================>|                           |
    |            |                              |                           |
    +------------+------------------------------+---------------------------+

If at any point, the server receives an invalid message from the client, it
will eject the client and send a final EJECTED message. If at any point, the
client receives an invalid message from the server, it will skip the message
and await the next one.
