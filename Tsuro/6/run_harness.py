import json
import os
import subprocess
import sys
import time
from threading import Thread


PATH = os.path.join(os.path.dirname(__file__))
SERVER_IP = "127.0.0.1"
SERVER_PORT = "8000"


def start_server():
    subprocess.call([f"{PATH}/xserver"])


def start_client(name: str, strategy: str):
    subprocess.call([f"{PATH}/xclient", SERVER_PORT, SERVER_IP, name, strategy])


def run_game(names):
    server = Thread(target=start_server)
    clients = []
    for client in names:
        clients.append(Thread(target=start_client, args=(client["name"], client["strategy"])))

    server.start()
    time.sleep(3)
    for client in clients:
        client.start()

    server.join()
    for client in clients:
        client.join()


if __name__ == "__main__":
    try:
        names = json.loads(sys.stdin.read())
        run_game(names)
    except json.JSONDecodeError as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(code=1)
