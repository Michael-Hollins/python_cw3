import unittest
import random
import sys
sys.path.append("../")

from battleship.ship import Ship
from battleship.ship import ShipFactory

class TestShipMethods(unittest.TestCase):

    def test_vertical(self):
        start = (2, 5)
        end = (2, 7)
        ship = Ship(start=start, end=end)
        output = ship.is_vertical()
        self.assertTrue(output)
    
    
    def test_horizontal(self):
        start = (4, 5)
        end = (2, 5)
        ship = Ship(start=start, end=end)
        output = ship.is_horizontal()
        self.assertTrue(output)
    
    
    def test_get_cells(self):
        start = (1, 1)
        end = (1, 6)
        ship = Ship(start=start, end=end)
        output = ship.get_cells()
        self.assertSetEqual(output, set({(1,1), (1,2), (1,3), (1,4), (1,5), (1,6)}))
      

    def test_length_1(self):
        start = (1, 1)
        end = (1, 4)
        ship = Ship(start=start, end=end)
        self.assertEqual(ship.length(), 4)
        
        
    def test_length_too_long(self):
        start = (9, 1)
        end = (3, 1)
        ship = Ship(start=start, end=end)
        self.assertIs(ship.length(), ValueError)
        
        
    def test_occupying_cell_1(self):
        start = (5, 1)
        end = (3, 1)
        ship = Ship(start=start, end=end)
        cell_to_check = tuple([4, 1])
        self.assertTrue(ship.is_occupying_cell(cell_to_check))
        
        
    def test_occupying_cell_2(self):
        start = (5, 1)
        end = (3, 1)
        ship = Ship(start=start, end=end)
        cell_to_check = tuple([1, 1])
        self.assertFalse(ship.is_occupying_cell(cell_to_check))
        
        
    def test_damage_1(self):
        start = (5, 1)
        end = (3, 1)
        ship = Ship(start=start, end=end)
        cell_attacked = tuple([3, 1])
        self.assertTrue(ship.receive_damage(cell_attacked))
        
        
    def test_damage_2(self):
        start = (5, 1)
        end = (3, 1)
        ship = Ship(start=start, end=end)
        cell_attacked = tuple([3, 1])
        ship.receive_damage(cell_attacked)
        empty_set = set()
        empty_set.add(cell_attacked)
        self.assertSetEqual(ship.damaged_cells, empty_set)
    
        
    def test_near_other_ship(self):
        start = (5, 1)
        end = (3, 1)
        ship = Ship(start=start, end=end)
        start = (2, 2)
        end = (5, 2)
        other_ship = Ship(start=start, end=end)
        self.assertTrue(ship.is_near_ship(other_ship=other_ship))
     
        
    def test_not_near_other_ship(self):
        start = (5, 1)
        end = (3, 1)
        ship = Ship(start=start, end=end)
        start = (4, 4)
        end = (4, 7)
        other_ship = Ship(start=start, end=end)
        self.assertFalse(ship.is_near_ship(other_ship=other_ship))
    
        
    def test_build_ship(self):
        for i in range(1000):
            ships = ShipFactory().generate_ships()
            random_idx = random.randint(0, len(ships)-1)
            ship_to_check = ships[random_idx]
            ships.remove(ship_to_check)
            self.assertFalse(any(ship_to_check.is_near_ship(other_ship) for other_ship in ships))
        
        
if __name__ == "__main__":
    unittest.main()