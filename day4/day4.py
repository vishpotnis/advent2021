
class BingoBoard:    

    def __init__(self):
        self.rowTracker = [0] * 5
        self.colTracker = [0] * 5
        self.board = []
        self.numMap = {}
        self.marked = []
        self.totalSum = 0
        self.done = False

    def isComplete(self):
        for x in self.rowTracker:
            if x == 5: 
                self.done = True
                return True
        for x in self.colTracker:
            if x == 5:
                self.done = True
                return True
        return False

    def isDone(self):
        return self.done

    def markNumber(self, num):
        pos = self.numMap.get(num)
        if pos is not None:
            rowIdx, colIdx = pos
            self.rowTracker[rowIdx] += 1
            self.colTracker[colIdx] += 1
            self.marked.append(num)
            return True
        return False

    def parse_board(self, file):        
        for i in range(5):
            line = [int(x) for x in file.readline().strip().split()]
            self.board.append(line)

        self._create_hashmap()

    def _create_hashmap(self):
        for rowIdx, row in enumerate(self.board):
            for colIdx, num in enumerate(row):
                self.numMap[num] = (rowIdx, colIdx)
                self.totalSum += num 

    def get_unmarked_sum(self):
        return self.totalSum - sum(self.marked)

    def __str__(self) -> str:
        return str(self.board)

                    
        
def parse_board_input(fname):
    boards = []

    with open(fname) as file:
        bingo_order = [int(x) for x in file.readline().strip().split(',')]

        line = file.readline()
        while line:
            board = BingoBoard()
            board.parse_board(file)
            boards.append(board)

            line = file.readline()
    return boards, bingo_order

def play_bingo(boards, bingo_order):

    for round, num in enumerate(bingo_order):
        print(f"Round {round}: {num}")
        for boardIdx, board in enumerate(boards):
            if not board.isDone() and board.markNumber(num):
                print(f"\tBoard {boardIdx} marked {num}")
            if not board.isDOne() and board.isComplete():
                unmarked_sum = board.get_unmarked_sum()
                print(f"\tBoard {boardIdx} BINGO!")
                print(f"\t\tSum of unmarked numbers: {unmarked_sum}")
                print(f"\t\tFinal score: {unmarked_sum} * {num} = {unmarked_sum * num}")
                return

def play_bingo_last(boards, bingo_order):

    for round, num in enumerate(bingo_order):
        print(f"Round {round}: {num}")
        for boardIdx, board in enumerate(boards):
            if not board.isDone() and board.markNumber(num):
                print(f"\tBoard {boardIdx} marked {num}")
            if not board.isDone() and board.isComplete():
                unmarked_sum = board.get_unmarked_sum()
                print(f"\tBoard {boardIdx} BINGO!")
                print(f"\t\tSum of unmarked numbers: {unmarked_sum}")
                print(f"\t\tFinal score: {unmarked_sum} * {num} = {unmarked_sum * num}")

def main():
    fname = "day4_input2.txt"

    boards, bingo_order = parse_board_input(fname)
    play_bingo_last(boards, bingo_order)


if __name__ == "__main__":
    main()