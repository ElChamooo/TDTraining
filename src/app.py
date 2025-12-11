from interface.ui import *
from generation.Maze import Maze
from generation.GenRandomDefault import GenRandomDefault
from generation.GenRandomCorridors import GenRandomCorridors
import argparse


def main(debug=False):

    if debug:
        print("[DEBUG] Mode debug activé")
        step_mode = True          # On attend que l'utilisateur appuie
        auto_play = False         # Mode "continue" en automatique
        
    print("Starting Maze Solver Interface...")
    pygame.init()
    pygame.display.set_caption("Maze Solver - Interface")

    param = Param()
    param.updateparamfromfile()
    
    screen = create_screen()

    # create buttons once
    btns = create_buttons()
    maze=Maze(41,41)

    if debug:
        generation = GenRandomCorridors(maze).generate_corridors(debug=True)
    else:
        generation=GenRandomDefault(maze)
        generation.generate_default()

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)

        # handle events and forward them to buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for b in btns:
                b.handle_event(event, maze)
            # --- CONTRÔLES DEBUG ---
            if event.type == pygame.KEYDOWN and debug:
                if event.key == pygame.K_SPACE:       # un pas
                    step_mode = True
                elif event.key == pygame.K_c:         # continuer automatiquement
                    auto_play = True
                elif event.key == pygame.K_p:         # pause
                    auto_play = False
                elif event.key == pygame.K_r:         # reset
                    maze.clear_maze()
                    generation = GenRandomCorridors(maze).generate_corridors(debug=True)
                    auto_play = False

            if debug:
                if step_mode or auto_play:
                    try:
                        action = next(generation)
                        print("[DEBUG] action:", action)
                    except StopIteration:
                        auto_play = False

                    step_mode = False  # on exécute un pas et on attend le suivant


        # draw UI each frame (but create_controls won't recreate buttons)
        screen.fill((240,240,240))
        screen = assemble_ui(screen, btns, maze)
        pygame.display.flip()

    pygame.quit()

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Activer le mode debug")
    args = parser.parse_args()

    main(debug=args.debug)
