def parse_num_array_from_file(fname):
    x = []
    with open(fname) as file:
        for line in file.readlines():
            x.append(int(line))
    return x
    
def find_increasing_depths(x_arr):
    count = 0
    for index in range(1, len(x_arr)):
        if x_arr[index] > x_arr[index-1]:
            count = count + 1
    
    return count

def calc_sliding_sum(x_arr, size):
    result = []
    running_sum = sum(x_arr[0:size])
    result.append(running_sum)

    for index in range(size, len(x_arr)):
        running_sum = running_sum - x_arr[index - size] + x_arr[index]
        result.append(running_sum)

    return result


def main():

    fname = "day1_input2.txt"

    x = parse_num_array_from_file(fname)
    x = calc_sliding_sum(x, 3)
    depth = find_increasing_depths(x)
    print(f"Calculated depth increases: {depth}")


if __name__ == "__main__":
    main()