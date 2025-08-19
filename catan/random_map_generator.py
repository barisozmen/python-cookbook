# https://chatgpt.com/share/68a40488-7bac-8010-936b-947515a13172
# https://en.wikipedia.org/wiki/Catan

import random

# Standard Catan number tokens (without desert)
TOKENS = [2, 3, 3, 4, 4, 5, 5, 6, 6, 
          8, 8, 9, 9, 10, 10, 11, 11, 12]

# Adjacency list for the 19-hexagon Catan layout
# Indexing from top-left to bottom-right
ADJACENCY = {
    0: [1, 3, 4],
    1: [0, 2, 4, 5],
    2: [1, 5, 6],
    3: [0, 4, 7, 8],
    4: [0, 1, 3, 5, 8, 9],
    5: [1, 2, 4, 6, 9, 10],
    6: [2, 5, 10, 11],
    7: [3, 8, 12],
    8: [3, 4, 7, 9, 12, 13],
    9: [4, 5, 8, 10, 13, 14],
    10: [5, 6, 9, 11, 14, 15],
    11: [6, 10, 15],
    12: [7, 8, 13, 16],
    13: [8, 9, 12, 14, 16, 17],
    14: [9, 10, 13, 15, 17, 18],
    15: [10, 11, 14, 18],
    16: [12, 13, 17],
    17: [13, 14, 16, 18],
    18: [14, 15, 17]
}

def is_valid(arrangement):
    """Check if no two 6s or 8s are neighbors."""
    for i, token in enumerate(arrangement):
        if token in (6, 8):
            for neighbor in ADJACENCY[i]:
                if arrangement[neighbor] in (6, 8):
                    return False
    return True

def generate_board():
    """Generate a valid random Catan number arrangement."""
    while True:
        arrangement = TOKENS[:] + ["D"]  # add desert (D)
        random.shuffle(arrangement)
        if is_valid(arrangement):
            return arrangement

# Generate a few valid boards
boards = [generate_board() for _ in range(3)]

print(boards)
# [9, 12, 6, 8, 5, 11, 3, D, 2, 6, 4, 10, 4, 9, 3, 11, 5, 10, 8]
# [8, D, 11, 9, 2, 3, 3, 12, 10, 11, 4, 6, 4, 6, 10, 5, 5, 9, 8]
# [10, 8, 11, 5, D, 10, 3, 12, 6, 9, 3, 4, 11, 2, 5, 9, 6, 4, 8]
