import random

from battleship.board import Board
from battleship.convert import CellConverter

class Player:
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players
    
    def __init__(self, board=None, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        
        if board is None:
            self.board = Board()
        else:
            self.board = board
        
        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name
    
    def __str__(self):
        return self.name
    
    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError
    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        This method does not do anything by default, but can be overridden by a 
        subclass to do something useful, for example to record a successful or 
        failed attack.
        
        Returns:
            None
        """
        return None
    
    def has_lost(self):
        """ Check whether player has lost the game.
        
        Returns:
            bool: True if and only if all the ships of the player have sunk.
        """
        return self.board.have_all_ships_sunk()


class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, board, name=None):
        """ Initialise the player with a board and other attributes.
        
        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(board=board, name=name)
        self.converter = CellConverter((board.width, board.height))
        
    def select_target(self):
        """ Read coordinates from user prompt.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        print(f"It is now {self}'s turn.")

        while True:
            try:
                coord_str = input('coordinates target = ')
                x, y = self.converter.from_str(coord_str)
                return x, y
            except ValueError as error:
                print(error)


class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()

    def select_target(self):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        target_cell = self.generate_random_target()
        self.tracker.add(target_cell)
        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        
        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)


class AutomaticPlayer(Player):
    """ Player playing automatically using a strategy."""
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        
        self.tracker = set()
        self.moves = list()
        self.attack_successful = False
        self.ship_being_attacked = list()
        
    def is_valid_target(self, cell):
        """ Checks if a cell lies within the board """
        x_min = 1
        y_min = 1
        x_max = self.board.width
        y_max = self.board.height        
        x = cell[0]
        y = cell[1]        
        return (x_min <= x <= x_max and y_min <= y <= y_max)
    
    def cell_unvisited(self, cell):
        return cell not in self.tracker
    
    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)
    
    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        
        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell
    
    def all_surrounding_cells(self, cell):
        x = cell[0]
        y = cell[1]
        
        top_left = tuple([x-1, y-1])
        top_mid = tuple([x, y-1])
        top_right = tuple([x+1, y-1])
        left = tuple([x-1, y])
        right = tuple([x+1, y])
        bot_left = tuple([x-1, y+1])
        bot_mid = tuple([x, y-1])
        bot_right = tuple([x+1, y-1])
        
        cells = [top_left, top_mid, top_right, left, right, bot_left, bot_mid, bot_right]
        
        # Remove any that are out of bounds
        cells = [cell for cell in cells if self.is_valid_target(cell)]
        
        # Also remove any we've already visited
        cells = [cell for cell in cells if self.cell_unvisited(cell)]
        
        return cells
    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        Returns:
            (bool) : True if ship is hit but not sunk
        """
        # Log the successful move into the ship being attacked
        if is_ship_hit:
            previous_move = self.moves[-1]
            self.ship_being_attacked.append(previous_move)
            self.attack_successful = True
        else:
            self.attack_successful = False
           
        if has_ship_sunk:
            # We need to remove all adjacent cells from future consideration
            for cell in self.ship_being_attacked:
                for surrounding_cell in self.all_surrounding_cells(cell):                    
                    self.tracker.add(surrounding_cell)
            self.ship_being_attacked = list()
            
        
    def get_adjacent_cells(self, cell):
        """ Returns the surrounding cells of a given cell, if within bounds"""
        x_min = 1
        y_min = 1
        x_max = self.board.width
        y_max = self.board.height
        
        x = cell[0]
        y = cell[1]
        
        if x - 1 >= x_min:
            left = tuple([x-1, y])
        else:
            left = tuple([x, y])
        
        if x + 1 <= x_max:
            right = tuple([x+1, y])
        else:
            right = tuple([x, y])
        
        if y - 1 >= y_min:
            up = tuple([x, y - 1])
        else:
            up = tuple([x, y])
            
        if y + 1 <= y_max:
            down = tuple([x, y + 1])
        else:
            down = tuple([x, y])
            
        potential_targets =  [left, right, up, down]
        targets = [cell for cell in potential_targets if self.cell_unvisited(cell)]
        return targets
    
    def select_target(self):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """

        # If we have no ship yet being attacked, select a random cell
        if len(self.ship_being_attacked) == 0:
            target_cell = self.get_random_coordinates()
            self.tracker.add(target_cell)
            self.moves.append(target_cell)
            return target_cell
        
        
        # If we have only a single hit, try hitting an adjacent cell
        if len(self.ship_being_attacked) == 1:
            previous_successful_hit = self.ship_being_attacked[0]
            potential_targets = self.get_adjacent_cells(previous_successful_hit)
            for cell in potential_targets:
                if self.cell_unvisited(cell) and self.is_valid_target(cell):
                    target_cell = cell
                    self.tracker.add(target_cell)
                    self.moves.append(target_cell)
                    return target_cell
        
        # If we've got successive attacks, figure out the orientation of the ship
        if len(self.ship_being_attacked) > 1:
            
            if self.ship_being_attacked[0][0] == self.ship_being_attacked[1][0]:
                orientation = 'horizontal'
            else:
                orientation = 'vertical'
        
            # Attack the next square in that direction, unless the last attack failed
            if self.attack_successful == True:
                if orientation == 'horizontal':
                    potential_target =  tuple([self.ship_being_attacked[-1][0] - 1, self.ship_being_attacked[-1][1]])
                    if self.cell_unvisited(potential_target) and self.is_valid_target(potential_target):
                        target_cell = potential_target
                        self.tracker.add(target_cell)
                        self.moves.append(target_cell)
                        return target_cell
                    else:
                        target_cell = tuple([self.ship_being_attacked[0][0] + 1, self.ship_being_attacked[0][1]])
                        self.tracker.add(target_cell)
                        self.moves.append(target_cell)
                        return target_cell
            else:
                if orientation == 'horizontal':
                    potential_target = tuple([self.ship_being_attacked[-1][0], self.ship_being_attacked[-1][1] - 1])
                    if self.cell_unvisited(potential_target) and self.is_valid_target(potential_target):
                        target_cell = potential_target
                        self.tracker.add(target_cell)
                        self.moves.append(target_cell)
                        return target_cell
                    else:
                        target_cell = tuple([self.ship_being_attacked[0][0], self.ship_being_attacked[0][1] + 1])
                        self.tracker.add(target_cell)
                        self.moves.append(target_cell)
                        return target_cell
        
            
