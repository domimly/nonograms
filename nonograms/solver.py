from itertools import combinations_with_replacement


ROW_CLUES = [[1], [3], [1, 1], [3], [1]]
COL_CLUES = [(1), (3), (1), (3), (1)]

# ROW_CLUES = [[1], [3], [1, 2], [3], [1]]
# COL_CLUES = [(1), (3), (1), (3), (1), (1)]


class Nonogram:
    def __init__(self, row_clues, col_clues) -> None:
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.width = len(self.col_clues)
        self.height = len(self.row_clues)
        self.board = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]


class Solver:
    def __init__(self, board) -> None:
        self.board = board

    def row_permutations(self, row):
        # calculate number of movable (empty) white squares
        groups = self.board.row_clues[row]
        black_squares = sum(self.board.row_clues[row])
        white_squares = self.board.width - black_squares
        empty_squares = white_squares - (len(groups) - 1)

        # ensure that there is at least 1 white square
        # between each group of black squares
        row_contents = []
        for group in groups[:-1]:
            row_contents.append([1] * group + [0])
        row_contents.append([1] * groups[-1])

        # generate permutations of empty white squares
        positions = len(groups) + 1
        row_permutations = []
        for combo in combinations_with_replacement(
            range(positions), empty_squares
        ):
            white_count = [0] * positions
            for pos in combo:
                white_count[pos] += 1
            valid_row = []
            for i in range(positions):
                if i > 0:
                    valid_row += row_contents[i - 1]
                valid_row.extend([0] * white_count[i])
            row_permutations.append(valid_row)

        return row_permutations

    def solve(self):
        pass


nonogram = Nonogram(ROW_CLUES, COL_CLUES)
solver = Solver(nonogram)
perms = solver.row_permutations(2)
for perm in list(perms):
    print(perm)
