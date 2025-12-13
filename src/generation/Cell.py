class Cell:

    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.state=False # False for empty, True for wall
        self.visited=False
        self.current=False
        self.origin=False
        self.finish=False

    def set_finish(self):  
        self.finish=True

    def is_finish(self) -> bool:
        return self.finish

    def set_origin(self):
        self.origin=True

    def is_origin(self) -> bool:
        return self.origin

    def set_current(self):
        self.current=True
    
    def unset_current(self):
        self.current=False

    def is_current(self) -> bool:
        return self.current

    def is_wall(self) -> bool:
        return self.state

    def is_free(self) -> bool:
        return not self.state
    
    def is_visited(self) -> bool:
        return self.visited

    def set_visited(self):
        self.visited = True

    def unset_visited(self):
        self.visited = False

    def set_wall(self):
        self.state = True

    def set_free(self):
        self.state = False

    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return f"Cell({self.x}, {self.y}, state={'Wall' if self.state else 'Free'}, visited={self.visited}, current={self.current}, origin={self.origin}, finish={self.finish})"