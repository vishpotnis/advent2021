import numpy as np

def parse_input(fname):
    grid = []
    with open(fname) as file:        
        for line in file.readlines():
            grid.append([int(x) for x in line.strip()])
    grid = np.array(grid, dtype=np.int32)
    return grid

def calculate_low_points(grid):
    low_points = []
    num_rows, num_cols = grid.shape
    for row in range(num_rows):
        for col in range(num_cols):
            if isLowPoint(grid, (row, col)):
                low_points.append((row,col))
    return low_points

def get_adj_points(point):
    row, col = point
    adj_points = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    return adj_points

def isLowPoint(grid, point):
    adj_points = get_adj_points(point)    
    for adj_point in adj_points:
        if isValidCoord(grid.shape, adj_point) and grid[point] >= grid[adj_point]:
            return False
    return True

def isValidCoord(shape, point):
    if point[0] < 0 or point[0] >= shape[0]:
        return False
    if point[1] < 0 or point[1] >= shape[1]:
        return False
    return True

def basin_size_bfs_search(grid, point):
    queue = [point]
    visited = [point]
    size = 0
    while queue:
        curr_point = queue.pop(0)        
        size += 1
        adj_points = get_adj_points(curr_point)
        for adj_point in adj_points:
            if isValidCoord(grid.shape, adj_point) and adj_point not in visited and grid[adj_point] != 9:
                queue.append(adj_point)
                visited.append(adj_point)
    return size


def main():
    fname = "day9_input2.txt"
    grid = parse_input(fname)

    low_points = calculate_low_points(grid)

    risk_level = 0
    for low_point in low_points:
        risk_level += grid[low_point] + 1

    print(f"Risk level: {risk_level}")

    basin_sizes = []
    for low_point in low_points:
        basin_size = basin_size_bfs_search(grid, low_point)
        basin_sizes.append(basin_size)

    basin_sizes.sort()
    tmp = basin_sizes[-3:]
    basin_product = tmp[0] * tmp[1] * tmp[2]

    print(f"Basic product: {basin_product}")
    


if __name__ == "__main__":
    main()