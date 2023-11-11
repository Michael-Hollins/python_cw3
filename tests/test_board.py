import unittest
import sys
sys.path.append("../")
from battleship.board import Board
from battleship.ship import Ship


class TestBoardMethods(unittest.TestCase):
    
    def test_out_of_bounds(self):
        ships = [
            Ship(start=(3, 1), end=(3, 5)),  
            Ship(start=(9, 8), end=(9, 11)), # out of bounds
            Ship(start=(1, 9), end=(3, 9)),  
            Ship(start=(5, 2), end=(6, 2)),  
            Ship(start=(8, 3), end=(8, 3)),  
        ]  
        self.assertRaises(ValueError, Board, ships)

    def test_ships_too_close(self):
        ships = [
            Ship(start=(3, 1), end=(3, 5)),  
            Ship(start=(4, 1), end=(4, 4)), # too close
            Ship(start=(1, 9), end=(3, 9)),  
            Ship(start=(5, 2), end=(6, 2)),  
            Ship(start=(8, 3), end=(8, 3)),  
        ] 
        self.assertRaises(ValueError, Board, ships)
        
    def test_devastating_barrage(self):
        ships = [
            Ship(start=(3, 1), end=(3, 5)),  
            Ship(start=(9, 7), end=(9, 10)),
            Ship(start=(1, 9), end=(3, 9)),  
            Ship(start=(5, 2), end=(6, 2)),  
            Ship(start=(8, 3), end=(8, 3)),  
        ]
        board = Board(ships=ships)
        for ship in board.ships:
            for cell in ship.get_cells():
                ship.receive_damage(cell)
        self.assertTrue(board.have_all_ships_sunk())
        
    
    # def test_board(self):
    #     ships = [
    #         Ship(start=(3, 1), end=(3, 5)),  # length = 5
    #         Ship(start=(9, 7), end=(9, 10)), # length = 4
    #         Ship(start=(1, 9), end=(3, 9)),  # length = 3
    #         Ship(start=(5, 2), end=(6, 2)),  # length = 2
    #         Ship(start=(8, 3), end=(8, 3)),  # length = 1
    #     ]
        
    #     board = Board(ships=ships)
    #     print(board.are_ships_within_bounds(ships))
    #     print(board.ships)
    #     is_ship_hit, has_ship_sunk = board.is_attacked_at((3, 4))
    #     print(is_ship_hit, has_ship_sunk)
    #     assert self.is_ship_hit == True
    #     assert self.has_ship_sunk == False


if __name__ == "__main__":
    unittest.main()