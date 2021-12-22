
def parse_directions_from_file(fname):

    directions = []

    with open(fname) as file:
        for line in file.readlines():
            direction = line.strip().split()
            direction[1] = int(direction[1])
            directions.append(direction)

    return directions

def calculate_location_1(directions):
    depth = 0
    position = 0

    for direction in directions:
        if direction[0] == "forward":
            position = position + direction[1]
        elif direction[0] == "down":
            depth = depth + direction[1]
        elif direction[0] == "up":
            depth = depth - direction[1]

    return (depth, position)

def calculate_location_2(directions):
    depth = 0
    position = 0
    aim = 0

    for direction in directions:
        if direction[0] == "forward":
            position = position + direction[1]
            depth = depth + aim * direction[1]
        elif direction[0] == "down":
            aim = aim + direction[1]
        elif direction[0] == "up":
            aim = aim - direction[1]

    return (depth, position)


def main():

    fname = "day2_input2.txt"

    directions = parse_directions_from_file(fname)
    (depth, position) = calculate_location_2(directions)

    print(f"Depth is {depth}")
    print(f"Position is {position}")
    print(f"Product: {depth * position}")

if __name__ == "__main__":
    main()