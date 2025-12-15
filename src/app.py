from interface.ui import *
from generation.Maze import Maze
from generation.GenRandomDefault import GenRandomDefault
from generation.GenRandomCorridors import GenRandomCorridors
import globals 
import argparse


generating= False
resolving=False
playing=True

def main(debug=False):
    
    
    global generation
    
    print(f"generating: {generating}, playing: {playing}, resolving: {resolving}")

    print("Starting Maze Solver Interface...")
    pygame.init()
    pygame.display.set_caption("Maze Solver - Interface")

    param = Param()
    param.updateparamfromfile()
    print(f"Param loaded: width={param.get_width()}, height={param.get_height()}, maze_width={param.get_maze_width()}, nav_height={param.get_nav_height()}")
    
    screen = create_screen()
    print("Screen created")

    # create buttons once
    btns = create_buttons()
    maze = Maze(51,41)
    maze.set_current(1,1)
    maze.generate_borders()

    # Initial draw to show the UI
    screen.fill((240,240,240))
    screen = assemble_ui(screen, btns, maze)
    pygame.display.flip()
    print("Initial draw done")

    if debug:
        globals.new_generation = GenRandomCorridors(maze).generate_corridors(debug=True)
    else:
        # Start with empty maze, generation triggered by buttons
        pass




    clock = pygame.time.Clock()
    running = True
    frame = 0
    while running:
        frame += 1

#-------------------------------------1. How many FPS-------------------------------------#

        clock.tick(60)

#-------------------------------------2. Handle Player input-------------------------------------#

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_buttons(btns, event, maze)
            action=handle_key_input(event, maze, debug)

#-------------------------------------3. Modifying env variable-------------------------------------#

        # if resolving:
        #     print("Resolving")
        #     pass   
        if globals.new_generation is not None:
            generation=globals.new_generation
            globals.new_generation = None
            set_generating()



#-------------------------------------4. Actions-------------------------------------#

        if generating:
            for _ in range(10):  # Step 10 times per frame for faster generation
                try:
                    next(generation)
                except StopIteration:
                    set_playing()
                    print("Visual maze generation finished")
                    break
                except Exception as e:
                    print(f"Error during generation: {e}")
                    set_playing()
                    break
        elif resolving: 
            pass
            # A implémenter
        elif playing:
            token=False
            match action:
                case "up":
                    token=True
                    maze.set_direction(3)
                case "left":
                    token=True
                    maze.set_direction(2)
                case "down":
                    token=True
                    maze.set_direction(1)
                case "right":
                    token=True
                    maze.set_direction(0)
            if maze.get_cell_front(maze.get_current().x, maze.get_current().y).is_free() and token and frame%5==0:
                maze.move_forward()
        

#-------------------------------------4 Update the screen-------------------------------------#



        
        screen.fill((240,240,240))
        screen = assemble_ui(screen, btns, maze)
        pygame.display.flip()
        # if frame % 60 == 0:
        #     print(f"generation {generation}")

    pygame.quit()

def handle_buttons(btns, event, maze):
    for b in btns:
        b.handle_event(event, maze)

    
def handle_key_input(event, maze, debug):
    if event.type == pygame.KEYDOWN and debug:
        if event.key == pygame.K_r:         # reset
            maze.clear()
            globals.new_generation = GenRandomCorridors(maze).generate_corridors(debug=True)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            return "up"
        if event.key == pygame.K_RIGHT:
            return "right"
        if event.key == pygame.K_DOWN:
            return "down"
        if event.key == pygame.K_LEFT:
            return "left"


def set_generating():
    global playing, resolving, generating
    playing=False
    resolving=False
    generating=True
    
def set_resolving():
    global playing, resolving, generating
    playing=False
    resolving=True
    generating=False
    
def set_playing():
    global playing, resolving, generating
    playing=True
    resolving=False
    generating=False

    




    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Activer le mode debug")
    args = parser.parse_args()

    main(debug=args.debug)



# # handle events and forward them to buttons
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     for b in btns:
    #         b.handle_event(event, maze)
    #     if event.type == pygame.KEYDOWN and debug:
    #         if event.key == pygame.K_r:         # reset
    #             maze.clear()
    #             new_generation = GenRandomCorridors(maze).generate_corridors(debug=True)

