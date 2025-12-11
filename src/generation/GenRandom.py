import random
from generation.Cell import Cell


class GenRandom:
    def __init__(self, maze):
        self.maze = maze
        self.maze.set_current(1, 1)
        self.split_nodes = []

#-------------------------------------Get données membres-------------------------------------#

    def get_width(self) -> int:
        return self.maze.get_width()
    
    def get_height(self) -> int:
        return self.maze.get_height()

    def get_origin(self) -> Cell:
        return self.maze.get_origin()

    def get_finish(self) -> Cell:
        return self.maze.get_finish()

    def get_direction(self) -> int:
        return self.maze.get_direction()
    
#-------------------------------------Get Cell-------------------------------------#

    def get_cell(self, cell) -> Cell:
        return self.maze.get_cell(cell)

    def get_cell_current(self) -> Cell:
        if self.maze.get_current() is None:
            raise ValueError("No current cell is set in the maze.")
        return self.maze.get_current()
    
    def get_cell_front(self, cell, howfar=1) -> Cell:
        return self.maze.get_cell_front(cell.x, cell.y, howfar)
    
    def get_cell_left(self, cell, howfar=1) -> Cell:
        return self.maze.get_cell_left(cell.x, cell.y, howfar)
    
    def get_cell_right(self, cell, howfar=1) -> Cell:
        return self.maze.get_cell_right(cell.x, cell.y, howfar)
    
    def get_cell_back(self, cell, howfar=1) -> Cell:
        return self.maze.get_cell_back(cell.x, cell.y, howfar)
    



#-------------------------------------Verification functions-------------------------------------#

    def state_to_str(self, cell):
        if cell is None:
            return "wall"
        elif cell.is_wall():
            return "wall"
        elif cell.is_visited():
            return "visited"
        elif cell.is_free():
            return "free"

#-------------------------------------Setter-------------------------------------#
    
    def set_direction(self, direction: int):
        self.maze.set_direction(direction)

    def set_origin(self, x, y):
        self.maze.set_origin(x, y)

    def set_finish(self, x, y):
        self.maze.set_finish(x, y)

    def set_current(self, x, y):
        self.maze.set_current(x, y)

    def turn_right(self):
        self.maze.set_direction((self.maze.get_direction() + 1) % 4)
    
    def turn_left(self):
        self.maze.set_direction((self.maze.get_direction() - 1) % 4)

    def turn_back(self):
        self.maze.set_direction((self.maze.get_direction() + 2) % 4)

    def forward(self):
        self.maze.move_forward()

    def clear_maze(self):
        self.maze.clear()

    def generate_borders(self):
        self.maze.generate_borders()

    def is_infront_valid(self, cell) -> bool:
        return self.maze.is_forward_valid(cell)
            
    def is_rightside_valid(self, cell) -> bool:
        return self.maze.is_rightside_valid(cell)
            
    def is_leftside_valid(self, cell) -> bool:
        return self.maze.is_leftside_valid(cell)
    
    def is_deadend(self, cell) -> bool:
        free_neighbors = 0
        # Check forward
        if self.is_infront_valid(cell):
            free_neighbors += 1
        # Check left
        if self.is_leftside_valid(cell):
            free_neighbors += 1
        # Check right
        if self.is_rightside_valid(cell):
            free_neighbors += 1
        return free_neighbors == 0  # Dead-end if no free neighbor

    def is_cornered(self, cell) -> bool:
        if self.is_infront_valid(cell):
            return False
        elif self.is_leftside_valid(cell) == self.is_rightside_valid(cell):
            return False
        else:
            return True

    def put_wall_onsides(self, current_cell):
        if self.is_leftside_valid(current_cell):
            self.maze.set_wall_on_left()
        if self.is_rightside_valid(current_cell):
            self.maze.set_wall_on_right()

    def put_wall_infront(self):
        self.maze.set_wall_in_front()

    def put_wall_left(self):
        self.maze.set_wall_on_left()

    def put_wall_right(self):
        self.maze.set_wall_on_right()

    def put_wall_back(self):
        self.maze.set_wall_in_back()


    def choose_random_direction(self):
        if self.is_deadend(self.get_cell_current()):
            return -1
        elif self.is_cornered(self.get_cell_current()):
            if self.is_rightside_valid(self.get_cell_current()):
                return 1
            else:
                return 3
        elif random.choice([True, False]):
            if self.is_leftside_valid(self.get_cell_current()):
                return 3
        else:
            if self.is_rightside_valid(self.get_cell_current()):
                return 1

    def does_forward_loops(self, x, y) -> bool:
        current_cell = self.get_cell(x, y)
        cell_infront = self.get_cell_front(current_cell)
        if self.is_infront_valid(current_cell) and self.get_cell_front(cell_infront).is_visited() and not self.get_cell_front(cell_infront).is_wall():
            return True
        else:
            return False
        
    def forward_not_to_loop(self):
        self.choose_random_direction()
        if not self.does_forward_loops(self.get_cell_current().x,self.get_cell_current().y):
            self.forward()
            return "Move forward"
        else: 
            self.put_wall_infront()
            return "Put wall in front to avoid looping"
        


    def split_nodes_empty(self) -> bool:
        return len(self.split_nodes) == 0
    
    def add_split_node(self, cell: Cell):
        self.split_nodes.append(cell)

    def del_split_node(self, cell_to_del) -> Cell:
        for i, cell in enumerate(self.split_nodes):
            if cell.x == cell_to_del.x and cell.y == cell_to_del.y:
                return self.split_nodes.pop(i)
        print(f"No matching split node found ({cell_to_del.x}, {cell_to_del.y})")
    
    def get_last_split_node(self) -> Cell:
        if self.split_nodes:
            last_node=self.split_nodes[-1]
            return last_node
        else:
            return None
        
    def is_fully_generated(self) -> bool:
        if not self.split_nodes_empty() or not self.maze.get_finish().is_visited():
            return False
        return True

    def __del__(self):
        del self.maze
