
def parse_binary_input(fname):

    nums = []
    with open(fname) as file:
        for line in file.readlines():
            nums.append(line.strip())

    return nums

def get_most_common_digit(nums, pos):
    count_zero = 0
    count_one = 0
    for num in nums:
        if num[pos] == "0":
            count_zero = count_zero + 1
        elif num[pos] == "1":
            count_one = count_one + 1

    return 0 if count_zero > count_one else 1


def calculate_gamma_epsilon(nums):
    gamma = ""
    epsilon = ""

    num_digits = len(nums[0])

    for pos in range(num_digits):
        if get_most_common_digit(nums, pos) == 0:
            gamma = gamma + "0"
            epsilon = epsilon + "1"
        else:
            gamma = gamma + "1"
            epsilon = epsilon + "0"
    
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)

    return gamma, epsilon


def calculate_oxygen_generator_rating(nums):
    pos = 0
    while(len(nums) > 1):        

        mcd = get_most_common_digit(nums, pos)
        prune_nums = []
        for num in nums:
            if int(num[pos]) == mcd:
                prune_nums.append(num)

        nums = prune_nums
        pos = pos + 1
        
    return int(nums[0], 2)

def calculate_co2_scrubber_rating(nums):
    pos = 0
    while(len(nums) > 1):        

        lcd = 1 - get_most_common_digit(nums, pos)
        prune_nums = []
        for num in nums:
            if int(num[pos]) == lcd:
                prune_nums.append(num)

        nums = prune_nums
        pos = pos + 1
        
    return int(nums[0], 2)

def main():
    fname = "day3_input2.txt"
    nums = parse_binary_input(fname)

    gamma, epsilon = calculate_gamma_epsilon(nums)

    print(f"gamma = {gamma}, epsilon = {epsilon}")
    print(f"product = {gamma * epsilon}")

    oxygen_rating = calculate_oxygen_generator_rating(nums)
    co2_rating = calculate_co2_scrubber_rating(nums)
    print(f"oxygen generator rating = {oxygen_rating}")
    print(f"co2 scrubber rating = {co2_rating}")
    print(f"life support rating = {oxygen_rating * co2_rating}")


if __name__ == "__main__":
    main()