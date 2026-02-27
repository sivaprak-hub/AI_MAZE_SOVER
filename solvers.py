import heapq
from collections import deque


def solve_bfs(maze):
    start, goal = (0, 0), (maze.rows - 1, maze.cols - 1)
    queue = deque([start])
    path = {start: None}
    explored = 0
    while queue:
        c = queue.popleft()
        explored += 1
        if c == goal:
            break
        for nbr in maze.get_neighbors(*c):
            if nbr not in path:
                path[nbr] = c
                queue.append(nbr)
    return reconstruct(path, goal), explored


def solve_dfs(maze):
    start, goal = (0, 0), (maze.rows - 1, maze.cols - 1)
    stack = [start]
    path = {start: None}
    explored = 0
    while stack:
        c = stack.pop()
        explored += 1
        if c == goal:
            break
        for nbr in maze.get_neighbors(*c):
            if nbr not in path:
                path[nbr] = c
                stack.append(nbr)
    return reconstruct(path, goal), explored

def get_dist(p1, p2, mode='manhattan'):
    y1, x1 = p1
    y2, x2 = p2
    if mode.lower().startswith('man'):
        return abs(y1 - y2) + abs(x1 - x2)
    # Euclidean distance
    return ((y1 - y2)**2 + (x1 - x2)**2)**0.5

def solve_astar(maze, heuristic='Manhattan'):
    start = (0, 0)
    target = (maze.rows - 1, maze.cols - 1)
    queue = [(0, start)]
    parent_map = {start: None}
    g_score = {start: 0}
    nodes_visited = 0

    while queue:
        _, current = heapq.heappop(queue)
        nodes_visited += 1

        if current == target:
            break

        for neighbor in maze.get_neighbors(*current):
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                h_score = get_dist(neighbor, target, mode=heuristic)
                f_score = tentative_g + h_score
                
                heapq.heappush(queue, (f_score, neighbor))
                parent_map[neighbor] = current

    if target not in parent_map:
        return None, nodes_visited

    return reconstruct(parent_map, target), nodes_visited


def reconstruct(came_from, goal):
    path, curr = [], goal
    while curr is not None:
        path.append(curr)
        curr = came_from.get(curr)
    return path[::-1]


def _extract_path_bfs(maze, V, goal):
    start = (0, 0)
    heap = [(-V[start], start)]
    came_from = {start: None}
    while heap:
        _, curr = heapq.heappop(heap)
        if curr == goal:
            break
        for nbr in maze.get_neighbors(*curr):
            if nbr not in came_from:
                came_from[nbr] = curr
                heapq.heappush(heap, (-V[nbr], nbr))
    if goal not in came_from:
        return [start]
    path, curr = [], goal
    while curr is not None:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()
    return path

#mdp value
def solve_value_iteration(maze, gamma=0.99, epsilon=0.001, max_iter=10000):
    rows, cols = maze.rows, maze.cols
    goal = (rows - 1, cols - 1)
    terminal_reward = float(rows * cols * 10)
    V = {(r, c): 0.0 for r in range(rows) for c in range(cols)}
    V[goal] = terminal_reward

    for iteration in range(max_iter):
        delta = 0.0
        new_V = V.copy()
        new_V[goal] = terminal_reward
        for r in range(rows):
            for c in range(cols):
                if (r, c) == goal:
                    continue
                nbrs = maze.get_neighbors(r, c)
                if not nbrs:
                    continue
                action_values = [
                    (-1.0 if (nr, nc) != goal else 0.0) + gamma * V[(nr, nc)]
                    for nr, nc in nbrs
                ]
                best = max(action_values)
                delta = max(delta, abs(V[(r, c)] - best))
                new_V[(r, c)] = best
        V = new_V
        if delta < epsilon:
            break

    return _extract_path_bfs(maze, V, goal), rows * cols


def solve_policy_iteration(maze, gamma=0.99, eval_epsilon=0.01, max_iter=500):
    rows, cols = maze.rows, maze.cols
    goal = (rows - 1, cols - 1)
    states = [(r, c) for r in range(rows) for c in range(cols)]
    terminal_reward = float(rows * cols * 10)
    policy = {}
    for s in states:
        nbrs = maze.get_neighbors(*s)
        policy[s] = nbrs[0] if nbrs else s
    V = {s: 0.0 for s in states}
    V[goal] = terminal_reward

    for outer in range(max_iter):
        for _ in range(10000):
            delta = 0.0
            for s in states:
                if s == goal:
                    V[s] = terminal_reward
                    continue
                next_s = policy[s]
                step_r = 0.0 if next_s == goal else -1.0
                new_v = step_r + gamma * V[next_s]
                delta = max(delta, abs(V[s] - new_v))
                V[s] = new_v
            if delta < eval_epsilon:
                break
        policy_stable = True
        for s in states:
            if s == goal:
                continue
            old_action = policy[s]
            nbrs = maze.get_neighbors(*s)
            if nbrs:
                best_nbr = max(nbrs, key=lambda n: V[n])
                policy[s] = best_nbr
                if best_nbr != old_action:
                    policy_stable = False
        if policy_stable:
            break
    return _extract_path_bfs(maze, V, goal), rows * cols