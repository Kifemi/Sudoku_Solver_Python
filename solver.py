import copy


def solve(puzzle):
    temp_puzzle = copy.deepcopy(puzzle)

    run = True

    while run:
        possible_values = [[get_possible_values(temp_puzzle, i, j) for j in range(9)] for i in range(9)]

        # Fill unique values
        if fill_unique(possible_values, temp_puzzle):
            continue

        # Check if possible value appears once in a 3x3 square
        if fill_square(possible_values, temp_puzzle):
            continue

        # Check if possible value appears once in a row
        if fill_row(possible_values, temp_puzzle):
            continue

        # Check if possible value appears once in a column
        if fill_col(possible_values, temp_puzzle):
            continue

        run = False

    backtracking(temp_puzzle)
    # print(temp_puzzle)
    if check_solution(temp_puzzle):
        return temp_puzzle
    else:
        return None


def fill_unique(possible_values, temp_puzzle) -> bool:
    for i in range(9):
        for j in range(9):
            if possible_values[i][j] is not None:
                value_set = possible_values[i][j]
                # If only one possible value in cell, fill it
                if len(value_set) == 1:
                    temp_puzzle[i][j] = next(iter(value_set))
                    # print(f"first loop: {i}, {j}, {temp_puzzle[i][j]}")
                    return True
    return False


def fill_row(possible_values, temp_puzzle) -> bool:
    for i in range(9):
        for j in range(9):
            if possible_values[i][j] is not None:
                value_set = possible_values[i][j]
                for index, row_set in enumerate(possible_values[i]):
                    if row_set is not None and index != j:
                        value_set = value_set.difference(row_set)
                if len(value_set) == 1:
                    temp_puzzle[i][j] = next(iter(value_set))
                    # print(f"row loop: {i}, {j}, {temp_puzzle[i][j]}")
                    return True
    return False


def fill_col(possible_values, temp_puzzle) -> bool:
    for i in range(9):
        for j in range(9):
            value_set = [possible_values[j][i] for j in range(9)]
            if value_set[j] is not None:
                for index, col_set in enumerate(value_set):
                    if col_set is not None and value_set[j] is not None and index != j:
                        value_set[j] = value_set[j].difference(col_set)
                if len(value_set[j]) == 1:
                    temp_puzzle[j][i] = next(iter(value_set[j]))
                    # print(f"col loop: {j}, {i}, {temp_puzzle[j][i]}")
                    return True
    return False


def fill_square(possible_values, temp_puzzle) -> bool:
    for n in range(3):
        for m in range(3):
            value_set = []
            for i in range(3*n, 3*n + 3):
                for j in range(3*m, 3*m + 3):
                    if possible_values[i][j] is not None:
                        value_set.append(possible_values[i][j])
                    else:
                        value_set.append(None)
            for k in range(9):
                value_set_temp = value_set.copy()
                for index, square_set in enumerate(value_set_temp):
                    if square_set is not None and value_set_temp[k] is not None and index != k:
                        value_set_temp[k] = value_set_temp[k].difference(square_set)
                if value_set_temp[k] is not None and len(value_set_temp[k]) == 1:
                    temp_puzzle[n*3 + k // 3][m*3 + k % 3] = next(iter(value_set_temp[k]))
                    # print(f"square loop: {n*3 + k // 3}, {m*3 + k % 3}, {temp_puzzle[n*3 + k // 3][m*3 + k % 3]}")
                    return True
    return False


def backtracking(puzzle) -> bool:
    empty_cell = check_if_empty(puzzle)
    if empty_cell:
        row, col = empty_cell
        # print(f"row: {row}, col: {col}")
    else:
        return True
    for k in range(1, 10):
        if is_possible(puzzle, k, row, col)[0]:
            puzzle[row][col] = k
            # for row_temp in puzzle:
            #     print(row_temp)
            # print()
            if backtracking(puzzle):
                return True
            # print(f"row2: {row}, col2: {col}")
            puzzle[row][col] = 0

    return False


def is_possible(puzzle, value, row, col) -> (bool, list):
    """
    Check if the given `value` is viable to be put into the cell located to `row` and `col`
    :param puzzle: Current state of the sudoku excluding the value which is being checked.
    :param value: Value which is
    :param row: The row where the `value` is put
    :param col: The column where the `value` is put
    :return: Return a tuple of length 2 of the form (bool, list). Bool is False if the `value`
        is already found in the `row`, `col` or 3x3 square where the value would be placed.
        In this case the list contains every location where duplicate was found.
        Otherwise it is possible to place the value into the cell.
        In this case return True with empty list.
    """
    # possible = True
    errors = []
    # If there is an another number in the cell where the value is tried to be put, then
    # if the number is different than the value, the function returns True, and
    # if the number is same than the value, the function returns False (in this case there
    # is no need for change).
    # The empty cell corresponds to value 0 or None, so the function returns True for
    # numbers 1-9
    for i in range(9):
        if puzzle[row][i] == value:
            errors.append((row, i))
            # return False
        if puzzle[i][col] == value:
            errors.append((i, col))
            # return False
    x = row // 3
    y = col // 3
    for i in range(3 * x, 3 * x + 3):
        for j in range(3 * y, 3 * y + 3):
            if puzzle[i][j] == value:
                errors.append((i, j))
                # return False
    return (True, errors) if len(errors) == 0 else (False, errors)


def check_if_empty(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return i, j


def get_possible_values(puzzle, row, col):
    if not puzzle[row][col]:
        number_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        # Check rows
        for j in range(9):
            number_set.discard(puzzle[row][j])
        # Check columns
        for i in range(9):
            number_set.discard(puzzle[i][col])
        # Check 3x3 square
        x = row // 3
        y = col // 3
        for i in range(3*x, 3*x + 3):
            for j in range(3*y, 3*y + 3):
                number_set.discard(puzzle[i][j])
        # if not number_set:
        #     print("Impossible puzzle")
        return number_set
    return None


def check_solution(puzzle) -> bool:
    """
    Check that each row, column and 3x3 square of the sudoku puzzle has every number
    between 1-9 once.
    :param puzzle: List containing the lists of values of the each row.
    :return: Return True if each row, column and 3x3 square contain each of the numbers
    between 1-9 once. Return False otherwise
    """
    numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    is_correct = True
    for i in range(9):
        # collect set of all values from the i:th row of the puzzle
        row = set(puzzle[i])
        # check if the row contains every number once
        if row != numbers:
            is_correct = False
            break

        # collect set of all values from the i:th column of the puzzle
        col = set()
        for j in range(9):
            col.add(puzzle[j][i])
        # check if the column contains every number once
        if col != numbers:
            is_correct = False
            break

        # collect set of all values from the 3x3 square
        square = set()
        for j in range(9):
            x = i // 3
            y = j // 3
            for i2 in range(3 * x, 3 * x + 3):
                for j2 in range(3 * y, 3 * y + 3):
                    square.add(puzzle[i2][j2])
        # check if the square contains every number once
        if square != numbers:
            is_correct = False
            break
    return is_correct
