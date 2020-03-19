# 5

The test harnesses accepts input from STDIN.

    ./xref < ./ref-tests/1.json
    ./xobs < ./obs-tests/test1


## xref

`xref` expects a single JSON array with the following format:

    [ String, ... ]

where each string in the array is a player name.

## xobs

`xobs` also expects a single JSON array as input, with one of the following formats:

    [ placement, placement, ... ]

    [ placement, placement, ..., [ intermediate-placement, tile-index, tile-index ] ]

    [ placement, placement, ..., [ initial-placement, tile-index, tile-index, tile-index ] ]

Where a `placement` is either an `initial-placement` or an `intermediate-placement`, and an `intermediate-placement` is:

    [ tile-index, rotation, color, x, y ]

and an `initial-placement` is:

    [ tile-index, rotation, color, x, y, port ]

as per the original Phase 3 specification.

### Output

The output of is an image of the board. If a final requested placement is specified, the requested tile is displayed in the topmost position to the right of the board, followed by the color of the player requesting the placement, followed by the other tiles in the player's hand.
