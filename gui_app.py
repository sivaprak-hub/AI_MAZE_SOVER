import tkinter as tk
from tkinter import messagebox
import argparse
import solvers
from maze_gen import Maze

class MazeGUI:
    def __init__(self, root, size, algo_name):
        self.root = root
        self.root.title(f"Maze Traversal: {algo_name.upper()} ({size}x{size})")
        
        self.size = size
        self.offset = 800 // size 
        self.canvas = tk.Canvas(root, width=size*self.offset, height=size*self.offset, bg="white")
        self.canvas.pack(padx=10, pady=10)

        # 1. Use your existing Maze class
        self.maze = Maze(size, size)
        self.draw_walls()

        # 2. Use your existing solvers
        self.path, _ = self.get_solution(algo_name)
        
        if self.path:
            self.animate_path(0)
        else:
            messagebox.showwarning("No Path", "No solution found.")

    def get_solution(self, algo):
        # Maps CLI strings to your functions in solvers.py
        algo_map = {
            'bfs': lambda: solvers.solve_bfs(self.maze),
            'dfs': lambda: solvers.solve_dfs(self.maze),
            'astar': lambda: solvers.solve_astar(self.maze, 'Manhattan'),
            'mdp': lambda: solvers.solve_value_iteration(self.maze)
        }
        return algo_map.get(algo.lower(), lambda: ([], 0))()

    def draw_walls(self):
        """Draws the grid based on your walls dictionary."""
        for r in range(self.size):
            for c in range(self.size):
                x, y = c * self.offset, r * self.offset
                w = self.maze.walls[r][c]
                if w['N']: self.canvas.create_line(x, y, x + self.offset, y, width=2)
                if w['W']: self.canvas.create_line(x, y, x, y + self.offset, width=2)

    def animate_path(self, index):
        """Draws a continuous line from the previous node to the current one."""
        if index > 0 and index < len(self.path):
            # Get previous and current coordinates
            prev_r, prev_c = self.path[index - 1]
            curr_r, curr_c = self.path[index]

            # Calculate center points for the line
            x1 = prev_c * self.offset + self.offset // 2
            y1 = prev_r * self.offset + self.offset // 2
            x2 = curr_c * self.offset + self.offset // 2
            y2 = curr_r * self.offset + self.offset // 2

            # Draw the line segment
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3, capstyle=tk.ROUND)
            
        if index < len(self.path) - 1:
            # Continue animation
            self.root.after(30, self.animate_path, index + 1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=25)
    parser.add_argument('--algo', type=str, default='astar')
    args = parser.parse_args()

    root = tk.Tk()
    app = MazeGUI(root, args.size, args.algo)
    root.mainloop()