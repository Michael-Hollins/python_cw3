import random

from battleship.convert import CellConverter

class Ship:
    """ Represent a ship that is placed on the board.
    """
    def __init__(self, start, end, should_validate=True):
        """ Creates a ship given its start and end coordinates on the board. 
        
        The order of the cells do not matter.

        Args:
            start (tuple[int, int]): tuple of 2 positive integers representing
                the starting cell coordinates of the Ship on the board
            end (tuple[int, int]): tuple of 2 positive integers representing
                the ending cell coordinates of the Ship on the board
            should_validate (bool): should the constructor check whether the 
                given coordinates result in a horizontal or vertical ship? 
                Defaults to True.

        Raises:
            ValueError: if should_validate==True and 
                if the ship is neither horizontal nor vertical
        """
        # Start and end (x, y) cell coordinates of the ship
        self.x_start, self.y_start = start
        self.x_end, self.y_end = end

        # make x_start on left and x_end on right
        self.x_start, self.x_end = (
            min(self.x_start, self.x_end), max(self.x_start, self.x_end)
        )
        
        # make y_start on top and y_end on bottom
        self.y_start, self.y_end = (
            min(self.y_start, self.y_end), max(self.y_start, self.y_end)
        )
        
        if should_validate:
            if not self.is_horizontal() and not self.is_vertical():
                raise ValueError("The given coordinates are invalid. "
                    "The ship needs to be either horizontal or vertical.")

        # Set of all (x,y) cell coordinates that the ship occupies
        self.cells = self.get_cells()
        
        # Set of (x,y) cell coordinates of the ship that have been damaged
        self.damaged_cells = set()
    
    def __len__(self):
        return self.length()
        
    def __repr__(self):
        return (f"Ship(start=({self.x_start},{self.y_start}), "
            f"end=({self.x_end},{self.y_end}))")
        
    def is_vertical(self):
        """ Check whether the ship is vertical.
        
        Returns:
            bool : True if the ship is vertical. False otherwise.
        """
        return self.x_start == self.x_end
   
    def is_horizontal(self):
        """ Check whether the ship is horizontal.
        
        Returns:
            bool : True if the ship is horizontal. False otherwise.
        """
        return self.y_start == self.y_end
    
    def get_cells(self):
        """ Get the set of all cell coordinates that the ship occupies.
        
        For example, if the start cell is (3, 3) and end cell is (5, 3),
        then the method should return {(3, 3), (4, 3), (5, 3)}.
        
        This method is used in __init__() to initialise self.cells
        
        Returns:
            set[tuple] : Set of (x ,y) coordinates of all cells a ship occupies
        """
        if self.is_vertical():
          y_coords = list(range(self.y_start, self.y_end + 1))
          occupied_coords = [(self.x_start, y) for y in y_coords]
        else:
          x_coords = list(range(self.x_start, self.x_end + 1))
          occupied_coords = [(x, self.y_start) for x in x_coords]        
        return set(occupied_coords)

    def length(self):
        """ Get length of ship (the number of cells the ship occupies).
        
        Returns:
            int : The number of cells the ship occupies
        """
        x_coords = [item[0] for item in list(self.cells)]
        y_coords = [item[1] for item in list(self.cells)]
        x_domain = max(x_coords) - min(x_coords) + 1
        y_domain = max(y_coords) - min(y_coords) + 1
        length = max(x_domain, y_domain)
        if length > 5:
            return ValueError
        else:
            return length 

    def is_occupying_cell(self, cell):
        """ Check whether the ship is occupying a given cell

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to check

        Returns:
            bool : return True if the given cell is one of the cells occupied 
                by the ship. Otherwise, return False
        """
        return cell in self.cells
    
    def receive_damage(self, cell):
        """ Receive attack at given cell. 
        
        If ship occupies the cell, add the cell coordinates to the set of 
        damaged cells. Then return True. 
        
        Otherwise return False.

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the cell coordinates that is damaged

        Returns:
            bool : return True if the ship is occupying cell (ship is hit). 
                Return False otherwise.
        """
        if cell in self.cells:
            self.damaged_cells.add(cell)
            return True
        else:
            return False
    
    def count_damaged_cells(self):
        """ Count the number of cells that have been damaged.
        
        Returns:
            int : the number of cells that are damaged.
        """
        return len(self.damaged_cells)
        
    def has_sunk(self):
        """ Check whether the ship has sunk.
        
        Returns:
            bool : return True if the ship is damaged at all its positions. 
                Otherwise, return False
        """
        if self.length() == self.count_damaged_cells():
            return True
        else:
            return False
    
    def is_near_ship(self, other_ship):
        """ Check whether a ship is near another ship instance.
        
        Hint: Use the method is_near_cell(...) to complete this method.

        Args:
            other_ship (Ship): another Ship instance against which to compare

        Returns:
            bool : returns True if and only if the coordinate of other_ship is 
                near to this ship. Returns False otherwise.
        """
        for other_ship_cell in other_ship.cells:
            if self.is_near_cell(other_ship_cell):
                return True
        return False

    def is_near_cell(self, cell):
        """ Check whether the ship is near an (x,y) cell coordinate.

        In the example below:
        - There is a ship of length 3 represented by the letter S.
        - The positions 1, 2, 3 and 4 are near the ship
        - The positions 5 and 6 are NOT near the ship

        --------------------------
        |   |   |   |   | 3 |   |
        -------------------------
        |   | S | S | S | 4 | 5 |
        -------------------------
        | 1 |   | 2 |   |   |   |
        -------------------------
        |   |   | 6 |   |   |   |
        -------------------------

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to compare

        Returns:
            bool : returns True if and only if the (x, y) coordinate is at most
                one cell from any part of the ship OR is at the corner of the 
                ship. Returns False otherwise.
        """
        return (self.x_start-1 <= cell[0] <= self.x_end+1 
                and self.y_start-1 <= cell[1] <= self.y_end+1)


