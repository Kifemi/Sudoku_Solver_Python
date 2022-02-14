import copy
import pygame


def fill_unique(possible_values, temp_puzzle) -> (bool, (int, int)):
    for i in range(9):
        for j in range(9):
            if possible_values[i][j] is not None:
                value_set = possible_values[i][j]
                # If only one possible value in cell, fill it
                if len(value_set) == 1:
                    temp_puzzle[i][j] = next(iter(value_set))
                    # print(f"first loop: {i}, {j}, {temp_puzzle[i][j]}")
                    return True, (i, j)
    return False, (None, None)


def fill_row(possible_values, temp_puzzle) -> (bool, (int, int)):
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
                    return True, (i, j)
    return False, (None, None)


def fill_col(possible_values, temp_puzzle) -> (bool, (int, int)):
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
                    return True, (j, i)
    return False, (None, None)


def fill_square(possible_values, temp_puzzle) -> (bool, (int, int)):
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
                    return True, (n*3 + k // 3, m*3 + k % 3)
    return False, (None, None)


def backtracking(board, screen) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()

    empty_cell = check_if_empty(board.current_puzzle)
    if empty_cell:
        row, col = empty_cell
        # print(f"row: {row}, col: {col}")
    else:
        return True
    for k in range(1, 10):
        if is_possible(board.current_puzzle, k, row, col)[0]:
            board.current_puzzle[row][col] = k
            board.cells[row][col].backtracking_correct = True
            board.cells[row][col].value = k
            board.update_board(screen)
            pygame.time.delay(50)
            if backtracking(board, screen):
                return True
            # print(f"row2: {row}, col2: {col}")
            board.current_puzzle[row][col] = 0
            board.cells[row][col].backtracking_incorrect = True
            board.cells[row][col].backtracking_correct = False
            board.cells[row][col].value = 0
            pygame.time.delay(50)

            board.update_board(screen)

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
