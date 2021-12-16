import sys
import numpy as np

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
    adjacent_pos = np.array([[-1,-1], [0, -1], [1, -1], [-1, 0], [1,  0], [-1, 1], [0,  1], [1,  1]])
    adjacent_pos += idx
    valid_pos = [pos for pos in adjacent_pos if is_valid_idx(pos, shape)]
    return valid_pos


def simulate_step(grid):

    num_flashes = 0

    reset_locs = []

    flash_locs = np.where(grid >= 9)
    flash_locs = list(zip(flash_locs[0], flash_locs[1]))
    curr_flashes = len(flash_locs)
    while(curr_flashes > 0):
        num_flashes += curr_flashes

        reset_locs.append(flash_locs)
        for loc in flash_locs:
            adj_idx = get_adjacent_idx(loc, grid.shape)
            for idx in adj_idx:
                grid[idx[0], idx[1]] += 1
        for loc in flash_locs:
            grid[loc] = 0

        flash_locs = np.where(grid >= 9)
        flash_locs = list(zip(flash_locs[0], flash_locs[1]))
        curr_flashes = len(flash_locs)

    grid = grid + 1
    for tmp in reset_locs:
        for loc in tmp:
            grid[loc] = 0

    return grid, num_flashes

def simulate_fixed_steps(max_steps, grid):
    total_flashes = 0
    for i in range(max_steps):
        grid, num_flashes = simulate_step(grid)
        total_flashes += num_flashes
        print(f"Step {i+1}: {num_flashes} flashes")

    print(f"{total_flashes} flashes after {max_steps} steps")

def find_sync_step(grid):
    count = 0
    while True:
        grid, num_flashes = simulate_step(grid)
        count += 1
        if num_flashes == 100:
            break
    print(f"flashes synchronized after {count} steps")


def main():
    fname = sys.argv[1]
    grid = parse_input(fname)

    simulate_fixed_steps(max_steps=100, grid=grid)
    find_sync_step(grid)
    

if __name__ == "__main__":
    main()