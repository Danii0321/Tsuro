# 4

The test harness accepts input from STDIN.

    ./xrules < ./rules-tests/1.json

Example output is as follows:

    > echo '[
      [10, 0, "white", "A", 0, 0],
      [["white", 12, 90, 1, 0], 3, 4]
    ]' | ./xrules
    "legal"
