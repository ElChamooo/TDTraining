import sys
import pygame

from generation.GenRandomDefault import GenRandomDefault
from generation.GenRandomCorridors import GenRandomCorridors
import globals 


class Button:

    global new_generation

    def __init__(self, rect, label, action=lambda: None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.action = action
        self.hover = False

    def draw(self, surf, font):
        color = (200, 200, 200) if self.hover else (160, 160, 160)
        pygame.draw.rect(surf, color, self.rect, border_radius=6)
        pygame.draw.rect(surf, (100,100,100), self.rect, 2, border_radius=6)
        txt = font.render(self.label, True, (20,20,20))
        txt_rect = txt.get_rect(center=self.rect.center)
        surf.blit(txt, txt_rect)

    def handle_event(self, event, maze=None):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action(maze)

def action_generate_default(maze):    
    print(f"Action generate default called") 
    globals.new_generation = GenRandomDefault(maze).generate_default(debug=False)  
    print("Generated new random maze")

def action_generatecorridors(maze):
    print(f"Action generate corridors called")
    globals.new_generation = GenRandomCorridors(maze).generate_corridors(debug=False)
    print("Corridor generator created")

def action_generatecorridors_DEBUG(maze):
    globals.new_generation = GenRandomCorridors(maze).generate_corridors(debug=True)
    print("Corridor generator created (DEBUG)")

def action_solve_bfs(maze):
    print("Solve BFS (not implemented yet)")

def action_solve_dfs(maze):
    print("Solve DFS (not implemented yet)")

def action_clear(maze):
    print("Clear path (not implemented yet)")

def action_quit(maze):
    print("Quitting...")
    pygame.quit()
    sys.exit(0)
