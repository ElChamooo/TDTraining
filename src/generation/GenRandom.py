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
        
    def update_cells_states(self, loc_cells):
        for key, value in loc_cells.items():
                    if not isinstance(value, dict):
                        continue  # ignore les ints
                    value["state_cell"]=self.state_to_str(value["cell"])
                    value["state_neighboor"]=self.state_to_str(value["neighboor"])
                    value["state_wife"]=self.state_to_str(value["wife"])
        return loc_cells

        
    def update_is_adj_wife_visited(self, loc_cells):
        if loc_cells["front"]["state_wife"]=="visited":
            loc_cells["front"]["is_adj_wife_visited"]=True
            loc_cells["right"]["is_adj_wife_visited"]=True
        if loc_cells["right"]["state_wife"]=="visited":
            loc_cells["right"]["is_adj_wife_visited"]=True
            loc_cells["back"]["is_adj_wife_visited"]=True
        if loc_cells["back"]["state_wife"]=="visited":
            loc_cells["back"]["is_adj_wife_visited"]=True
            loc_cells["left"]["is_adj_wife_visited"]=True
        if loc_cells["left"]["state_wife"]=="visited":
            loc_cells["left"]["is_adj_wife_visited"]=True
            loc_cells["front"]["is_adj_wife_visited"]=True
        return loc_cells

    def update_state_path(self, loc_cells):
        for key, value in loc_cells.items():
            if not isinstance(value, dict):
                continue  # ignore les ints
            elif value["state_cell"] == "wall" or value["state_cell"] == "visited":
                value["state_path"]="unvalid"
            elif value["state_cell"] == "free" and (value["state_neighboor"] == "visited" or value["is_adj_wife_visited"]) :
                value["state_path"]="looping"
            elif value["state_cell"] == "free" and (value["state_neighboor"] == "wall" or value["state_neighboor"] == "free") and not value["is_adj_wife_visited"]:
                value["state_path"]="valid"
                loc_cells["free_neightboor"]+=1
            else: 
                raise ValueError(f'The state_path couldn\'t be deternemined: state_cell({value["state_cell"]}), state_neighboor({value["state_neightboor"]}), is_adj_wife_visited({value["is_adj_wife_visited"]})')
        return loc_cells
    
    def update_turn(self, end_corridor, loc_cells):
        if end_corridor:
            return self.choose_direction_end_corridor(loc_cells)
        else:
            return self.choose_direction_corridor(loc_cells)
    
#-------------------------------------Turn functions-------------------------------------#
    
    def choose_direction_corridor(self, loc_cells):
        print(f'[DEBUG]: Choosing next turn (not end of corridor)')
        front_free=loc_cells["front"]["state_path"]=="valid"
        print(f'[DEBUG]: Front cell: {"valid" if front_free else "invalid"}')
        right_free=loc_cells["right"]["state_path"]=="valid"
        print(f'[DEBUG]: Right cell: {"valid" if right_free else "invalid"}')
        back_free=loc_cells["back"]["state_path"]=="valid"
        print(f'[DEBUG]: Back cell: {"valid" if back_free else "invalid"}')
        left_free=loc_cells["left"]["state_path"]=="valid"
        print(f'[DEBUG]: Left cell: {"valid" if left_free else "invalid"}')
        if front_free:
            return 0
        elif not back_free and not left_free and not right_free: # 000
            return -1
        elif not back_free and not left_free and right_free: # 001
            return 1
        elif not back_free and left_free and not right_free: # 010
            return 3
        elif not back_free and left_free and right_free: # 011
            return random.choice([1,3])
        elif back_free and not left_free and not right_free: #100 
            return 2
        elif back_free and not left_free and right_free: # 101
            return random.choice([1,2])
        elif back_free and left_free and not right_free: # 110
            return random.choice([2,3])
        elif back_free and left_free and right_free: # 111
            return random.choice([1,2,3])
            
    def choose_direction_end_corridor(self, loc_cells):
        print(f'[DEBUG]: Choosing next turn (not end of corridor)')
        front_free=loc_cells["front"]["state_path"]=="valid"
        print(f'[DEBUG]: Front cell: {"valid" if front_free else "invalid"}')
        right_free=loc_cells["right"]["state_path"]=="valid"
        print(f'[DEBUG]: Right cell: {"valid" if right_free else "invalid"}')
        back_free=loc_cells["back"]["state_path"]=="valid"
        print(f'[DEBUG]: Back cell: {"valid" if back_free else "invalid"}')
        left_free=loc_cells["left"]["state_path"]=="valid"
        print(f'[DEBUG]: Left cell: {"valid" if left_free else "invalid"}')

        if not back_free and not front_free and not right_free and not left_free: # 0000
            return -1
        elif not back_free and not front_free and not right_free and left_free: # 0001
            return 3
        elif not back_free and not front_free and right_free and not left_free: # 0010
            return 1
        elif not back_free and not front_free and right_free and left_free: # 0011
            return random.choice([1,3])
        elif not back_free and front_free and not right_free and not left_free: # 0100
            return 0
        elif not back_free and front_free and not right_free and left_free: # 0101
            return random.choice([0,3])
        elif not back_free and front_free and right_free and not left_free: # 0110
            return random.choice([0,1])
        elif not back_free and front_free and right_free and left_free: # 0111
            return random.choice([0,1,3])
        elif back_free and not front_free and not right_free and not left_free: # 1000
            return 2
        elif back_free and not front_free and not right_free and left_free: # 1001
            return random.choice([2,3])
        elif back_free and not front_free and right_free and not left_free: # 1010
            return random.choice([1,2])
        elif back_free and not front_free and right_free and left_free: # 1011
            return random.choice([1,2,3])
        elif back_free and front_free and not right_free and not left_free: # 1100
            return random.choice([0,2])
        elif back_free and front_free and not right_free and left_free: # 1101
            return random.choice([0,2,3])
        elif back_free and front_free and right_free and not left_free: # 1110
            return random.choice([0,1,2])
        elif back_free and front_free and right_free and left_free: # 1111
            return random.choice([0,1,2,3])
        
