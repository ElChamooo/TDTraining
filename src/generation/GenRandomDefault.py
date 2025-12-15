from generation.GenRandom import GenRandom

class GenRandomDefault(GenRandom):
    def __init__(self, maze):
        super().__init__(maze)

    def generate_default(self, debug=False):
        import random
        self.clear_maze()
        self.generate_borders()
        self.set_current(1,1)
        self.set_origin(self.get_cell_current().x, self.get_cell_current().y)
        self.set_finish(self.get_width()-2, self.get_height()-2)
        for y in range(self.maze.get_height()):
            for x in range(self.maze.get_width()):
                if self.maze.get_cell(x, y).is_wall():
                    continue  # Skip border cells
                if random.random() < 0.3:
                    self.maze.set_wall(x, y)
                    action = "Put a wall"
                else:
                    self.maze.set_free(x, y)
                    action = "Dont put a wall"
                yield action