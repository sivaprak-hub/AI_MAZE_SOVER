import csv, os, sys
from maze_gen import Maze
import solvers
import time

sys.setrecursionlimit(10000)

def run_benchmarks():
    os.makedirs('output', exist_ok=True)
    with open('output/results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['maze_size', 'algorithm', 'time', 'path_length', 'nodes_explored'])
        
        for i in range(1, 51):
            size = 10 + (i * 2) # complexity of size
            m = Maze(size, size)
            tests = [
                    ('BFS', lambda: solvers.solve_bfs(m)),
                    ('DFS', lambda: solvers.solve_dfs(m)),
                    ('A*Man', lambda: solvers.solve_astar(m, 'Manhattan')),
                    ('A*Euc', lambda: solvers.solve_astar(m, 'Euclidean')),
                    ('MDP_value', lambda: solvers.solve_value_iteration(m)),
                    ('MDP_policy', lambda: solvers.solve_policy_iteration(m))
                ]
            
            for name, func in tests:
                start_t = time.perf_counter()
                path, explored = func()
                dt = time.perf_counter() - start_t
                writer.writerow([size, name, f"{dt:.6f}", len(path), explored])
                print(name,size)
                # save multiples of 10
                if i % 5 == 0:
                    m.draw(path, f'output/maze_{size}_{name}.png')

if __name__ == "__main__":
    run_benchmarks()