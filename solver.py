import settings


def solve(puzzle):
    possible_values = [[get_possible_values(puzzle, i, j) for j in range(9)] for i in range(9)]
    return possible_values


def get_possible_values(puzzle, row, col):
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
    return list(number_set)


print(solve(settings.puzzle))
