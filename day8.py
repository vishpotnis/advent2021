

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

def calc_sum_of_mapped_outpues(data):
    sum = 0
    for datum in data:
        sum += calculate_output(datum[0], datum[1])
    print(f"Sum of output values: {sum}")

def calculate_output(data, output):
    pattern_map = find_mapping(data)
    val = 0
    for out_str in output:
        val = val * 10 + pattern_map["".join(sorted(out_str))]
    
    return val

def find_mapping(pattern):
    pattern_len = {}
    segment_map = {}

    # create dictionary that maps length to pattern
    for s in pattern:
        num_seg = len(s)
        tmp = pattern_len.get(num_seg, [])
        tmp.append(s)
        pattern_len[num_seg] = tmp
    
    # map digits that have unique length (should only be 1 item in the list)
    segment_map[1] = pattern_len[2][0]
    segment_map[4] = pattern_len[4][0]
    segment_map[7] = pattern_len[3][0]
    segment_map[8] = pattern_len[7][0]

    top_seg = set(segment_map[7]).difference(segment_map[1])

    # narrow pattern list for 2, 5, 6 since they dont have both the right segments
    # that the digit 1 has
    pattern_256 = [s for s in pattern if not set(s).issuperset(segment_map[1])]

    # determine 2 vs 5/6. 2 contains top right segment, 5/6 contain bottom right
    # partition the 3 patterns in pattern_256 based on the segments from digit 1

    # first determine the top right segment
    count = [0, 0]
    for s in pattern_256:
        for i, c in enumerate(segment_map[1]):
            if c in s:
                count[i] += 1    
    idx2 = count.index(1)
    top_right_seg = segment_map[1][idx2]

    # identify 2 based on top right segment
    for s in pattern_256:
        if set(s).issuperset(top_right_seg):
            segment_map[2] = s

    # remaining patterns are for 5 and 6. 5 has len 5, 6 has len 6
    pattern_256.remove(segment_map[2])
    for s in pattern_256:
        segment_map[len(s)] = s   

    # remaining len 5 pattern is for 3
    pattern_235 = pattern_len[5] 
    pattern_235.remove(segment_map[2])
    pattern_235.remove(segment_map[5])
    segment_map[3] = pattern_235[0]

    # determine 0 vs 9. 9 doesn't have bottom left segment. diff between 5 and 6 is bottom left segment
    bottom_left_seg = set(segment_map[6]).difference(segment_map[5])

    pattern_069 = pattern_len[6]
    pattern_069.remove(segment_map[6])
    for s in pattern_069:
        if set(s).issuperset(bottom_left_seg):
            segment_map[0] = s
        else:
            segment_map[9] = s    

    pattern_map = {}
    for digit, pattern in segment_map.items():
        pattern_map["".join(sorted(pattern))] = digit

    return pattern_map


def main():
    fname = "day8_input2.txt"
    data = parse_input(fname)

    calc_unique_segments_in_output(data)
    calc_sum_of_mapped_outpues(data)
    

if __name__ == "__main__":
    main()