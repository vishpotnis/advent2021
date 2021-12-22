import sys
import numpy as np
from collections import deque


def parse_input(fname):
    grid = []
    with open(fname) as file:
        for line in file.readlines():
            grid.append([int(x) for x in line.strip()])
    return np.array(grid)

def is_valid_idx(idx, shape):
    if idx[0] < 0 or idx[0] >= shape[0]:
        return False
    if idx[1] < 0 or idx[1] >= shape[1]:
        return False
    return True

def get_adjacent_idx(idx, shape):
    adjacent_pos = np.array([[0, -1], [-1, 0], [1,  0], [0,  1]])
    adjacent_pos += idx
    valid_pos = [pos for pos in adjacent_pos if is_valid_idx(pos, shape)]
    return valid_pos

def calculate_risk_bfs(grid, risk_grid):
    q = deque()
    start = (0,0)

    q.append([start, 0, []])

    while q:
        print(f"q length: {len(q)}")
        curr = q.popleft()
        coord = curr[0]
        risk = curr[1]
        visited = curr[2]

        visited.append(coord)
        risk += grid[coord]

        if risk_grid[coord] < risk:
            continue
        risk_grid[coord] = risk

        adj_idx = get_adjacent_idx(coord, grid.shape)

        for idx in adj_idx:
            idx_coord = (idx[0], idx[1])
            if idx_coord not in visited:
                q.append([idx_coord, risk, visited.copy()])
    
    return risk_grid

def get_lowest_cost_coord(risk_grid):
    min_idx = np.where(risk_grid==np.min(risk_grid))
    return (min_idx[0][0], min_idx[1][0])

def calculate_risk_dijkstra(grid, risk_grid):
    visited = []

    risk_grid_min = np.ones(shape=grid.shape, dtype=np.int64) * np.iinfo(np.int64).max

    risk_grid[0][0] = 0
    risk_grid_min[0][0] = 0
    num_nodes = grid.shape[0] * grid.shape[1]

    while len(visited) != num_nodes:

        print(f"{len(visited)}/{num_nodes}")

        coord = get_lowest_cost_coord(risk_grid_min)
        visited.append(coord)
        risk_grid_min[coord] = np.iinfo(np.int64).max

        curr_risk = risk_grid[coord]
        adj_idx = get_adjacent_idx(coord, grid.shape)
        for idx in adj_idx:
            idx_coord = (idx[0], idx[1])
            if curr_risk + grid[idx_coord] < risk_grid[idx_coord]:
                risk_grid[idx_coord] = curr_risk + grid[idx_coord]
                risk_grid_min[idx_coord] = curr_risk + grid[idx_coord]

    return risk_grid

def repeat_grid(grid):
    print(grid)

    tmp = np.copy(grid)
    for _ in range(4):
        tmp = tmp + 1
        tmp[tmp==10] = 1
        grid = np.append(grid, tmp, axis=1)

    tmp = np.copy(grid)
    for _ in range(4):
        tmp = tmp + 1
        tmp[tmp==10] = 1
        grid = np.append(grid, tmp, axis=0)

    return grid



def main():
    fname = sys.argv[1]
    grid = parse_input(fname)    
    grid = repeat_grid(grid)  # Part 2

    risk_grid = np.ones(shape=grid.shape, dtype=np.int64) * np.iinfo(np.int64).max

    risk_grid = calculate_risk_dijkstra(grid, risk_grid)
    print(f"Lowest Risk Path: {risk_grid[-1][-1] - risk_grid[0][0]}")

if __name__ == "__main__":
    main()