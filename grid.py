import copy


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.all_squares = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

        self.solve()


    def solve(self):
        prev_iteration = None
        iteration = self.grid

        while iteration != prev_iteration:
            prev_iteration = copy.deepcopy(iteration)
            for value in range(1, 10):
                prev_laser_iteration = None
                laser_iteration = self.grid
                while laser_iteration != prev_laser_iteration:
                    self._laser_check_number(value)
                    prev_laser_iteration = laser_iteration
                    laser_iteration = self.grid

                prev_row_iteration = None
                row_iteration = self.grid
                while row_iteration != prev_row_iteration:
                    self._row_check_number(value)
                    prev_row_iteration = row_iteration
                    row_iteration = self.grid

                prev_column_iteration = None
                column_iteration = self.grid
                while column_iteration != prev_column_iteration:
                    self._column_check_number(value)
                    prev_column_iteration = column_iteration
                    column_iteration = self.grid

                prev_square_iteration = None
                square_iteration = self.grid
                while square_iteration != prev_square_iteration:
                    self._square_check_number(value)
                    prev_square_iteration = square_iteration
                    square_iteration = self.grid

            iteration = self.grid

    def __str__(self):
        string = ''
        for j, row in enumerate(self.grid):
            for i, value in enumerate(row):
                if isinstance(value, int):
                    string += str(value)
                else:
                    string += ' '

                if (i + 1) % 3 == 0 and not i == 8:
                    string += '|'

            string += '\n'
            if (j + 1) % 3 == 0 and not j == 8:
                string += '-' * 11
                string += '\n'

        return string

    @staticmethod
    def _squares(coordinate):
        i, j = coordinate
        i_temp = i - i % 3
        j_temp = j - j % 3

        i_all = [i_temp, i_temp + 1, i_temp + 2]
        j_all = [j_temp, j_temp + 1, j_temp + 2]

        square_coordinates = []
        for i_coordinate in i_all:
            for j_coordinate in j_all:
                square_coordinates.append((i_coordinate, j_coordinate))
        return square_coordinates

    def _laser_check_number(self, number):
        mask = [[True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True, True]]

        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):

                if self.grid[i][j]:
                    mask[i][j] = False

                if value == number:
                    for k in range(9):
                        mask[k][j] = False
                        mask[i][k] = False

                    squares = self._squares((i, j))

                    for a, b in squares:
                        mask[a][b] = False

        for square in self.all_squares:
            square_coordinates = self._squares(square)

            mask_entries = []
            for i, j in square_coordinates:
                if mask[i][j]:
                    mask_entries.append((i, j))

            if len(mask_entries) == 1:
                i, j = mask_entries[0]
                self.grid[i][j] = number

    def _row_check_number(self, number):
        for j, row in enumerate(self.grid):
            if row.count(None) == 1 and number not in row:
                row = [number if not value else value for value in row]

            self.grid[j] = row

    def _column_check_number(self, number):
        for j in range(len(self.grid)):
            column = []
            for i in range(len(self.grid)):
                column.append(self.grid[i][j])

            if column.count(None) == 1 and number not in column:
                column = [number if not value else value for value in column]

            for i, value in enumerate(column):
                self.grid[i][j] = value

    def _square_check_number(self, number):
        for square_number in self.all_squares:
            square_coordinates = self._squares(square_number)
            square = []
            for coordinate in square_coordinates:
                i, j = coordinate
                square.append(self.grid[i][j])

            if square.count(None) == 1 and number not in square:
                for coordinate in square_coordinates:
                    i, j = coordinate
                    self.grid[i][j] = number if self.grid[i][j] is None else self.grid[i][j]
