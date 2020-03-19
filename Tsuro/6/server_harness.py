import argparse
import sys

from Remote import server


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, nargs="?", default=8000, help="the port to connect to")
    parser.add_argument(
        "ip", type=str, nargs="?", default="127.0.0.1", help="the ip address to connect to"
    )
    args = parser.parse_args(args)
    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    server.start_server(args.ip, args.port)
