import sys
from collections import defaultdict

def parse_input(fname):
    with open(fname) as file:
        template = file.readline().strip()
        pairs = {}
        file.readline()
        for line in file.readlines():
            tmp = line.strip().split('->')            
            pairs[tmp[0].strip()] = tmp[1].strip()

    return template, pairs

########## slow solution  ###########

def perform_step_slow(template, pairs):
    result = template[0]
    for i in range(1, len(template)):
        curr_pair = template[i-1:i+1]
        result = result + pairs.get(curr_pair, "") + template[i]
    return result

def get_letter_counts(text):
    chars = defaultdict(int)
    for char in text:
        chars[char] += 1
    return chars

def solution_slow(template, pairs, steps):
    print(f"Template:     {template}")
    text = template
    for step in range(steps):
        print(f"Processing step {step+1}...")
        text = perform_step_slow(text, pairs)
        

    chars = get_letter_counts(text)
    print(f"Answer: {max(chars.values()) - min(chars.values())}")

########### fast solution ############

def convert_input_to_dict(template):
    d = defaultdict(int)
    chars = defaultdict(int)
    for i in range(1, len(template)):
        curr_pair = template[i-1:i+1]
        d[curr_pair] += 1
    for char in template:
        chars[char] += 1
    return d, chars

def perform_step_fast(d, chars, pairs):
    d_new = defaultdict(int)
    for key, value in d.items():
        ins_char = pairs[key]
        new_key1 = key[0] + ins_char
        new_key2 = ins_char + key[1]

        d_new[new_key1] += value
        d_new[new_key2] += value
        chars[ins_char] += value
    return d_new, chars

def solution_fast(template, pairs, steps):    
    print(f"Template:     {template}")
    d, chars = convert_input_to_dict(template)
    
    for step in range(steps):
        print(f"Processing step {step+1}...")
        d, chars = perform_step_fast(d, chars, pairs)        
    print(f"Answer: {max(chars.values()) - min(chars.values())}")
    

def main():
    fname = sys.argv[1]
    template, pairs = parse_input(fname)
    steps = 40
    
    solution_fast(template, pairs, steps)

if __name__ == "__main__":
    main()