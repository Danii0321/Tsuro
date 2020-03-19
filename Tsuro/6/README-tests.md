# 5

The `xrun` test harnesses accepts input from STDIN.

    ./xrun < ./run-tests/1.json

The `xserver` and `xclient` can be run independently. By default, the server binds to `127.0.0.1:8000`, but the address and port can be specified.

    ./xserver [-h] [port] [ip]

The client requires specifying the address and port to bind to as well as the name of the player and its strategy.

    ./xclient [-h] port ip name {dumb,second}
