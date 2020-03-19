from Common.board import *
from Common.render import *
from Common.tiles import *


"""
Observer is responsible for rendering the state of the game. This includes the game board,
displaying which player's turn it is, and showing that player's current hand.
"""


# renders the state of the board given the board and its players
def render_board(board, players, turn=None):
    # grid is a 2d array, check at [x][y]
    size = board.SIZE * 100
    background = Image.new("RGBA", (size + 500, size), "lightgray")
    draw = aggdraw.Draw(background)

    count = 0
    for i in range(Board.SIZE):
        for j in range(Board.SIZE):
            obj_at = board.get_tile_at(i, j)
            # must check if the object at an x,y position is a tile or None
            if obj_at is None:
                count += 1
                # print("NONE - ")
                # print(count)
                img = draw_empty_space()
                draw = aggdraw.Draw(img)
            else:
                player = None
                for p in players:
                    if p.tile == obj_at:
                        player = p
                        break

                # else, if no players have this tile...
                img = draw_tile(obj_at, player)
                draw = aggdraw.Draw(img)

            background.paste(img, (i * 100, j * 100))

    if turn is not None:
        img2 = draw_turn(turn)
        player_hand = render_hand(turn)
        background.paste(img2, (1000, 0))
        background.paste(player_hand, (1000, 150))

    draw.flush()
    return background


# renders the hand of the player whose turn it is
def render_hand(player):
    hand = Image.new("RGBA", (300, 100), "lightgray")
    draw = aggdraw.Draw(hand)
    tilenum = 0
    for tile in player.tile_hand:
        img = draw_tile(tile, None)
        draw = aggdraw.Draw(img)
        hand.paste(img, (0, tilenum * 100))

    draw.flush()
    return hand
