import matplotlib.pyplot as plt

def calc_cost(nums, val, type):
    sum = 0
    for x in nums:
        step = abs(x - val)
        if type == 1:
            cost = step
        elif type == 2:
            cost = (step * (step + 1))/2
            
        sum += cost
    return sum

def main():
    fname = "day7_input2.txt"

    with open(fname) as file:
        nums = [int(x) for x in file.readline().split(',')]
    
    minVal = 0
    maxVal = max(nums)

    costVec = []
    for val in range(minVal, maxVal + 1):
        costVec.append(calc_cost(nums, val, 2))
    
    minFuel = min(costVec)
    minFuelIdx = costVec.index(minFuel)

    print(f"Position {minFuelIdx} has fuel of {minFuel}")

    plt.plot(costVec)
    plt.grid()
    plt.ylabel("Fuel cost")
    plt.show()


if __name__ == "__main__":
    main()