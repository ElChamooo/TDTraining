from generation.Maze import Maze
from generation.GenRandomCorridors import GenRandomCorridors
from generation.GenRandomDefault import GenRandomDefault
import time

def test_performance():
    maze = Maze(61, 61)

    # Test GenRandomCorridors
    start = time.time()
    gen_corr = GenRandomCorridors(maze)
    for _ in gen_corr.generate_corridors(debug=False):
        pass
    end = time.time()
    print(f"GenRandomCorridors time: {end - start:.4f} seconds")

    gen_corr.clear_maze()

    # Test GenRandomDefault
    start = time.time()
    gen_def = GenRandomDefault(maze)
    gen_def.generate_default()
    end = time.time()
    print(f"GenRandomDefault time: {end - start:.4f} seconds")

if __name__ == "__main__":
    test_performance()