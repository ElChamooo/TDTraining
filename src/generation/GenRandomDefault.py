from generation.GenRandom import GenRandom

class GenRandomDefault(GenRandom):
    def __init__(self, maze):
        super().__init__(maze)

    def generate_default(self, debug=False):
        import random
        self.clear_maze()
        self.generate_borders()
        for y in range(self.maze.get_height()):
            for x in range(self.maze.get_width()):
                if self.maze.get_cell(x, y).is_wall():
                    continue  # Skip border cells
                if random.random() < 0.3:
                    self.maze.set_wall(x, y)
                else:
                    self.maze.set_free(x, y)