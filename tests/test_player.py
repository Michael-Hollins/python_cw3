import unittest
import random
import sys
sys.path.append("../")
from battleship.player import RandomPlayer
from battleship.board import Board

board=Board()

tracker = set()
moves = list()
attack_successful = False
ship_being_attacked = list()

width = board.width
height = board.height

cell = (9,0)

def is_valid_target(cell):
    """ Checks if a cell lies within the board """
    x_min = 1
    y_min = 1
    x_max = board.width
    y_max = board.height        
    x = cell[0]
    y = cell[1]        
    return (x_min <= x <= x_max and y_min <= y <= y_max)

cells_to_test = list(zip(range(0,12), range(0,12)))
for cell in cells_to_test:
    tracker.add(cell)
    
def cell_unvisited(cell):
    return cell not in tracker

cell = (9,9)
print(cell_unvisited(cell))    
