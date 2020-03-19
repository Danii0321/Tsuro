import json
import re


NON_WHITESPACE_REGEX = re.compile(r"[^\s]")


class MultipleJSONDecodeError(Exception):
    """
    Exception indicating the index of the object with the decode error.
    """

    def __init__(self, msg, objno, pos):
        self.msg = msg
        self.objno = objno
        self.pos = pos

    def __str__(self):
        return f"{self.msg}: object {self.objno} char {self.pos}"


def load_multiple(input_string: str):
    """
    Decodes multiple JSON documents from one input string.
    """
    decoder = json.JSONDecoder()

    pos = 0
    object_count = 0

    while pos < len(input_string):
        # raw_decode expects character 0 to be the start of the JSON
        # document - so, find the next non-whitespace character
        match = NON_WHITESPACE_REGEX.search(input_string, pos)
        if not match:
            return  # exit if only whitespace remains
        pos = match.start()

        try:
            obj, pos = decoder.raw_decode(input_string, pos)
        except json.JSONDecodeError as e:
            raise MultipleJSONDecodeError(e.msg, object_count, e.pos)

        object_count += 1
        yield obj
