 # Inspired by https://github.com/norvig/pytudes/blob/main/ipynb/Life.ipynb
 
from collections     import Counter
import random
from typing          import Set, Tuple, Dict, Iterator, List
from itertools       import islice
from time            import sleep
import sys


Cell = Tuple[int, int]
AliveCells = Set[Cell]

def life(alive_cells, n=sys.maxsize):
    for _ in range(n):
        yield alive_cells
        alive_cells = next_generation(alive_cells)
        

def next_generation(alive_cells):
    return {
        cell
        for cell, count in neighbor_counts(alive_cells).items()
        if count == 3 or (cell in alive_cells and count == 2)
    }
    
def neighbor_counts(alive_cells):
    """A Counter of the number of live neighbors for each cell."""
    return Counter(neighbor for cell in alive_cells for neighbor in neighbors(cell))

def neighbors(cell):
    return {
        (cell[0] + dx, cell[1] + dy)
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        if (dx, dy) != (0, 0)
    }
    
def make_random_world(size, alive_probability=0.2):
    # Create a size x size world where each cell has a probability of alive_probability to be alive
    return {(x, y) for x in range(size) for y in range(size) if random.random() < alive_probability}

LIVE  = '@'
EMPTY = '.'
PAD   = ' '
def picture(world, Xs: range, Ys: range) -> str:
    """Return a picture of the world: a grid of characters representing the cells in this window."""
    def row(y): return PAD.join(LIVE if (x, y) in world else EMPTY for x in Xs)
    return '\n'.join(row(y) for y in Ys)
    

world = make_random_world(10, 0.2)

for _ in range(10):
    print(f'Generation {_}')
    print(picture(world, range(15), range(15)))
    world = next_generation(world)
    print('\n')
    
    
""" Output after running `python3 conways_game_of_life.py`

Generation 0
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . @ . @ . . . @ . . . . . .
. @ . @ . . @ . @ . . . . . .
@ . . @ . . . @ . @ . . . . .
@ . . . . . . . . . . . . . .
@ @ . . . . . . . . . . . . .
. . . @ . . . . . . . . . . .
. . . . @ . . . . . . . . . .
. . . . . . @ . . @ . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


Generation 1
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . @ @ . . . @ . . . . . . .
. @ . @ @ . . . @ @ . . . . .
@ @ @ . . . . @ @ . . . . . .
@ . . . . . . . . . . . . . .
@ @ . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


Generation 2
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . @ @ @ . . . @ . . . . . .
@ . . . @ . . . . @ . . . . .
. . @ @ . . . @ @ @ . . . . .
. . @ . . . . . . . . . . . .
@ @ . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


Generation 3
. . . . . . . . . . . . . . .
. . . @ . . . . . . . . . . .
. . . @ @ . . . . . . . . . .
. @ . . @ . . @ . @ . . . . .
@ @ @ @ . . . . @ @ . . . . .
. . @ @ . . . . @ . . . . . .
@ @ . . . . . . . . . . . . .
@ . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


Generation 4
. . . . . . . . . . . . . . .
. . . @ @ . . . . . . . . . .
. . @ @ @ . . . . . . . . . .
. @ . . @ . . . . @ . . . . .
. . . . @ . . @ . @ . . . . .
. . . @ . . . . @ @ . . . . .
. @ @ . . . . . . . . . . . .
@ @ . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


Generation 5
. . . . . . . . . . . . . . .
. . @ . @ . . . . . . . . . .
. . @ . . @ . . . . . . . . .
. . @ . @ @ . . @ . . . . . .
. . . @ @ . . . . @ @ . . . .
. . @ @ . . . . @ @ . . . . .
. @ @ . . . . . . . . . . . .
@ @ @ . . . . . . . . . . . .
@ . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


Generation 6
. . . . . . . . . . . . . . .
. . . @ . . . . . . . . . . .
. @ @ . . @ . . . . . . . . .
. . @ . . @ . . . @ . . . . .
. . . . . @ . . . . @ . . . .
. @ . . @ . . . @ @ @ . . . .
. . . . . . . . . . . . . . .
. . @ . . . . . . . . . . . .
@ . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


Generation 7
. . . . . . . . . . . . . . .
. . @ . . . . . . . . . . . .
. @ @ @ @ . . . . . . . . . .
. @ @ . @ @ @ . . . . . . . .
. . . . @ @ . . @ . @ . . . .
. . . . . . . . . @ @ . . . .
. . . . . . . . . @ . . . . .
@ . . . . . . . . . . . . . .
@ . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


Generation 8
. . . . . . . . . . . . . . .
. @ @ . . . . . . . . . . . .
. . . . @ . . . . . . . . . .
. @ . . . . @ . . . . . . . .
. . . @ @ . @ . . . @ . . . .
. . . . . . . . @ . @ . . . .
@ . . . . . . . . @ @ . . . .
@ . . . . . . . . . . . . . .
@ . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


Generation 9
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. @ @ . . . . . . . . . . . .
. . . @ @ . . . . . . . . . .
@ . . . . @ . @ . @ . . . . .
@ . . . . . . . . . @ @ . . .
@ . . . . . . . . @ @ . . . .
@ @ . . . . . . . . . . . . .
@ . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .


"""