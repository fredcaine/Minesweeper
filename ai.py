class MinesweeperAI:

    def __init__(self, cells_dict: dict):

        self.cells_dict = cells_dict
        self.known_info = {}

        self.solutions = []
        self.bombs = []
        self.known_bombs = []

    def run_ai(self, goal):

        for cell in self.cells_dict.values():
            if cell.clicked == 1:  # we are not allowed to access adjacent bomb count unless the cell has been clicked already
                self.known_info.update({(cell.row, cell.column) : cell.adjacent_bombs})

        self.solutions = []
        self.bombs = []
        self.solutions.extend(self.check_zeroes())
        self.solutions.extend(self.check_forceclears())
        self.bombs.extend(self.check_forcible())
        self.solutions = [tuple(t) for t in set(tuple(x) for x in self.solutions)]
        self.bombs = [tuple(t) for t in set(tuple(x) for x in self.bombs)]

        self.bombs = [x for x in self.bombs if self.cells_dict[x].flagged == 0]
        self.known_bombs.extend(self.bombs)
        self.known_bombs = [tuple(t) for t in set(tuple(x) for x in self.known_bombs)]

        if goal == 0:
            try:
                self.cells_dict[self.solutions[0]].tkbutton.config(bg="lightgreen")
            except IndexError:
                pass
        else:
            try:
                self.cells_dict[self.bombs[0]].tkbutton.config(bg="red")
            except IndexError:
                pass

    def all_known_adjacent(self, row, column, known_or_unknown = True):
        all_known = []

        invalid_cells = []
        adjacent = ((row + 1, column + 1),
                    (row + 1, column),
                    (row + 1, column - 1),
                    (row, column + 1), 
                    (row, column - 1),
                    (row - 1, column + 1),
                    (row - 1, column),
                    (row - 1, column - 1))
        
        for item in adjacent:
            try:
                self.cells_dict[item]
            except KeyError:
                invalid_cells.append(item)
        adjacent = [x for x in adjacent if x not in invalid_cells]
        
        if known_or_unknown:
            for possible in adjacent:
                try:
                    self.known_info[possible]
                    all_known.append(self.known_info[tuple(possible)])
                except KeyError:
                    pass

            return all_known
        
        else:
            for possible in adjacent:
                try:
                    self.known_info[possible]
                except KeyError:
                    all_known.append(tuple(possible))
            
            return all_known

    def check_zeroes(self):

        zero_solutions = []
        for cell in self.known_info.keys():
            if self.known_info[cell] == 0:
                zero_solutions.extend(self.all_known_adjacent(cell[0], cell[1], False))
        
        return zero_solutions
    
    def check_forceclears(self):
        forceclear_solutions = []

        for cell in self.known_info.keys():
            known_adjacent_bombs = [x for x in self.all_known_adjacent(cell[0], cell[1], False) if x in self.known_bombs]
            if len(known_adjacent_bombs) == self.cells_dict[cell].adjacent_bombs:
                forceclear_solutions.extend([x for x in self.all_known_adjacent(cell[0], cell[1], False) if x not in self.known_bombs])
    
        return forceclear_solutions

    def check_forcible(self):
        
        forcible_solutions = []
        for cell in self.known_info.keys():
            if len(self.all_known_adjacent(cell[0], cell[1], False)) == self.cells_dict[cell].adjacent_bombs:
                forcible_solutions.extend(self.all_known_adjacent(cell[0], cell[1], False))

        return forcible_solutions

    def clear_ai(self):
        self.known_info = {}

        self.solutions = []
        self.bombs = []
        self.known_bombs = []