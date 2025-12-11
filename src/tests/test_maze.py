import pytest
from generation.Maze import Maze


class TestMaze:

    def test_maze_initialization(self):
        maze = Maze(10, 15)
        assert maze.get_width() == 10
        assert maze.get_height() == 15
        assert maze.get_direction() == 0  # Initial direction should be 0 (east)

    def test_all_cells_initial_state(self):
        maze = Maze(5, 5)
        for x in range(5):
            for y in range(5):
                cell = maze.get_cell(x, y)
                assert not cell.is_visited()
                assert not cell.is_current()

    def test_set_and_get_direction(self):
        maze = Maze(5, 5)
        maze.set_direction(2)
        assert maze.get_direction() == 2
        maze.set_direction(5)  # Should wrap around
        assert maze.get_direction() == 1

    def test_set_and_get_current(self):
        maze = Maze(5, 5)
        maze.set_current(2, 3)
        current = maze.get_current()
        assert current.x == 2
        assert current.y == 3
        assert current.is_visited() == True
        assert current.is_current() == True
        # Ensure previous current is unset
        maze.set_current(3, 3)
        assert maze.get_cell(2, 3).is_current() == False
        assert maze.get_cell(3, 3).is_current() == True

    def test_set_and_get_origin(self):
        maze = Maze(5, 5)
        maze.set_origin(1, 1)
        origin = maze.get_origin()
        assert origin.x == 1
        assert origin.y == 1
        assert origin.is_origin() == True

    def test_set_and_get_finish(self):
        maze = Maze(5, 5)
        maze.set_finish(4, 4)
        finish = maze.get_finish()
        assert finish.x == 4
        assert finish.y == 4
        assert finish.is_finish() == True

    def test_set_and_get_visited(self):
        maze = Maze(5, 5)
        maze.set_visited(2, 2)
        cell = maze.get_cell(2, 2)
        assert cell.is_visited() == True
        maze.set_unvisited(2, 2)
        assert cell.is_visited() == False

    def test_set_and_get_wall_and_free(self):
        maze = Maze(5, 5)
        maze.set_wall(3, 3)
        cell = maze.get_cell(3, 3)
        assert cell.is_wall() == True
        maze.set_free(3, 3)
        assert cell.is_free() == True
        with pytest.raises(ValueError):
            maze.set_free(0, 0)  # Boundary cell
        with pytest.raises(ValueError):
            maze.set_free(4, 0)  # Boundary cell
        with pytest.raises(ValueError):
            maze.set_free(0, 8)  # Boundary cell
        with pytest.raises(IndexError):
            maze.set_wall(10, 2)  # Boundary cell
        with pytest.raises(IndexError):
            maze.set_wall(1, -1)  # Boundary cell

    def test_is_boundary(self):
        maze = Maze(5, 5)
        assert maze.is_boundary(0, 0) == True
        assert maze.is_boundary(4, 4) == True
        assert maze.is_boundary(2, 2) == False

    def test_is_valid_next_path(self):
        maze = Maze(5, 5)
        maze.set_current(2, 2)
        assert maze.is_valid_next_path(2, 3) == True
        assert maze.is_valid_next_path(2, 1) == True
        assert maze.is_valid_next_path(1, 2) == True
        assert maze.is_valid_next_path(3, 2) == True
        maze.set_wall(2, 3)
        assert maze.is_valid_next_path(2, 3) == False
        maze.set_visited(2, 1)
        assert maze.is_valid_next_path(2, 1) == False
        assert maze.is_valid_next_path(0, 0) == False  # Boundary cell

    def test_is_forward_left_right_valid(self):
        maze = Maze(5, 5)
        maze.set_current(2, 2)
        maze.set_direction(2)
        # Facing west
        assert maze.is_forward_valid(maze.get_current()) == True
        assert maze.is_leftside_valid(maze.get_current()) == True
        assert maze.is_rightside_valid(maze.get_current()) == True
        maze.set_wall(1, 2)  # Forward
        maze.set_wall(2, 3)  # Left
        maze.set_visited(2, 1)  # Right
        assert maze.is_forward_valid(maze.get_current()) == False
        assert maze.is_leftside_valid(maze.get_current()) == False
        assert maze.is_rightside_valid(maze.get_current()) == False

    def test_set_wall_on_sides(self):
        maze = Maze(5, 5)
        maze.set_current(2, 2)
        maze.set_direction(0)  # Facing east
        maze.set_wall_on_left()
        assert maze.get_cell(2, 1).is_wall() == True
        maze.set_wall_on_right()
        assert maze.get_cell(2, 3).is_wall() == True

    def test_move_forward(self):
        maze = Maze(5, 5)
        maze.set_current(2, 2)
        maze.set_direction(0)  # Facing east
        maze.move_forward()
        current = maze.get_current()
        assert current.x == 3
        assert current.y == 2
        maze.set_direction(1)  # Facing south
        maze.move_forward()
        current = maze.get_current()
        assert current.x == 3
        assert current.y == 3
        maze.set_direction(2)  # Facing west
        maze.move_forward()
        current = maze.get_current()
        assert current.x == 2
        assert current.y == 3
        maze.set_direction(3)  # Facing north
        maze.move_forward()
        current = maze.get_current()
        assert current.x == 2
        assert current.y == 2
        # Test moving into boundary
        maze.set_current(1, 1)
        maze.set_direction(3)  # Facing north
        with pytest.raises(ValueError):
            maze.move_forward()  # Should raise error

    def test_maze_boundaries(self):
        maze = Maze(5, 5)
        with pytest.raises(IndexError):
            maze.get_cell(-1, 0)
        with pytest.raises(IndexError):
            maze.get_cell(0, -1)
        with pytest.raises(IndexError):
            maze.get_cell(5, 5)
        with pytest.raises(IndexError):
            maze.get_cell(6, 6)

    def test_clear_maze(self):
        maze = Maze(5, 5)
        maze.set_current(2, 2)
        maze.set_visited(2, 2)
        maze.set_origin(1, 1)
        maze.set_finish(3, 3)
        maze.clear()
        assert maze.get_current() is None
        assert maze.get_origin() is None
        assert maze.get_finish() is None
        for x in range(5):
            for y in range(5):
                assert not maze.get_cell(x, y).is_visited()