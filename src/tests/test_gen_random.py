import pytest
from generation.GenRandom import GenRandom
from generation.Maze import Maze

class TestGenRandom:

    def test_genrandom_initialization(self):
        maze = GenRandom(Maze(10, 15))
        assert maze.get_width() == 10
        assert maze.get_height() == 15
        assert maze.get_cell_current() is not None
        assert len(maze.split_nodes) == 0

    def test_get_and_set_direction(self):
        maze = GenRandom(Maze(5, 5))
        assert maze.get_direction() == 0  # Default direction
        maze.set_direction(2)
        assert maze.get_direction() == 2
        maze.set_direction(7)
        assert maze.get_direction() == 3 

    def test_set_and_get_current(self):
        maze = GenRandom(Maze(5, 5))
        maze.set_current(2, 3)
        current = maze.get_cell_current()
        assert current.x == 2
        assert current.y == 3
        assert current.is_visited() == True
        assert current.is_current() == True

    def test_set_and_get_origin(self):
        maze = GenRandom(Maze(5, 5))
        maze.set_origin(1, 1)
        origin = maze.get_origin()
        assert origin.x == 1
        assert origin.y == 1
        assert origin.is_origin() == True

    def test_set_and_get_finish(self):
        maze = GenRandom(Maze(5, 5))
        maze.set_finish(4, 4)
        finish = maze.get_finish()
        assert finish.x == 4
        assert finish.y == 4
        assert finish.is_finish() == True

    def test_turning_directions(self):
        maze = GenRandom(Maze(5, 5))
        initial_direction = maze.maze.get_direction()
        maze.turn_right()
        assert maze.maze.get_direction() == (initial_direction + 1) % 4
        maze.turn_left()
        assert maze.maze.get_direction() == initial_direction
        maze.turn_back()
        assert maze.maze.get_direction() == (initial_direction + 2) % 4

    def test_move_forward(self):
        maze = GenRandom(Maze(5, 5))
        maze.set_current(2, 2)
        maze.maze.set_direction(0)  # Facing east
        initial_cell = maze.get_cell_current()
        maze.forward()
        new_cell = maze.get_cell_current()
        excepected_x, expected_y = initial_cell.x+1, initial_cell.y
        assert (new_cell.x == excepected_x) and (new_cell.y == expected_y)

    def test_get_current_cell_no_current(self):
        maze = GenRandom(Maze(5, 5))
        maze.maze.get_current().unset_current()
        with pytest.raises(ValueError):
            maze.get_cell_current()
        maze.set_current(1, 1)
        current_cell = maze.get_cell_current()
        assert current_cell.x == 1 and current_cell.y == 1

    def test_is_infront_valid(self):
        maze = GenRandom(Maze(7, 7))
        maze.set_current(3, 3)
        maze.maze.set_direction(0)  # Facing east
        # Initially all sides are free
        assert maze.is_infront_valid(maze.get_cell_current()) == True
        # Set wall in front
        maze.maze.set_wall(4, 3)
        assert maze.is_infront_valid(maze.get_cell_current()) == False
        # Set visited in front
        maze.maze.set_free(4, 3)
        maze.maze.set_visited(4, 3)
        assert maze.is_infront_valid(maze.get_cell_current()) == False
        maze.maze.set_free(4, 3)
        
        maze.maze.set_direction(3)  # Facing north
        # Initially all sides are free
        assert maze.is_infront_valid(maze.get_cell_current()) == True
        # Set wall in front
        maze.maze.set_wall(3, 2)
        assert maze.is_infront_valid(maze.get_cell_current()) == False
        # Set visited in front
        maze.maze.set_free(3, 2)
        maze.maze.set_visited(3, 2)
        assert maze.is_infront_valid(maze.get_cell_current()) == False
        maze.maze.set_free(3, 2)

        maze.set_current(1, 1)
        maze.maze.set_direction(2)  # Facing west
        # Initially in front is boundary
        assert maze.is_infront_valid(maze.get_cell_current()) == False
        maze.maze.set_direction(1)  # Facing south
        # Initially in front sides are free
        assert maze.is_infront_valid(maze.get_cell_current()) == True

    def test_is_rightside_valid(self):
        maze = GenRandom(Maze(7, 7))
        maze.set_current(3, 3)
        maze.maze.set_direction(0)  # Facing east
        # Initially all sides are free
        assert maze.is_rightside_valid(maze.get_cell_current()) == True
        # Set wall on right
        maze.maze.set_wall(3, 4)
        assert maze.is_rightside_valid(maze.get_cell_current()) == False
        # Set visited on right
        maze.maze.set_free(3, 4)
        maze.maze.set_visited(3, 4)
        assert maze.is_rightside_valid(maze.get_cell_current()) == False
        maze.maze.set_free(3, 4)

        
        maze.maze.set_direction(1)  # Facing south
        # Initially all sides are free
        assert maze.is_rightside_valid(maze.get_cell_current()) == True
        # Set wall on right
        maze.maze.set_wall(2, 3)
        assert maze.is_rightside_valid(maze.get_cell_current()) == False
        # Set visited on right
        maze.maze.set_free(2, 3)
        maze.maze.set_visited(2, 3)
        assert maze.is_rightside_valid(maze.get_cell_current()) == False
        maze.maze.set_free(2, 3)

        maze.set_current(5, 5)
        maze.maze.set_direction(3)  # Facing north
        # Initially right is boundary
        assert maze.is_rightside_valid(maze.get_cell_current()) == False
        maze.maze.set_direction(2)  # Facing west
        # Initially right sides are free
        assert maze.is_rightside_valid(maze.get_cell_current()) == True

    def test_is_leftside_valid(self):
        maze = GenRandom(Maze(7, 7))
        maze.set_current(3, 3)
        maze.maze.set_direction(0)  # Facing east
        # Initially all sides are free
        assert maze.is_leftside_valid(maze.get_cell_current()) == True
        # Set wall on left
        maze.maze.set_wall(3, 2)
        assert maze.is_leftside_valid(maze.get_cell_current()) == False
        # Set visited on left
        maze.maze.set_free(3, 2)
        maze.maze.set_visited(3, 2)
        assert maze.is_leftside_valid(maze.get_cell_current()) == False
        maze.maze.set_free(3, 2)

        
        maze.maze.set_direction(1)  # Facing south
        # Initially all sides are free
        assert maze.is_leftside_valid(maze.get_cell_current()) == True
        # Set wall on left
        maze.maze.set_wall(4, 3)
        assert maze.is_leftside_valid(maze.get_cell_current()) == False
        # Set visited on left
        maze.maze.set_free(4, 3)
        maze.maze.set_visited(4, 3)
        assert maze.is_leftside_valid(maze.get_cell_current()) == False
        maze.maze.set_free(4, 3)

        maze.set_current(1, 1)
        maze.maze.set_direction(3)  # Facing north
        # Initially left is boundary
        assert maze.is_leftside_valid(maze.get_cell_current()) == False
        maze.maze.set_direction(2)  # Facing west
        # Initially left sides are free
        assert maze.is_leftside_valid(maze.get_cell_current()) == True


    def test_is_deadend(self):
        maze = GenRandom(Maze(7, 7))
        maze.set_current(3, 3)
        # Surround current cell with walls
        maze.maze.set_wall(4, 3)
        maze.maze.set_wall(3, 4)
        maze.maze.set_wall(2, 3)
        maze.maze.set_wall(3, 2)
        assert maze.is_deadend(maze.get_cell_current()) == True
        maze.clear_maze()
        maze.generate_borders()
        
        # Surround current cell with visited cells
        maze.set_current(3, 3)
        maze.maze.set_visited(4, 3)
        maze.maze.set_visited(3, 4)
        maze.maze.set_visited(2, 3)
        maze.maze.set_visited(3, 2)
        assert maze.is_deadend(maze.get_cell_current()) == True
        maze.clear_maze()
        maze.generate_borders()

        # Surround with borders and walls and visited
        maze.set_current(1, 1)
        maze.maze.set_visited(2, 1)
        maze.maze.set_wall(1, 2)
        assert maze.is_deadend(maze.get_cell_current()) == True

        # Free the wall side
        maze.maze.set_free(1, 2)
        assert maze.is_deadend(maze.get_cell_current()) == False
        maze.maze.set_wall(1, 2)

        # Free the visited side
        maze.maze.set_unvisited(2, 1)
        assert maze.is_deadend(maze.get_cell_current()) == False

    def test_is_cornered(self):
        maze = GenRandom(Maze(7, 7))
        maze.set_current(3, 3)

        # No wall in front 
        assert maze.is_cornered(maze.get_cell_current()) == False

        # Wall in front, walls on both sides
        maze.maze.set_wall(4, 3)
        maze.maze.set_wall(3, 4)
        maze.maze.set_wall(3, 2)
        assert maze.is_cornered(maze.get_cell_current()) == False
        maze.clear_maze()
        maze.generate_borders()

        # Wall in front, left free, right visited
        maze.set_current(3, 3)
        maze.maze.set_wall(4, 3)
        maze.maze.set_visited(3, 4)
        assert maze.is_cornered(maze.get_cell_current()) == True
        maze.clear_maze()
        maze.generate_borders()

        # Wall in front, right free, left wall
        maze.set_current(3, 3)
        maze.maze.set_wall(4, 3)
        maze.maze.set_wall(3, 2)
        assert maze.is_cornered(maze.get_cell_current()) == True
        maze.clear_maze()
        maze.generate_borders()

        # Wall in front, both sides free
        maze.set_current(3, 3)
        maze.maze.set_wall(4, 3)
        assert maze.is_cornered(maze.get_cell_current()) == False
        maze.clear_maze()
        maze.generate_borders()

        # Next to boundary, wall in front, right free
        maze.set_current(1, 1)
        maze.maze.set_wall(2, 1)
        assert maze.is_cornered(maze.get_cell_current()) == True
        maze.clear_maze()
        maze.generate_borders()

        # Next to boundary, free in front, right wall
        maze.set_current(1, 1)
        maze.maze.set_wall(1, 2)
        assert maze.is_cornered(maze.get_cell_current()) == False
        maze.clear_maze()

    def test_put_wall_onsides(self):
        maze = GenRandom(Maze(7, 7))
        maze.set_current(3, 3)
        maze.maze.set_direction(0)  # Facing east
        maze.put_wall_onsides(maze.get_cell_current())
        assert maze.maze.get_cell(3, 2).is_wall() == True  # Left side
        assert maze.maze.get_cell(3, 4).is_wall() == True  # Right side
        maze.clear_maze()
        maze.generate_borders()

        maze.set_current(3, 3)
        maze.maze.set_direction(1)  # Facing south
        maze.put_wall_onsides(maze.get_cell_current())
        assert maze.maze.get_cell(2, 3).is_wall() == True  # Left side
        assert maze.maze.get_cell(4, 3).is_wall() == True  # Right side
        maze.clear_maze()
        maze.generate_borders()

        maze.set_current(1, 1)
        maze.maze.set_direction(2)  # Facing west
        maze.put_wall_onsides(maze.get_cell_current())
        assert maze.maze.get_cell(1, 2).is_wall() == True  # Left side
        assert maze.maze.get_cell(1, 0).is_wall() == True  # Right side (boundary)
        maze.clear_maze()
        maze.generate_borders()

        maze.set_current(5, 5)
        maze.maze.set_direction(3)  # Facing north
        maze.put_wall_onsides(maze.get_cell_current())   
        print(maze.maze)
        assert maze.maze.get_cell(4, 5).is_wall() == True  # Left side
        assert maze.maze.get_cell(6, 5).is_wall() == True  # Right side (boundary)
        maze.clear_maze()

    def test_choose_random_direction(self):
        maze = GenRandom(Maze(7, 7))
        maze.set_current(3, 3)

        # Case 1 : Deadend (no free side)
        original_direction = 0 # Facing east
        maze.set_direction(original_direction)
        maze.maze.set_wall(4, 3)
        maze.maze.set_wall(3, 4)
        maze.maze.set_wall(2, 3)
        maze.maze.set_visited(3, 2)
        with pytest.raises(ValueError):
            maze.choose_random_direction()

        # Case 2 : Cornered (one free side)
        maze.clear_maze()
        maze.generate_borders()
        original_direction = 0 # Facing east
        maze.set_direction(original_direction)
        maze.set_current(3, 3)
        maze.maze.set_wall(4, 3)
        maze.maze.set_wall(3, 4)
        maze.maze.set_visited(2, 3)
        maze.choose_random_direction()
        assert maze.get_direction() == 3  # Turned left to face north

        # Case 3 : Cornered (one free side)
        maze.clear_maze()
        maze.generate_borders()
        original_direction = 0 # Facing east
        maze.set_direction(original_direction)
        maze.set_current(3, 3)
        maze.maze.set_wall(4, 3)
        maze.maze.set_wall(3, 2)
        maze.maze.set_visited(2, 3)
        maze.choose_random_direction()
        assert maze.get_direction() == 1  # Turned right to face south

        # Case 4 : Both sides free but wall in front
        maze.clear_maze()
        maze.generate_borders()
        original_direction = 1 # Facing south
        maze.set_direction(original_direction)
        maze.set_current(3, 3)
        maze.maze.set_wall(3, 4)
        maze.maze.set_visited(2, 3)
        chosen_directions = []
        for _ in range(10):
            maze.choose_random_direction()
            chosen_directions.append(maze.get_direction())
            maze.set_direction(original_direction)  # Reset direction
        assert all(dir in [0, 2] for dir in chosen_directions)  # Only turned left or right

        # Case 5 : Left side free and front free
        maze.clear_maze()
        maze.generate_borders()
        original_direction = 2 # Facing west
        maze.set_direction(original_direction)
        maze.set_current(3, 3)
        maze.maze.set_visited(4, 3)
        maze.maze.set_wall(3, 2)
        print(maze.maze)
        chosen_directions = []  
        for _ in range(10):
            maze.choose_random_direction()
            chosen_directions.append(maze.get_direction())
            maze.set_direction(original_direction)  # Reset direction
        assert all(dir in [1, 2] for dir in chosen_directions)  # Only turned left or kept forward

        # Case 6 : Right side free and front free
        maze.clear_maze()
        maze.generate_borders()
        original_direction = 3 # Facing north
        maze.set_direction(original_direction)
        maze.set_current(3, 3)
        maze.maze.set_visited(3, 4)
        maze.maze.set_wall(2, 3)
        chosen_directions = []  
        for _ in range(10):
            maze.choose_random_direction()
            chosen_directions.append(maze.get_direction())
            maze.set_direction(original_direction)  # Reset direction
        assert all(dir in [0, 3] for dir in chosen_directions)

        # Case 7 : All sides free except back
        maze.clear_maze()
        maze.generate_borders()
        original_direction = 0 # Facing east
        maze.set_direction(original_direction)
        maze.set_current(3, 3)
        maze.maze.set_visited(2, 3)
        chosen_directions = []  
        for _ in range(10):
            maze.choose_random_direction()
            chosen_directions.append(maze.get_direction())
            maze.set_direction(original_direction)  # Reset direction
        assert all(dir in [0, 1, 3] for dir in chosen_directions)

        # Case 8 : All sides free
        maze.clear_maze()
        maze.generate_borders()
        original_direction = 1 # Facing south
        maze.set_direction(original_direction)
        maze.set_current(3, 3)
        chosen_directions = []  
        for _ in range(10):
            maze.choose_random_direction()
            chosen_directions.append(maze.get_direction())
            maze.set_direction(original_direction)  # Reset direction
        assert all(dir in [0, 1, 2] for dir in chosen_directions)


    def test_does_forward_loops(self):

        # Scenario where it's gonna loop if we go forward
        maze = GenRandom(Maze(7, 7))
        maze.maze.set_visited(1,1)
        maze.maze.set_visited(2,1)
        maze.maze.set_visited(3,1)
        maze.maze.set_visited(3,2)
        maze.maze.set_visited(3,3)
        maze.maze.set_visited(3,4)
        maze.maze.set_visited(2,4)
        maze.maze.set_visited(1,4)
        maze.maze.set_visited(1,3)
        maze.maze.set_wall(4,2)
        maze.maze.set_wall(4,3)
        maze.maze.set_wall(2,2)
        maze.maze.set_wall(2,3)
        maze.maze.set_wall(2,5)
        maze.set_current(1,3)
        maze.set_direction(3)
        assert maze.does_forward_loops(1,3) == True
        
        # Scenario where it's not gonna loop if we go forward (because wall two cell infront)
        maze.maze.set_wall(1,1)
        assert maze.does_forward_loops(1,3) == False
        
        # Scenario where it's not gonna loop if we go forward (because wall infront)
        maze.maze.set_free(1,1)
        maze.maze.set_visited(1,1)
        maze.maze.set_wall(1,2)
        assert maze.does_forward_loops(1,3) == False




        