class ShipFactory:
    """ Class to create new ships in specific configurations."""
    def __init__(self, board_size=(10,10), ships_per_length=None):
        """ Initialises the ShipFactory class with necessary information.
        
        Args: 
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)
            ships_per_length (dict): A dict with the length of ship as keys and
                the count as values. Defaults to 1 ship each for lengths 1-5.
        """
        self.board_size = board_size
        
        if ships_per_length is None:
            # Default: lengths 1 to 5, one ship each
            self.ships_per_length = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        else:
            self.ships_per_length = ships_per_length

    @classmethod
    def create_ship_from_str(cls, start, end, board_size=(10,10)):
        """ A class method for creating a ship from string based coordinates.
        
        Example usage: ship = ShipFactory.create_ship_from_str("A3", "C3")
        
        Args:
            start (str): starting coordinate of the ship (example: 'A3')
            end (str): ending coordinate of the ship (example: 'C3')
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)

        Returns:
            Ship : a Ship instance created from start to end string coordinates
        """
        converter = CellConverter(board_size)
        return Ship(start=converter.from_str(start),
                    end=converter.from_str(end))

    def generate_ships(self):
        """ Generate a list of ships in the appropriate configuration.
        
        The number and length of ships generated must obey the specifications 
        given in self.ships_per_length.
        
        The ships must also not overlap with each other, and must also not be 
        too close to one another (as defined earlier in Ship::is_near_ship()).
        This is done in the while() loop. If we have an impossible 
        ships_per_length to satisfy, we try to fit as many ships on the grid 
        as possible but will terminate at some point, hence the counter to 
        limit the while loop from running indefinitely.
        
        The coordinates should also be valid given self.board_size
        
        Returns:
            list[Ships] : A list of Ship instances, adhering to the rules above
        """
        ships = [] # Initialise list to collect Ship objects
        
        for ships_to_build in [item for item in self.ships_per_length.items()]:
            ship_number = ships_to_build[1] # default is 1 per length
            ship_length = ships_to_build[0]
            for ship_to_build in range(0, ship_number): # build n ships per length
                ship = self.build_ship(length = ship_length)
                if len(ships) == 0: # if our list is empty, add the first ship
                    ships.append(ship)
                else:
                    i = 1
                    # Check if the ship is too close to our existing ships
                    while i < 1000: 
                        if any(ship.is_near_ship(other_ship) for other_ship in ships):
                            ship = self.build_ship(length = ship_length)
                        i += 1
                    # If not, add it into the list of ships
                    ships.append(ship)   
        return ships
                        
        
        
    def build_ship(self, length):
        """ Build a ship of a given length.
        
        We begin by randomnly selecting a co-ordinate on the grid to build from.
        Then we choose a direction to build in: horizontal or vertical.
        Then we build out for the given length, ensuring we're within the grid
        
        Args:
            length (int): how many cells the ship should occupy
            existing_ships (list) : list of already created Ship instances 
            
        Returns:
            Ship : a Ship instance created from start to end string coordinates
        """
        
        converter = CellConverter(self.board_size)
        
        # Specify valid grid limits
        min_valid_x = 1
        min_valid_y = 1
        max_valid_x = self.board_size[0]
        max_valid_y = self.board_size[1]
        
        # Create random starting coords
        x_start = random.randint(min_valid_x, max_valid_x)
        y_start = random.randint(min_valid_y, max_valid_y)
        cell_start = converter.to_str(tuple([x_start, y_start]))
        
        # Generate a random direction for the ship to build out from
        rand_dir = random.random()
        if rand_dir < 0.5: # note a *very* minor bias due to inequality
            # We build horizontally
            x_end = x_start + 1 - length # by default build left
            if x_end < min_valid_x: # but build right if we go out of bounds
                x_end = x_start - 1 + length
            cell_end = converter.to_str(tuple([x_end, y_start]))
            ship = ShipFactory.create_ship_from_str(cell_start, cell_end)
        else:
            # We build vertically
            y_end = y_start -1 + length # by default build down
            if y_end > max_valid_y:
                y_end = y_start + 1 - length
            cell_end = converter.to_str(tuple([x_start, y_end]))
            ship = ShipFactory.create_ship_from_str(cell_start, cell_end)
        
        return ship     
        
        
        
if __name__ == '__main__':
    # SANDBOX for you to play and test your methods

    ship = Ship(start=(3, 3), end=(5, 3))
    print(ship.get_cells())
    print(ship.length())
    print(ship.is_horizontal())
    print(ship.is_vertical())
    print(ship.is_near_cell((5, 3)))
    
    print(ship.receive_damage((4, 3)))
    print(ship.receive_damage((10, 3)))
    print(ship.damaged_cells)
    
    ship2 = Ship(start=(4, 1), end=(4, 5))
    print(ship.is_near_ship(ship2))

    # For Task 3
    ships = ShipFactory().generate_ships()
    print(ships)
        
    