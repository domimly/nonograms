from itertools import combinations

ROW_CLUES = [[1], [3], [1, 1], [3], [1]]
COL_CLUES = [[1], [3], [1], [3], [1]]

# ROW_CLUES = [[1], [3], [1, 2], [3], [1]]
# COL_CLUES = [[1], [3], [1], [3], [1]]


class Nonogram:
    def __init__(self, row_clues, col_clues) -> None:
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.width = len(self.col_clues)
        self.height = len(self.row_clues)
        self.rows_possibilities = None
        self.cols_possibilities = None
        self.board = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]
        self.solved = False

    def possibilities(self, clues, line_length):
        possibiliies = []
        for line_clues in clues:
            line_possibilities = (
                self.line_possibilities(line_clues, line_length)
            )
            possibiliies.append(line_possibilities)
        return possibiliies

    def line_possibilities(self, line_clues, line_length):
        line_possibilities = []
        groups_n = len(line_clues)
        empty_squares = line_length - sum(line_clues) - (groups_n - 1)

        groups_placement_possibilities = (
            combinations(range(groups_n + empty_squares), groups_n)
        )

        for possibility in groups_placement_possibilities:
            line = [0] * line_length
            groups_separator_counter = 0
            for index, group_length in zip(possibility, line_clues):
                group_pos = index + groups_separator_counter
                for i in range(group_length):
                    line[group_pos + i] = 1
                    groups_separator_counter += 1

            line_possibilities.append(line)
        return line_possibilities

    def place_square(self, line_combinations, index):
        first_value = line_combinations[0][index]
        for combo in line_combinations:
            if combo[index] != first_value:
                return None
        return first_value

    def solve(self):
        self.rows_possibilities = self.possibilities(
            self.row_clues, self.width
        )
        self.cols_possibilities = self.possibilities(
            self.col_clues, self.height
        )


nonogram = Nonogram(ROW_CLUES, COL_CLUES)
rows = nonogram.possibilities(nonogram.row_clues, nonogram.width)
for p in rows[2]:
    print(p)
