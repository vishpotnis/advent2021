
import sys

p_open = ['(', '[', '{', '<']

p_map = {'(' : ')',
         '[' : ']',
         '{' : '}',
         '<' : '>' 
        }

p_error_val = {')' : 3,
               ']' : 57,
               '}' : 1197,
               '>' : 25137 
              }

p_autocomplete_val = {')' : 1,
                      ']' : 2,
                      '}' : 3,
                      '>' : 4
                    }


def check_chunk(chunk):
    stk = []

    for c in chunk:
        if c in p_open:
            stk.append(c)
        else:
            top_p = stk.pop()
            if p_map[top_p] != c:
                return c, stk
    return "", stk


def find_closing_seq(stk):
    seq = []
    for c in stk:
        seq.append(p_map[c])
    seq.reverse()
    return seq


def calc_autocomplete_score(stk):
    seq = find_closing_seq(stk)
    score = 0
    for c in seq:
        score = score * 5 + p_autocomplete_val[c]
    return score


def main():
    fname = sys.argv[1]
        
    with open(fname) as file:
        chunks = [str.strip() for str in file.readlines()]
    
    syntax_error_score = 0
    autocomplete_scores = []
    for chunk in chunks:
        p, stk = check_chunk(chunk)    
        if len(p) == 1: 
            syntax_error_score += p_error_val[p]
        else:
            autocomplete_scores.append(calc_autocomplete_score(stk))

    autocomplete_scores.sort()
    middle_score = autocomplete_scores[int(len(autocomplete_scores)/2)]    

    print(f"Syntax error score: {syntax_error_score}")
    print(f"Middle score: {middle_score}")



if __name__ == "__main__":
    main()