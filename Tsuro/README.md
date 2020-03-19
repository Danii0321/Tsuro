# Tsuro

## Submissions

Phase 6 - [04fb4fc](https://github.ccs.neu.edu/cs4500-fall2019-neu/418-IM-A-TEAPOT/commit/04fb4fc61b72af7dc3a7b9a3998cf1259dc68894)  
Phase 5 - [a4f3e57](https://github.ccs.neu.edu/cs4500-fall2019-neu/418-IM-A-TEAPOT/commit/a4f3e576dc355e3713397d3538054866fc720b9e)  
Phase 4 - [1211a9e](https://github.ccs.neu.edu/cs4500-fall2019-neu/418-IM-A-TEAPOT/commit/1211a9e7dd227e643b2511bd545d9815cadda443)  
Phase 3 - [5e68237](https://github.ccs.neu.edu/cs4500-fall2019-neu/418-IM-A-TEAPOT/commit/5e68237f379c4872f76363624b3d4f042999bafb)  
Phase 2 - [4e4ff0e](https://github.ccs.neu.edu/cs4500-fall2019-neu/418-IM-A-TEAPOT/commit/4e4ff0e5834ea407b345cb183e2e3a968d85c379)  
Phase 1B - [9e77bc3](https://github.ccs.neu.edu/cs4500-fall2019-neu/418-IM-A-TEAPOT/commit/9e77bc39b4e6966138fe986a0c71b5500988f637)  
Phase 1A - [e5eab61](https://github.ccs.neu.edu/cs4500-fall2019-neu/418-IM-A-TEAPOT/commit/e5eab61df32070b4fcb8be84127bea6d0a9bbeb4)  

## Installation

Optionally, create a virtual environment first:

    python3 -m venv /path/to/venv
    source /path/to/venv/bin/activate

Then, to install dependencies, run:

    pip3 install -r requirements/dev.txt

## Testing

Run:

    python3 -m unittest

## Linting

Run:

    black --config pyproject.toml .
    isort -y .
    flake8 --config=setup.cfg .
