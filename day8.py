

def parse_input(fname):
    data = []

    with open(fname) as file:
        for line in file.readlines():
            tmp = line.strip().split('|')
            data.append([tmp[0].strip().split(), tmp[1].strip().split()])
    
    return data

def calc_unique_segments_in_output(data):
    num = 0
    unique_segments = [2, 4, 3, 7]

    for item in data:
        lens_exist = [len(x) in unique_segments for x in item[1]]        
        num += sum(lens_exist)

    print(f"1, 4, 7, 8 appear {num} times")

def calculate_output(data):
    find_mapping(data[0][0], data[0][1])

def find_mapping(pattern, output):
    print(pattern, output)

def main():
    fname = "day8_input3.txt"
    data = parse_input(fname)

    calc_unique_segments_in_output(data)
    calculate_output(data)
    

if __name__ == "__main__":
    main()