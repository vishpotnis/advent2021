import numpy as np

def simulate(fish, days: int):
    
    print(f"Initial state: {fish}")
    current_day = 0
    while current_day < days:
        repro_fish = np.where(fish == 0)
        num_repro_fish = repro_fish[0].size

        new_fish = np.ones(num_repro_fish, dtype=np.int32) * 8

        change_vec = np.ones(len(fish), dtype=np.int32)
        fish -= change_vec
        fish[repro_fish] = 6
        fish = np.append(fish, new_fish)

        current_day += 1
        print(f"After {current_day:2} days: {fish}")
    
    return len(fish)

def simulate_fast(fish, days: int):

    fish_state = [0] * 9
    for f in fish:
        fish_state[f] += 1
    
    print(f"Initial state: {fish_state}")
    current_day = 0
    while current_day < days:
        num_repro_fish = fish_state.pop(0)

        fish_state.append(num_repro_fish)
        fish_state[6] += num_repro_fish

        current_day += 1        
        print(f"After {current_day:2} days: {fish_state}")

    return sum(fish_state)


def main():
    fname = "day6_input2.txt"
    days = 256
    with open(fname) as file:
        fish = np.array([int(x) for x in file.readline().strip().split(',')])
    
    num_fish = simulate_fast(fish, days)

    print(f"{num_fish} fish after {days} days")

    
if __name__ == "__main__":
    main()
