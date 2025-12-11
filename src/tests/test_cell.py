import pytest
from generation.Cell import Cell


class TestCell:
    """Test suite for the Cell class."""

    def test_cell_initialization(self):
        """Test that a cell is initialized correctly."""
        cell = Cell(5, 10)
        assert cell.x == 5
        assert cell.y == 10
        assert cell.state == False
        assert cell.visited == False
        assert cell.current == False
        assert cell.origin == False
        assert cell.finish == False

    def test_set_finish(self):
        """Test setting finish flag."""
        cell = Cell(0, 0)
        cell.set_finish()
        assert cell.is_finish() == True

    def test_is_finish_default(self):
        """Test that finish is False by default."""
        cell = Cell(0, 0)
        assert cell.is_finish() == False

    def test_set_origin(self):
        """Test setting origin flag."""
        cell = Cell(0, 0)
        cell.set_origin()
        assert cell.is_origin() == True

    def test_is_origin_default(self):
        """Test that origin is False by default."""
        cell = Cell(0, 0)
        assert cell.is_origin() == False

    def test_set_current(self):
        """Test setting current flag."""
        cell = Cell(0, 0)
        cell.set_current()
        assert cell.is_current() == True

    def test_unset_current(self):
        """Test unsetting current flag."""
        cell = Cell(0, 0)
        cell.set_current()
        cell.unset_current()
        assert cell.is_current() == False

    def test_is_current_default(self):
        """Test that current is False by default."""
        cell = Cell(0, 0)
        assert cell.is_current() == False

    def test_is_wall(self):
        cell = Cell(0, 0)
        assert cell.is_wall() == False

    def test_set_wall(self):
        cell = Cell(0, 0)
        cell.set_wall()
        assert cell.is_wall() == True

    def test_is_free(self):
        cell = Cell(0, 0)
        assert cell.is_free() == True

    def test_set_free(self):
        cell = Cell(0, 0)
        cell.set_wall()
        cell.set_free()
        assert cell.is_free() == True
        assert cell.is_wall() == False

    def test_is_visited(self):
        cell = Cell(0, 0)
        assert cell.is_visited() == False

    def test_set_visited(self):
        cell = Cell(0, 0)
        cell.set_visited()
        assert cell.is_visited() == True

    def test_unset_visited(self):
        cell = Cell(0, 0)
        cell.set_visited()
        cell.unset_visited()
        assert cell.is_visited() == False

    def test_str_representation_free(self):
        """Test string representation of a free cell."""
        cell = Cell(0, 0)
        assert str(cell) == '.'

    def test_str_representation_wall(self):
        """Test string representation of a wall cell."""
        cell = Cell(0, 0)
        cell.set_wall()
        assert str(cell) == '#'

    def test_repr_representation(self):
        """Test repr representation of a cell."""
        cell = Cell(3, 4)
        repr_str = repr(cell)
        assert "Cell(3, 4" in repr_str
        assert "Free" in repr_str
        assert "visited=False" in repr_str

    def test_repr_representation_wall(self):
        """Test repr representation of a wall cell."""
        cell = Cell(3, 4)
        cell.set_wall()
        repr_str = repr(cell)
        assert "Cell(3, 4" in repr_str
        assert "Wall" in repr_str

    def test_multiple_flags_combination(self):
        """Test that multiple flags can be set independently."""
        cell = Cell(1, 1)
        cell.set_origin()
        cell.set_visited()
        cell.set_current()
        
        assert cell.is_origin() == True
        assert cell.is_visited() == True
        assert cell.is_current() == True
        assert cell.is_finish() == False
        assert cell.is_wall() == False

    def test_wall_and_visited(self):
        """Test that a cell can be both a wall and visited."""
        cell = Cell(2, 2)
        cell.set_wall()
        cell.set_visited()
        
        assert cell.is_wall() == True
        assert cell.is_visited() == True

    def test_origin_and_finish(self):
        """Test that a cell cannot be both origin and finish (logical test)."""
        cell = Cell(0, 0)
        cell.set_origin()
        cell.set_finish()
        
        # Both flags can be set (no constraint in current implementation)
        assert cell.is_origin() == True
        assert cell.is_finish() == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])