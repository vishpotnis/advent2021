import sys
import numpy as np

def parse_input(fname):
    dots = []
    instructions = []
    with open(fname) as file:
        file.readline
        lines = file.readlines()
        for line in lines:
            if line == '\n':
                continue
            if line[0] != 'f':
                tmp = [int(x) for x in line.strip().split(',')]
                dots.append(tmp)
            else:
                tmp = line.strip().split('=')                
                tmp = [tmp[0][-1], int(tmp[1])]
                instructions.append(tmp)
    return np.array(dots), instructions

def get_paper_dim(dots):
    maxx = 0
    maxy = 0
    for dot in dots:
        maxx = max(maxx, dot[0])
        maxy = max(maxy, dot[1])
    
    return maxx, maxy
        
def fold_along_y(dots, y):
    for dot in dots:
        if dot[1] > y:
            dot[1] = y - (dot[1] - y)    
    return np.unique(dots, axis=0)

def fold_along_x(dots, x):
    for dot in dots:
        if dot[0] > x:
            dot[0] = x - (dot[0] - x)
    return np.unique(dots, axis=0)

def draw_image(dots):
    maxx, maxy = get_paper_dim(dots)
    
    grid = []
    for y in range(maxy + 1):
        grid.append([' '] * (maxx + 1))
    for dot in dots:
        grid[dot[1]][dot[0]] = '#'
    
    for g in grid:
        print(''.join(g))


def main():
    fname = sys.argv[1]
    dots, instructions = parse_input(fname)

    for count, instruction in enumerate(instructions):
        if instruction[0] == 'y':
            dots = fold_along_y(dots, instruction[1])
        elif instruction[0] == 'x':
            dots = fold_along_x(dots, instruction[1])
        print(f"{count + 1} fold: {len(dots)} dots after {instruction[0]} = {instruction[1]}")
    
    draw_image(dots)

        


if __name__ == "__main__":
    main()