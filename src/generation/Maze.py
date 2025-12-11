from generation.Cell import Cell

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.direction = 0  # 0: east, 1: south, 2: west, 3: north
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]  # Tableau de lignes
        self.generate_borders()


#-------------------------------------Get données membres-------------------------------------#

    def get_width(self) -> int:
        return self.width
    
    def get_height(self) -> int:
        return self.height

    def get_origin(self) -> Cell:
        for row in self.grid:
            for cell in row:
                if cell.is_origin():
                    return cell
        return None

    def get_finish(self) -> Cell:
        for row in self.grid:
            for cell in row:
                if cell.is_finish():
                    return cell
        return None 

    def get_direction(self) -> int: 
        return self.direction

    # def get_visited(self, x, y) -> Cell:
    #     return self.get_cell(x, y)
    
#-------------------------------------Get Cell-------------------------------------#

    def get_cell(self, x, y) -> Cell:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            return None

    def get_current(self) -> Cell:
        for row in self.grid:
            for cell in row:
                if cell.is_current():
                    return cell
        return None 
    
    def get_cell_front(self, x ,y, howfar=1) -> Cell:
        direction=self.get_direction()
        match direction:
            case 0: # East
                return self.get_cell(x+howfar,y)
            case 1: # South
                return self.get_cell(x,y+howfar)
            case 2: # West
                return self.get_cell(x-howfar,y)
            case 3: # North
                return self.get_cell(x,y-howfar)
    
    def get_cell_left(self, x ,y, howfar=1) -> Cell:
        direction=self.get_direction()
        match direction:
            case 0: # East
                return self.get_cell(x,y-howfar)
            case 1: # South
                return self.get_cell(x+howfar,y)
            case 2: # West
                return self.get_cell(x,y+howfar)
            case 3: # North
                return self.get_cell(x-howfar,y)
    
    def get_cell_back(self, x ,y, howfar=1) -> Cell:
        direction=self.get_direction()
        match direction:
            case 0: # East
                return self.get_cell(x-howfar,y)
            case 1: # South
                return self.get_cell(x,y-howfar)
            case 2: # West
                return self.get_cell(x+howfar,y)
            case 3: # North
                return self.get_cell(x,y+howfar)
    
    def get_cell_right(self, x ,y, howfar=1) -> Cell:
        direction=self.get_direction()
        match direction:
            case 0: # East
                return self.get_cell(x,y+howfar)
            case 1: # South
                return self.get_cell(x-howfar,y)
            case 2: # West
                return self.get_cell(x,y-howfar)
            case 3: # North
                return self.get_cell(x+howfar,y)
            
