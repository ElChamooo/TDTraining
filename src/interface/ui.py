"""
Minimal pygame UI:
- top nav bar
- left: maze visualisation
- right: control buttons (Generate / Solve BFS / Solve DFS / Clear / Quit)
Designed to work with generation.depth_first.generate and algorithmes.bfs.bfs when present.
"""

import pygame
from interface.Button import Button, action_generate_default, action_solve_bfs, action_solve_dfs, action_clear, action_quit, action_generatecorridors, action_generatecorridors_DEBUG
from interface.Param import Param


param=Param()
param.updateparamfromfile()

def create_screen():
    screen = pygame.display.set_mode((param.get_width(), param.get_height()))
    return screen

def draw_navbar(screen):
    pygame.draw.rect(screen, (30,30,30), (0,0,param.get_width(),param.get_nav_height()))
    font = pygame.font.SysFont(None, 28)
    title = font.render("Maze Solver — Interface", True, (230,230,230))
    screen.blit(title, (12, 10))
    return screen

#--------------------------------------A MODIFIER--------------------------------------#
def draw_grid(screen, maze, origin, path=None, start=None, goal=None):
    x0,y0 = origin
    cell_size=min(param.get_maze_width() // maze.get_width(), (param.get_height() - param.get_nav_height()) // maze.get_height())
    h = maze.get_height(); w = maze.get_width()
    path_set = set(path or [])
    for gy in range(h):
        for gx in range(w):
            rect = pygame.Rect(x0 + gx*cell_size, y0 + gy*cell_size, cell_size, cell_size)
            if maze.get_cell(gx,gy).is_origin():
                color = (40,200,40)
            elif maze.get_cell(gx,gy).is_finish():
                color = (200,40,40)
            elif maze.get_cell(gx, gy).is_current():
                color = (0, 100, 255)
            elif maze.get_cell(gx, gy).is_visited():
                color = (173, 216, 230)
            elif maze.get_cell(gx, gy).is_wall():
                color = (10,10,10)
            else:
                color = (240,240,240)
            pygame.draw.rect(screen, color, rect)
    # grid lines
    for gy in range(h+1):
        pygame.draw.line(screen, (200,200,200), (x0, y0+gy*cell_size), (x0+w*cell_size, y0+gy*cell_size), 1)
    for gx in range(w+1):
        pygame.draw.line(screen, (200,200,200), (x0+gx*cell_size, y0), (x0+gx*cell_size, y0+h*cell_size), 1)
    return screen

def create_buttons():
    btns = []

    margin_x = param.get_maze_width() + 16
    bx = margin_x; by = param.get_nav_height() + 16
    bw = param.get_control_width() - 32; bh = 40; gap = 12

    # Simplified action_generate: only regenerate maze, no path/start/goal handling
    

    btns.append(Button((bx, by, bw, bh), "Generate random Maze", action_generate_default)); by += bh+gap
    btns.append(Button((bx, by, bw, bh), "Generate Smart Maze", action_generatecorridors)); by += bh+gap
    btns.append(Button((bx, by, bw, bh), "Generate Smart Maze [DEBUG]", action_generatecorridors_DEBUG)); by += bh+gap
    btns.append(Button((bx, by, bw, bh), "[WIP] Solve BFS", action_solve_bfs)); by += bh+gap
    btns.append(Button((bx, by, bw, bh), "[WIP] Solve DFS", action_solve_dfs)); by += bh+gap
    btns.append(Button((bx, by, bw, bh), "[WIP] Clear Path", action_clear)); by += bh+gap
    btns.append(Button((bx, by, bw, bh), "Quit", action_quit)); by += bh+gap
    return btns

def draw_buttons(screen, buttons):
    for b in buttons:
        b.draw(screen, pygame.font.SysFont(None, 20))
    return screen

def create_controls(screen, btns=None):
    pygame.draw.rect(screen, 
                     (235,235,235), 
                     (param.get_maze_width() + 8, param.get_nav_height()+8, param.get_control_width()-16, param.get_height()-param.get_nav_height()-16), 
                     border_radius=8
                    )
    # si btns fourni, on ne crée pas de nouveaux boutons (évite recréation chaque frame)
    if btns is None:
        btns = create_buttons()
    screen = draw_buttons(screen, btns)
    return screen

def create_maze_area(screen):
    pygame.draw.rect(screen, 
                     (220,220,220), 
                     (8, param.get_nav_height()+8, param.get_maze_width()-16, param.get_height()-param.get_nav_height()-16), 
                     border_radius=8
                    )
    return screen

def create_debug_area(screen):
    pygame.draw.rect(screen, 
                     (200,200,200), 
                     (8, param.get_nav_height()+8, param.get_width_debug()-16, param.get_height_debug()-16), 
                     border_radius=8
                    )
    return screen

def assemble_ui(screen, btns=None, maze=None):    
    # navbar
    screen = draw_navbar(screen)
    # left area background
    screen = create_maze_area(screen)
    screen = draw_grid(screen, maze, (8, param.get_nav_height()+8))
    # right area background + draw boutons (n'en crée pas si btns fourni)
    screen = create_controls(screen, btns)
    return screen
    






    # # maze parameters (cells)
    # cells_x = 41
    # cells_y = 31
    # 
    # left_margin = (MAZE_W - cell_size*cells_x) // 2
    # top_margin = NAV_H + (HEIGHT - NAV_H - cell_size*cells_y)//2

    
    # # state
    # generator = GenRandom(Maze(cells_x, cells_y))
    # generator.generate()
    # grid = [[1 if cell.is_wall else 0 for cell in row] for row in generator.maze.grid]
    # start = (0, 0)
    # goal = (cells_x - 1, cells_y - 1)
    # path = None
    # status = "Ready"

    # # Actions
    # def action_generate():
    #     nonlocal grid, start, goal, path, status
    #     grid, start, goal = generate_maze(cells_x, cells_y)
    #     path = None
    #     status = "Generated new maze"

    # def action_solve_bfs():
    #     nonlocal path, status
    #     status = "Solving (BFS)..."
    #     pygame.display.set_caption("Solving (BFS) ...")
    #     solution = solver_bfs(grid, start, goal)
    #     path = solution
    #     status = "Solved (BFS)" if solution else "No path (BFS)"

    # def action_solve_dfs():
    #     nonlocal path, status
    #     status = "Solving (DFS)..."
    #     pygame.display.set_caption("Solving (DFS) ...")
    #     # try to call solver_dfs if available else fallback to BFS
    #     if solver_dfs:
    #         solution = solver_dfs(grid, start, goal)
    #     else:
    #         solution = solver_bfs(grid, start, goal)
    #     path = solution
    #     status = "Solved (DFS)" if solution else "No path (DFS)"


    # 

    

    # 

    #     
    #     # draw maze
    #     origin = (left_margin + 8, top_margin)
    #     draw_grid(screen, grid, cell_size, origin, path, start, goal)

    #     # draw controls title & buttons
    #     heading = big_font.render("Controls", True, (30,30,30))
    #     screen.blit(heading, (MAZE_W + 24, NAV_H + 18))
    #     for b in btns:
    #         b.draw(screen, font)

    #     # status at bottom of control area
    #     status_txt = font.render(status, True, (50,50,50))
    #     screen.blit(status_txt, (MAZE_W + 24, HEIGHT - 36))

    #     # update HUD (maze size)
    #     hud = font.render(f"Maze: {cells_x}x{cells_y}  Path: {'yes' if path else 'no'}", True, (230,230,230))
    #     screen.blit(hud, (WIDTH - 240, 14))

    #     pygame.display.flip()