#-------------------------------------Split node functions-------------------------------------#
    
    def split_nodes_empty(self) -> bool:
        return len(self.split_nodes) == 0
    
    def add_split_node(self):
        cell_to_add=self.get_cell_current()
        for i, cell in enumerate(self.split_nodes):
            if cell.x == cell_to_add.x and cell.y == cell_to_add.y:
                print(f"Cannot add a cell that is already a in split_nodes: ({cell_to_add.x}, {cell_to_add.y})")
                return
        self.split_nodes.append(self.get_cell_current())
    
    def del_split_node(self) -> Cell:
        cell_to_del = self.get_cell_current()
        for i, cell in enumerate(self.split_nodes):
            if cell.x == cell_to_del.x and cell.y == cell_to_del.y:
                return self.split_nodes.pop(i)
        print(f"No matching split node found ({cell_to_del.x}, {cell_to_del.y})")

    def is_current_in_split_node(self) -> bool:
        cell_to_find = self.get_cell_current()
        for i, cell in enumerate(self.split_nodes):
            if cell.x == cell_to_find.x and cell.y == cell_to_find.y:
                return True
        return False

    
    def get_last_split_node(self) -> Cell:
        if self.split_nodes:
            last_node=self.split_nodes[-1]
            return last_node
        else:
            return None

#-------------------------------------Setter-------------------------------------#
    
    def set_direction(self, direction: int):
        self.maze.set_direction(direction)

    def set_origin(self, x, y):
        self.maze.set_origin(x, y)

    def set_finish(self, x, y):
        self.maze.set_finish(x, y)

    def set_current(self, x, y):
        self.maze.set_current(x, y)

    def turn(self, turn):
        self.maze.set_direction((self.maze.get_direction() + turn) % 4)

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

    def is_frontside_valid(self, cell) -> bool:
        return self.maze.is_frontside_valid(cell)
            
    def is_rightside_valid(self, cell) -> bool:
        return self.maze.is_rightside_valid(cell)
            
    def is_leftside_valid(self, cell) -> bool:
        return self.maze.is_leftside_valid(cell)
            
    def is_backside_valid(self, cell) -> bool:
        return self.maze.is_backside_valid(cell)
    
    def is_deadend(self, cell) -> bool:
        free_neighbors = 0
        # Check forward
        if self.is_frontside_valid(cell):
            free_neighbors += 1
        # Check left
        if self.is_leftside_valid(cell):
            free_neighbors += 1
        # Check right
        if self.is_rightside_valid(cell):
            free_neighbors += 1
        return free_neighbors == 0  # Dead-end if no free neighbor

    def is_cornered(self, cell) -> bool:
        if self.is_frontside_valid(cell):
            return False
        elif self.is_leftside_valid(cell) == self.is_rightside_valid(cell):
            return False
        else:
            return True

    def put_wall_onsides(self):
        if self.is_leftside_valid(self.get_cell_current()):
            self.maze.set_wall_on_left()
        if self.is_rightside_valid(self.get_cell_current()):
            self.maze.set_wall_on_right()

    def put_wall_infront(self):
        self.maze.set_wall_in_front()

    def put_wall_left(self):
        self.maze.set_wall_on_left()

    def put_wall_right(self):
        self.maze.set_wall_on_right()

    def put_wall_back(self):
        self.maze.set_wall_in_back()

    def does_forward_loops(self, x, y) -> bool:
        current_cell = self.get_cell(x, y)
        cell_infront = self.get_cell_front(current_cell)
        if self.is_frontside_valid(current_cell) and self.get_cell_front(cell_infront).is_visited() and not self.get_cell_front(cell_infront).is_wall():
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
        


    
        
    def is_fully_generated(self) -> bool:
        if self.split_nodes_empty() and self.maze.get_finish().is_visited():
            return True
        return False

    def __del__(self):
        del self.maze
