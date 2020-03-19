import argparse
import sys

from Remote import client


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help="the port to connect to")
    parser.add_argument("ip", type=str, help="the ip address to connect to")
    parser.add_argument("name", type=str, help="the name of the user")
    parser.add_argument(
        "strategy", type=str, choices=["dumb", "second"], help="the name of the strategy"
    )
    args = parser.parse_args(args)
    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    client.start_client(args.ip, args.port, args.name, args.strategy)
