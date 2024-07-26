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
        self.rows_done = [0] * self.height
        self.cols_done = [0] * self.width
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

    def order_by_possibility(self):
        # get lists of rows_p and cols_p with number of options for each line
        rows_options_n = [len(options) for options in self.rows_possibilities]
        cols_options_n = [len(options) for options in self.cols_possibilities]
        # add info about line type and id, filter out done lines
        rows_options_info = [
            (True, i, n) for i, n in enumerate(rows_options_n) if (
                self.rows_done[i] == 0
            )
        ]
        cols_options_info = [
            (False, i, n) for i, n in enumerate(cols_options_n) if (
                self.cols_done[i] == 0
            )
        ]
        # order by number of options
        ordered_by_possibility = sorted(
            rows_options_info + cols_options_info,
            key=lambda info: info[1]
        )
        return ordered_by_possibility

    def place_squares(self, is_row, line_id):
        placed_squares = []
        if is_row:
            line_combinations = self.rows_possibilities[line_id]
            line_length = self.width
        else:
            line_combinations = self.cols_possibilities[line_id]
            line_length = self.height
        for index in range(line_length):
            if new_square := self.place_square(line_combinations, index):
                placed_squares.append((index, new_square))
        return placed_squares

    def place_square(self, line_combinations, index):
        first_value = line_combinations[0][index]
        for combo in line_combinations:
            if combo[index] != first_value:
                return None
        return first_value

    def remove_options(self, is_row, line_id, index, square_value):
        if is_row:
            for i, possibility in enumerate(self.cols_possibilities[index]):
                if possibility[line_id] != square_value:
                    self.cols_possibilities.pop(i)
        else:
            for i, possibility in enumerate(self.rows_possibilities[index]):
                if possibility[line_id] != square_value:
                    self.cols_possibilities.pop(i)

    def solve(self):
        self.rows_possibilities = self.possibilities(
            self.row_clues, self.width
        )
        self.cols_possibilities = self.possibilities(
            self.col_clues, self.height
        )
        while not self.solved:
            ordered_by_possibility = self.order_by_possibility()
            for is_row, line_id, _ in ordered_by_possibility:
                placed_squares = self.place_squares(is_row, line_id)
                if is_row:
                    for index, square_val in placed_squares:
                        self.board[line_id, index] = square_val
                        self.remove_options(is_row, index, square_val)

                else:
                    for index, square_val in placed_squares:
                        self.board[index, line_id] = square_val
                        self.remove_options(is_row, line_id, index, square_val)


nonogram = Nonogram(ROW_CLUES, COL_CLUES)
rows = nonogram.possibilities(nonogram.row_clues, nonogram.width)
for p in rows[2]:
    print(p)
