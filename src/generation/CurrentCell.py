from generation.Cell import Cell

class CurrentCell(Cell):
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.direction = direction  # 0: east, 1: south, 2: west, 3: north
    
    def forward(self):
        match self.direction:
            case 0:  # east
                self.x += 1
            case 1:  # south
                self.y += 1
            case 2:  # west
                self.x -= 1
            case 3:  # north
                self.y -= 1

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def turn_left(self):
        self.direction = (self.direction - 1) % 4

    def turnback(self):
        self.direction = (self.direction + 2) % 4