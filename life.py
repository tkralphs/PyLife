'''
life.py
Simulates John Conway's Game of Life with random initial states
This is the original version using a dictionary to store the board.

Original code here:
http://www.daniweb.com/software-development/python/code/217028
Modified by Ted Ralphs and Aykut Bulut, January 2012
Second edit February 2013
Updated again January 2014
'''

__version__    = '1.0.0'
__author__     = 'G-Do (http://www.daniweb.com/members/G-Do/37720)'
__maintainer__ = 'Ted Ralphs'
__email__      = 'ted@lehigh.edu'
__url__        = 'http://coral.ie.lehigh.edu/~ted/files/ie172/code/life.py'
__title__      = 'The Game of Life'
__license__    = 'CC BY 3.0'

from  sys import argv, exit
import random, pygame
from pygame.locals import *
from time import time
import cProfile, pstats
#import pycallgraph

# GLOBALS
# The dimensions of each cell (in pixels)
CELL_DIMENSIONS = (5,5)
# The framerate of the game (in milliseconds)
FRAMERATE = 60
# The fraction of the board occupied by cells when randomly generated
OCCUPANCY = 0.25
# Colors used to represent the cells
COLORS = { 0:(0,0,0), 1:(200,200,100) }
NEIGHBORS = [(0,1),   # up
             (0,-1),  # down
             (1,0),   # left
             (-1,0),  # right
             (1,1),   # upper left
             (-1,1),  # upper right
             (-1,-1), # lower right
             (1,-1),  # lower left
            ]
# Board marks
DEAD = 0
ALIVE = 1
WILL_BORN = 2
WILL_DIE = -1

def life(dimx, dimy, iteration_limit = 10000):
    '''
    Simulates game of life for iteration_limit many iterations.
    Inputs:
        dimx: number of cells in x dimension
        dimy: number of cells in y dimension
        iteration_limit: iteration limit
    Return:
        Returns average time spend in update_board() method.
    '''
    # Initialize pygame elements
    screen, bg, clock = init(dimx, dimy)
    # Create random board
    board = make_random_board(dimx, dimy)
    # Enter the game loop
    quit_game = False
    counter, timing = 0, 0
    while not quit_game and counter <= iteration_limit:
        # Slow things down to match the framerate
        clock.tick(FRAMERATE)
        # Update the board
        start = time()
        update_board(board)
        timing += time() - start
        # Draw the board on the background
        draw_board(board, bg)
        # Blit bg to the screen, flip display buffers
        screen.blit(bg, (0,0))
        pygame.display.flip()
        # Queue user input to catch QUIT signals
        for e in pygame.event.get():
            if e.type == QUIT: quit_game = True
        counter += 1
    return timing/counter

def init(dimx, dimy):
    '''
    Initializes pygame elements.
    Inputs:
        dimx: number of cells in x dimension
        dimy: number of cells in y dimension
    Return:
        (screen, bg, clock): pygame elements that enables to draw board on the
                             screen
    '''
    # Initialize the pygame modules
    pygame.init()
    # Determine and set the screen dimensions
    dimensions = (dimx*CELL_DIMENSIONS[0],
                  dimy*CELL_DIMENSIONS[1])
    screen = pygame.display.set_mode(dimensions)
    # Set the title string of the root window
    pygame.display.set_caption(__title__+" "+__version__)
    # Grab the background surface of the screen
    bg = screen.convert()
    # Grab the game clock
    clock = pygame.time.Clock()
    # Return the screen, the background surface, and the game clock
    return screen, bg, clock

def make_random_board(dimx, dimy):
    '''
    Creates initial board.
    Inputs:
        dimx: number of cells in x dimension
        dimy: number of cells in y dimension
    Return:
        board: board, type of dictionary. Keys are tuple of coordinates (x,y)
    '''
    # Instantiate the board as a dictionary with a fraction occupied
    board = {}
    for x in range(dimx):
        for y in range(dimy):
            if random.random() < OCCUPANCY: board[(x,y)] = ALIVE
            else: board[(x,y)] = DEAD
    # Return the board
    return board

def update_board(board):
    '''
    Update the board according to the rules of the game
    Input:
        board: current board.
    Post:
        Updates board.
    '''
    # For every cell in the board...
    for cell in board:
        # How many occupied neighbors does this cell have?
        neighbors = count_neighbors(cell, board)
        # If the cell is empty and has 3 neighbors, mark it for occupation
        if board[cell] == DEAD and neighbors == 3:
            board[cell] = WILL_BORN
        # On the other hand, if the cell is occupied and doesn't have 2 or 3
        # neighbors, mark it for death
        elif board[cell] == ALIVE and not neighbors in [2, 3]:
            board[cell] = WILL_DIE

    # Now, go through it again, making all the approved changes
    for cell in board:
        if board[cell] == WILL_BORN: board[cell] = ALIVE
        if board[cell] == WILL_DIE: board[cell] = DEAD

def count_neighbors(cell, board):
    '''
    Return the number of occupied neighbors of cell.
    Inputs:
        cell: cell that we will count neighbors.
        board: game board.
    '''
    # For each potential neighbor, if the cell is occupied add one to the score
    score = 0
    for n in NEIGHBORS:
        # Is this a real neighbor, or is it out-of-bounds?
        if (cell[0] + n[0], cell[1] + n[1]) in board.keys():
            # Remember that neighbors which are marked for death count, too!
            if board[(cell[0] + n[0], cell[1] + n[1])] in [ALIVE, WILL_DIE]: 
                score += 1
    # Return the score
    return score

def draw_board(board, bg):
    '''
    Draw the board on the background.
    Inputs:
        board: game board.
        bg: background, pygame related object.
    '''
    # Grab hard-coded global values
    global CELL_DIMENSIONS
    # Draw every cell in the board as a rectangle on the screen
    for cell in board:
        rectangle = (cell[0]*CELL_DIMENSIONS[0],cell[1]*CELL_DIMENSIONS[1],
                     CELL_DIMENSIONS[0],CELL_DIMENSIONS[1])
        pygame.draw.rect(bg, COLORS[board[cell]], rectangle)

if __name__ == "__main__": 
    if len(argv) != 3 and len(argv) != 1: 
        exit("USAGE: life.py X_CELLS Y_CELLS")
    
    if len(argv) == 3:
        life(int(argv[1]), int(argv[2]))
    else:
        cProfile.run('life(100, 100, 10)', 'cprof.out')
        p = pstats.Stats('cprof.out')
        p.sort_stats('cumulative').print_stats(10)
