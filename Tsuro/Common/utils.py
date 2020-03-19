import json
import logging
import os
import sys

from Common.constants import Direction


log = logging.getLogger(__name__)


def get_or_default(l, index, default=None):
    if index < 0 or index >= len(l):
        return default

    return l[index]


def get_static_path(filename):
    """
    Returns the absolute path to a file relative to `static/`.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", filename))


def get_coordinates_in_direction(x, y, direction):
    if direction is Direction.NORTH:
        return (x, y - 1)
    elif direction is Direction.EAST:
        return (x + 1, y)
    elif direction is Direction.SOUTH:
        return (x, y + 1)
    elif direction is Direction.WEST:
        return (x - 1, y)


def revolve(size, clockwise):
    curr_x, curr_y = 0, 0
    if clockwise:
        for x_incr, y_incr in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            for i in range(size):
                yield curr_x, curr_y
                curr_x += x_incr
                curr_y += y_incr
    else:
        for y_incr, x_incr in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            for i in range(size):
                yield curr_x, curr_y
                curr_x += x_incr
                curr_y += y_incr


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        log.warning("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)
    return result


def process_input(input_str):
    log.info("Processing input received from the client")
    result = json.loads(input_str)
    return result
