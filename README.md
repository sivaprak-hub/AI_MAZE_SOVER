# AI Maze Solver: Search vs. MDP Analysis

This project explores computational pathfinding and decision-making within "perfect" maze environments.

## Overview
The goal is to analyze the performance trade-offs between classical **State-Space Search** and **Markov Decision Processes (MDP)**.

### Implemented Algorithms:
1.  **Breadth-First Search (BFS)**: Optimal pathfinding using uninformed search.
2.  **Depth-First Search (DFS)**: Memory-efficient exploration (non-optimal).
3.  **A* Search (Manhattan)**: Informed search optimized for grid-based movement.
4.  **A* Search (Euclidean)**: Informed search using straight-line distance.
5.  **MDP Value & Policy Iteration**: Global policy optimization using Bellman updates.

## Project Structure
* `maze_gen.py`: Maze generation using Recursive Backtracking (Iterative DFS).
* `solvers.py`: Core implementation of the 5 solver algorithms.
* `main.py`: Benchmarking script for automated 50-maze experiment.
* `gui_app.py`: Visualization tool for real-time algorithm demonstration.
* `output/`: Contains generated solution PNGs and `results.csv`.

## Installation & Usage
Ensure you have Python 3 and the Pillow library installed for visualization.

```bash
# Install dependencies
pip install Pillow

# Run the automated benchmarking suite
python3 main.py

# Run the GUI for a live demo
python3 gui_app.py
