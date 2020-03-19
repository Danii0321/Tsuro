import aggdraw
from PIL import Image, ImageFont

from Common.constants import Color
from Common.tiles import Connection, Port, Tile


# constants
WIDTH = 100  # tile width
HEIGHT = 100  # tile height
MARGIN = 2  # margin of border from tile edge
PORT_RADIUS = 2  # size of each port

# calculated values
CENTER = (WIDTH / 2, HEIGHT / 2)
BORDER = (MARGIN, MARGIN, WIDTH - MARGIN, HEIGHT - MARGIN)


def bounding_box(x, y, r):
    """Converts x, y and radius to bounding box."""
    return (x - r, y - r, x + r, y + r)


def port_location(port):
    """Given a port, returns its relative location on a tile in pixels."""
    n_thirds_width = lambda n: (WIDTH - 2 * MARGIN) / 3 * n
    n_thirds_height = lambda n: (HEIGHT - 2 * MARGIN) / 3 * n

    if port is Port.A:
        return (n_thirds_width(1), MARGIN)
    if port is Port.B:
        return (n_thirds_width(2), MARGIN)
    if port is Port.C:
        return (WIDTH - MARGIN, n_thirds_height(1))
    if port is Port.D:
        return (WIDTH - MARGIN, n_thirds_height(2))
    if port is Port.E:
        return (n_thirds_width(2), HEIGHT - MARGIN)
    if port is Port.F:
        return (n_thirds_width(1), HEIGHT - MARGIN)
    if port is Port.G:
        return (MARGIN, n_thirds_height(2))
    if port is Port.H:
        return (MARGIN, n_thirds_height(1))


def draw_base(im):
    """Draws the border and the ports."""
    draw = aggdraw.Draw(im)
    pen = aggdraw.Pen("black", 0.5)
    brush = aggdraw.Brush("black")

    draw.rectangle(BORDER, pen)

    bb = lambda xy: bounding_box(*xy, PORT_RADIUS)
    for port in Port:
        draw.ellipse(bb(port_location(port)), pen, brush)
    draw.flush()


def draw_connections(im, connections):
    """Draws the connections."""
    draw = aggdraw.Draw(im)
    pen = aggdraw.Pen("black", 0.5)

    for c in connections:
        xy1 = port_location(c.port1)
        xy2 = port_location(c.port2)

        path = aggdraw.Path()
        path.moveto(*xy1)
        path.curveto(*xy1, *CENTER, *xy2)

        draw.path(path, pen)

    draw.flush()


def draw_tile(tile, player):
    """Draws the tile."""
    # print("reached real tile")
    im = Image.new("RGBA", (WIDTH, HEIGHT), "white")
    draw_base(im)
    draw_connections(im, tile.connections)
    if player is not None:
        draw_token(im, player)
    return im


def draw_empty_space():
    # print("reached")
    im = Image.new("RGBA", (WIDTH, HEIGHT), "white")
    draw = aggdraw.Draw(im)
    pen = aggdraw.Pen("black", 0.5)
    draw.rectangle(BORDER, pen)
    draw.flush()
    return im


# passed a player and a color
def draw_token(im, player):
    # where im is the already-rendered tile
    draw = aggdraw.Draw(im)
    # print("Has a player")
    # tuple with x and y coords of the point
    c = get_color(player.color)
    pen = aggdraw.Pen("black", 0.5)  # draw border
    brush = aggdraw.Brush(c)  # fill
    # print(port_location(player.port))
    # print(isinstance(player.color, str))

    bb = lambda xy: bounding_box(*xy, PORT_RADIUS + 5)
    draw.ellipse(bb(port_location(player.port)), pen, brush)
    draw.flush()


def get_color(color):
    if color == Color.GREEN:
        return "green"
    if color == Color.BLUE:
        return "blue"
    if color == Color.WHITE:
        return "white"
    if color == Color.BLACK:
        return "black"
    if color == Color.RED:
        return "red"


def draw_turn(player):
    tile = player.next_move().build_tile()
    tile_im = draw_tile(tile, None)

    im = Image.new("RGBA", (100, 150), "white")
    im.paste(tile_im, (0, 50))
    draw = aggdraw.Draw(im)
    c = get_color(player.color)
    pen = aggdraw.Pen("black", 0.5)
    brush = aggdraw.Brush(c)

    draw.rectangle([0, 0, 150, 50], pen, brush)
    draw.flush()
    return im


if __name__ == "__main__":
    # with premade tile
    t = Tile.Builder.build(2)
    img = draw_tile(t)
    img.show()

    # with the actual structure- passed a generic tile w no connections yet
    # img = draw_empty_space()
    # img.show()

   
