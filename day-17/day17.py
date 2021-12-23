import sys

def parse_input(fname):
    with open(fname) as file:
        text = file.readline()
        tmp = text.split(':')[1].split(',')

        x_loc = [int(x) for x in tmp[0].strip().split('=')[1].split('..')]
        y_loc = [int(y) for y in tmp[1].strip().split('=')[1].split('..')]
    return x_loc, y_loc


def simulate(velocity, x_tar, y_tar):

    x_pos = 0
    y_pos = 0
    y_max = 0
    debug = False

    if debug:
        print(f"Target ({x_tar},{y_tar})\tvelocity ({velocity[0]},{velocity[1]})")
    step = 0
    done = False
    while True:
        step += 1
        x_pos, y_pos, velocity = simulate_step(x_pos, y_pos, velocity)
        done = is_in_target(x_pos, y_pos, x_tar, y_tar)
        y_max = max(y_max, y_pos)
        if debug:
            print(f"After step {step}: position ({x_pos},{y_pos}) velocity ({velocity[0]},{velocity[1]}) target hit {done}")

        if x_pos > x_tar[1] or y_pos < y_tar[0]:
            if debug:
                print(f"Target missed")
            break

        if done:
            if debug:
                print(f"Hit target after {step} steps. Max height {y_max}")
            break
    return y_max, done


def simulate_step(x_pos, y_pos, velocity):
    x_pos += velocity[0]
    y_pos += velocity[1]
    new_velocity = (max(0, velocity[0] - 1), velocity[1] - 1)
    return x_pos, y_pos, new_velocity

def is_in_target(x_pos, y_pos, x_tar, y_tar):
    if x_pos >= x_tar[0] and x_pos <= x_tar[1] and y_pos >= y_tar[0] and y_pos <= y_tar[1]:
        return True
    return False


def main():
    fname = sys.argv[1]
    x_tar, y_tar = parse_input(fname)

    print(f"Target ({x_tar},{y_tar})")
    y_max_all = 0
    valid_velocities = []
    for x_velocity in range(x_tar[1] + 1):
        for y_velocity in range(-500, 500):
            velocity = (x_velocity, y_velocity)

            y_max, done = simulate(velocity, x_tar, y_tar)            
            if done:
                y_max_all = max(y_max_all, y_max)
                valid_velocities.append(velocity)
                print(f"velocity {velocity}: Target hit, y_max: {y_max}")                
            else:
                print(f"velocity {velocity}: Target missed")
    print(f"Highest y position: {y_max_all}")
    print(f"Num valid velocities: {len(valid_velocities)}")
    print(valid_velocities)
    

if __name__ == "__main__":
    main()