#-------------------------------------Setter-------------------------------------#
    
    def set_direction(self, direction: int):
        self.direction = direction % 4 
    
    def set_current(self, x, y):
        if self.is_boundary(x, y):
            raise ValueError("Cannot set boundary cell as current: ({}, {})".format(x, y))
        current = self.get_current()
        if current:
            current.unset_current()
        self.get_cell(x, y).set_current()
        self.get_cell(x, y).set_visited() 

    def set_origin(self, x, y):
        self.get_cell(x, y).set_origin()
        self.set_current(x, y)
    
    def set_finish(self, x, y):
        self.get_cell(x, y).set_finish()
    
    def set_visited(self, x, y):
        self.get_cell(x, y).set_visited()

    def set_unvisited(self, x, y):
        self.get_cell(x, y).unset_visited()
    
    def set_height(self, height: int):
        self.height = height
    
    def set_width(self, width: int):
        self.width = width
        
    def set_wall(self, x, y):
        if self.is_boundary(x, y):
            raise ValueError("Cannot set boundary cell as wall: ({}, {})".format(x, y))
        self.get_cell(x, y).set_wall()

    def set_wall_boundary(self, x, y):
        self.get_cell(x, y).set_wall()

    def set_free(self, x, y):
        if self.is_boundary(x, y):
            raise ValueError("Cannot set boundary cell as free: ({}, {})".format(x, y))
        self.get_cell(x, y).set_free()



    
    
    
    def is_visited(self, x, y) -> bool:
        return self.get_cell(x, y).is_visited()
    
    def is_finish(self, x, y) -> bool:
        return self.get_cell(x, y).is_finish()
    
    def is_origin(self, x, y) -> bool:
        return self.get_cell(x, y).is_origin()
    
    def is_current(self, x, y) -> bool:
        return self.get_cell(x, y).is_current()

    def is_boundary(self, x, y) -> bool:
        return x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1

    def is_valid_next_path(self, x, y) -> bool:
        cell = self.get_cell(x, y)
        return cell.is_free() and not cell.is_visited() and not self.is_boundary(x, y)
    
    def is_forward_valid(self, cell) -> bool:
        match self.direction:
            case 0:  # east
                return self.is_valid_next_path(cell.x + 1, cell.y)
            case 1:  # south
                return self.is_valid_next_path(cell.x, cell.y + 1)
            case 2:  # west
                return self.is_valid_next_path(cell.x - 1, cell.y)
            case 3:  # north
                return self.is_valid_next_path(cell.x, cell.y - 1)
            case _:
                raise ValueError("Invalid direction: {}".format(self.direction))
    
    def is_leftside_valid(self, cell) -> bool:
        match self.direction:
            case 0:  # east
                return self.is_valid_next_path(cell.x, cell.y - 1)
            case 1:  # south
                return self.is_valid_next_path(cell.x + 1, cell.y)
            case 2:  # west
                return self.is_valid_next_path(cell.x, cell.y + 1)
            case 3:  # north
                return self.is_valid_next_path(cell.x - 1, cell.y)
            case _:
                raise ValueError("Invalid direction: {}".format(self.direction))
            
    def is_rightside_valid(self, cell) -> bool:
        match self.direction:
            case 0:  # east
                return self.is_valid_next_path(cell.x, cell.y + 1)
            case 1:  # south
                return self.is_valid_next_path(cell.x - 1, cell.y)
            case 2:  # west
                return self.is_valid_next_path(cell.x, cell.y - 1)
            case 3:  # north
                return self.is_valid_next_path(cell.x + 1, cell.y)
            case _:
                raise ValueError("Invalid direction: {}".format(self.direction))
            
    def set_wall_on_left(self):
        current = self.get_current()
        match self.direction:
            case 0:  # east
                self.set_wall(current.x, current.y - 1)
            case 1:  # south
                self.set_wall(current.x + 1, current.y)
            case 2:  # west
                self.set_wall(current.x, current.y + 1)
            case 3:  # north
                self.set_wall(current.x - 1, current.y)
            case _:
                raise ValueError("Invalid direction: {}".format(self.direction))
    
    def set_wall_in_back(self):
        current = self.get_current()
        match self.direction:
            case 0:  # east
                self.set_wall(current.x - 1, current.y)
            case 1:  # south
                self.set_wall(current.x, current.y - 1)
            case 2:  # west
                self.set_wall(current.x + 1, current.y)
            case 3:  # north
                self.set_wall(current.x, current.y + 1)
            case _:
                raise ValueError("Invalid direction: {}".format(self.direction))
            
    def set_wall_on_right(self):
        current = self.get_current()
        match self.direction:
            case 0:  # east
                self.set_wall(current.x, current.y + 1)
            case 1:  # south
                self.set_wall(current.x - 1, current.y)
            case 2:  # west
                self.set_wall(current.x, current.y - 1)
            case 3:  # north
                self.set_wall(current.x + 1, current.y)
            case _:
                raise ValueError("Invalid direction: {}".format(self.direction))
            
    def set_wall_in_front(self):
        current = self.get_current()
        match self.direction:
            case 0:  # east
                self.set_wall(current.x + 1, current.y)
            case 1:  # south
                self.set_wall(current.x, current.y + 1)
            case 2:  # west
                self.set_wall(current.x - 1, current.y)
            case 3:  # north
                self.set_wall(current.x, current.y - 1)
            case _:
                raise ValueError("Invalid direction: {}".format(self.direction))
            
    def move_forward(self):
        current = self.get_current()
        match self.direction:
            case 0:  # east
                if self.is_boundary(current.x + 1, current.y):
                    raise ValueError("Cannot move forward into boundary cell: ({}, {})".format(current.x + 1, current.y))
                self.set_current(current.x + 1, current.y)
            case 1:  # south
                if self.is_boundary(current.x, current.y + 1):
                    raise ValueError("Cannot move forward into boundary cell: ({}, {})".format(current.x, current.y + 1))
                self.set_current(current.x, current.y + 1)
            case 2:  # west
                if self.is_boundary(current.x - 1, current.y):
                    raise ValueError("Cannot move forward into boundary cell: ({}, {})".format(current.x - 1, current.y))
                self.set_current(current.x - 1, current.y)
            case 3:  # north
                if self.is_boundary(current.x, current.y - 1):
                    raise ValueError("Cannot move forward into boundary cell: ({}, {})".format(current.x, current.y - 1))
                self.set_current(current.x, current.y - 1)
            case _:
                raise ValueError("Invalid direction: {}".format(self.direction))

    def clear(self):
        self.get_current().unset_current()
        if self.get_origin() is not None:
            self.get_origin().origin = False
        if self.get_finish() is not None:
            self.get_finish().finish = False
        for row in self.grid:
            for cell in row:
                cell.set_free()
                cell.visited = False

    def generate_borders(self):
        for x in range(self.get_width()):
            self.set_wall_boundary(x, 0)
            self.set_wall_boundary(x, self.get_height() - 1)
        for y in range(self.get_height()):
            self.set_wall_boundary(0, y)
            self.set_wall_boundary(self.get_width() - 1, y)
    




    def __str__(self):
        def cell_to_char(cell):
            if cell.is_current():
                return 'c'
            elif cell.is_origin():
                return 'o'
            elif cell.is_finish():
                return 'f'
            elif cell.is_visited():
                return 'v'
            elif cell.is_wall() and self.is_boundary(cell.x, cell.y):
                return 'x'
            elif cell.is_wall():
                return 'w'
            else:
                return '.'
            
        def nb_to_dir(nb):
            match nb:
                case 0:
                    return 'East'
                case 1:
                    return 'South'
                case 2:
                    return 'West'
                case 3:
                    return 'North'
                case _:
                    return 'Unknown'

        return f'Direction: {nb_to_dir(self.direction)}\n' + '\n'.join(''.join(cell_to_char(cell) for cell in row) for row in self.grid)
    


    def display(self):
        for row in self.grid:
            print(''.join(str(cell) for cell in row))

    def __repr__(self):
        return f"Maze(width={self.width}, height={self.height})"
    
    