import pygame
import settings
import copy

from solver import solve, is_possible, check_solution
import solver_test

pygame.font.init()


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.width = settings.width
        self.height = settings.height
        self.puzzle = settings.puzzle_hard
        self._current_puzzle = None
        self.cells = [[Cell(self.puzzle[i][j], i, j, self.width, self.height, self.screen) for j in range(9)] for i in range(9)]
        self.selected_cell = (0, 0)
        self.solution = None

        # Initializing values
        self.cells[0][0].is_selected = True
        # Creating a deepcopy of self.puzzle by using current_puzzle setter property
        self.current_puzzle = self.puzzle

    @property
    def current_puzzle(self):
        return self._current_puzzle

    @current_puzzle.setter
    def current_puzzle(self, puzzle):
        self._current_puzzle = copy.deepcopy(puzzle)

    def draw_lines(self, screen) -> None:
        """
        Draw 10 horizontal and 10 vertical lines on the pygame `screen`.
        Every third line is wider.
        :param screen: Pygame display window
        :return: None
        """
        # Draw horizontal and vertical lines
        cell_size = self.width // 9
        for i in range(10):
            width = 1
            # Every third line is wider
            if i % 3 == 0:
                width = 5
            # Calculate start and end positions for the line
            start_pos_horizontal = (0, i * cell_size)
            end_pos_horizontal = (self.width, i * cell_size)
            start_pos_vertical = (i * cell_size, 0)
            end_pos_vertical = (i * cell_size, self.height)
            # Draw the i:th horizontal and vertical line
            pygame.draw.line(screen, settings.BLACK, start_pos_horizontal, end_pos_horizontal, width)
            pygame.draw.line(screen, settings.BLACK, start_pos_vertical, end_pos_vertical, width)

    def draw_cells(self, screen) -> None:
        """
        Draw each of the cells
        :param screen: Pygame display window
        :return: None
        """
        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw_cell(screen)

    def select_cell(self, row: int, col: int, screen) -> None:
        """
        Change the selected cell while resetting the previous values. Cells
        in the top row move to the bottom row in the case of upward movement and
        cells in the bottom row move to top row in the case of downward movement.
        Works similarly for the horizontal movement.
        :param row: Selected cell's row
        :param col: Selected cell's column
        :param screen: Pygame display window
        :return: None
        """
        # Reset every cell
        for i in range(9):
            for j in range(9):
                self.cells[i][j].is_selected = False

        # Row and column numbers are between 0 and 8. If the number is bigger
        # reduce it back to the range by taking modulo 9.
        row %= 9
        col %= 9
        # Select new cell
        self.cells[row][col].is_selected = True
        self.selected_cell = (row, col)

        # Draw the cells to update the screen.
        self.draw_cells(screen)

    def change_value(self, value: int) -> None:
        row = self.selected_cell[0]
        col = self.selected_cell[1]
        if not self.cells[row][col].has_initial_value:
            possible = True
            errors = []
            if value != 10:
                possible, errors = is_possible(self.current_puzzle, value, row, col)
            if possible:
                # If value 10 is provided, use the cell's value property to change
                # the value to zero (clear the cell).
                self.cells[row][col].value = value
                self.update_value(value, row, col)
                # self.cells[row][col].draw_cell(self.screen)
            else:
                for row, col in errors:
                    self.cells[row][col].show_error = True
                    self.cells[row][col].draw_cell(self.screen)

    def clear_cells(self) -> None:
        """
        Clear every cell except the ones with initial values.
        :return: None
        """
        self.current_puzzle = self.puzzle
        for i in range(9):
            for j in range(9):
                if not self.cells[i][j].has_initial_value:
                    self.cells[i][j].value = 0
                    # self.cells[i][j].draw_cell(self.screen)

    def clear_bg_colors(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].show_error = False
                self.cells[i][j].unique_value = None
                self.cells[i][j].backtracking_correct = False
                self.cells[i][j].backtracking_incorrect = False

    def update_value(self, value, row, col) -> None:
        if 0 < value < 10:
            self.current_puzzle[row][col] = value
            if check_solution(self.current_puzzle):
                print("Congratulations you solved the puzzle!")
        elif value == 10:
            self.current_puzzle[row][col] = 0

    def show_solution(self, solution):
        if solution is not None:
            self.solution = solution
            self.current_puzzle = self.solution
            print("Puzzle solved by non-visual backtracking")
        else:
            print("Puzzle is impossible to solve")
            return
        for i in range(9):
            for j in range(9):
                if not self.cells[i][j].has_initial_value:
                    self.cells[i][j].value = self.solution[i][j]
        self.draw_cells(self.screen)

    def update_board(self, screen):
        # self.draw_cells(screen)
        self.draw_lines(screen)
        # draw_game_info(screen)
        pygame.display.update()

    def solve_unique_values(self, func, possible_values, color):
        value_found = True
        continue_loop, cell = func(possible_values, self.current_puzzle)
        if continue_loop:
            self.cells[cell[0]][cell[1]].unique_value = color.copy()
            self.cells[cell[0]][cell[1]].value = self.current_puzzle[cell[0]][cell[1]]
            color[2] -= 3
            color[0] += 2
            # self.cells[cell[0]][cell[1]].draw_cell(self.screen)
        else:
            value_found = False
        self.update_board(self.screen)
        return value_found

    def solve_visually(self):
        run = True
        color = list(settings.DARK_BLUE)

        while run:
            possible_values = [[solver_test.get_possible_values(self.current_puzzle, i, j) for j in range(9)] for i in range(9)]

            if self.solve_unique_values(solver_test.fill_unique, possible_values, color):
                continue
            if self.solve_unique_values(solver_test.fill_square, possible_values, color):
                continue
            if self.solve_unique_values(solver_test.fill_row, possible_values, color):
                continue
            if self.solve_unique_values(solver_test.fill_col, possible_values, color):
                continue

            if not check_solution(self.current_puzzle):
                print("Backtracking visually....")
                solver_test.backtracking(self, self.screen)
                self.clear_bg_colors()
                self.draw_cells(self.screen)
                self.update_board(self.screen)

            run = False

        print("Closing solver")

        if check_solution(self.current_puzzle):
            print("Board solved by visual backtracking")
        else:
            print("Impossible puzzle (Visual backtracking)")


class Cell:
    def __init__(self, value, row, col, width, height, screen):
        self.screen = screen
        self._value = value
        self.row = row
        self.col = col
        self.cell_width = width // 9
        self.cell_height = height // 9
        self.has_initial_value = True if self.value else False
        # Attributes affecting to background color
        self.is_selected = False
        self.show_error = False
        self.unique_value = None
        self.backtracking_correct = False
        self.backtracking_incorrect = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        if 0 < x < 10:
            self._value = x
        else:
            self._value = 0
        self.draw_cell(self.screen)
        pygame.display.update()

    def draw_cell(self, screen) -> None:
        """
        Draw a new value in the cell in question
        :param screen: Pygame display screen
        :return: None
        """

        # Check if the cell is selected and choose corresponding color
        if self.is_selected or self.backtracking_correct:
            color = settings.SELECTED_COLOR
        elif self.show_error or self.backtracking_incorrect:
            color = settings.RED
        elif self.unique_value is not None:
            color = self.unique_value
        else:
            color = settings.WHITE
        # Create solid coloured Pygame Rect object and draw it into correct position
        cell = pygame.Rect(self.col * self.cell_width, self.row * self.cell_height, self.cell_width, self.cell_height)
        pygame.draw.rect(screen, color, cell)
        # If the cell has a value, draw it on top of the coloured cell
        if self.value:
            self.draw_value(screen)

    def draw_value(self, screen) -> None:
        """
        Draw a value in the cell. For the initial values the font is larger and darker.
        :param screen: Pygame display window
        :return: None
        """

        # Choose black color for initial values and grey for others
        color = settings.BLACK if self.has_initial_value else settings.GREY
        # Choose larger font for initial values
        size = settings.FONT_SIZE_LARGE if self.has_initial_value else settings.FONT_SIZE_NORMAL
        # Create the font object to draw
        font = pygame.font.SysFont("comicsans", size)
        text = font.render(str(self.value), True, color)
        # Calculate the placement for the text
        width_adjustment = (self.cell_width - text.get_width()) // 2
        height_adjustment = (self.cell_height - text.get_height()) // 2
        # Draw the text in the proper position
        screen.blit(text, (self.cell_width * self.col + width_adjustment,
                           self.cell_height * self.row + height_adjustment))


def handle_mouse_click(board, screen) -> None:
    """
    Calculate which cell is clicked and select it. If the click is outside the
    board, do nothing.
    :param board: `Board` class object
    :param screen: Pygame display window
    :return: None
    """
    # Get mouse click coordinates
    x, y = pygame.mouse.get_pos()
    # Check if the click is inside the board
    if y < settings.height:
        # Calculate which row and column contain the clicked cell
        row = y // settings.cell_size
        col = x // settings.cell_size
    # If click outside of the board, do nothing
    else:
        return
    # Select new cell
    board.select_cell(row, col, screen)


def handle_arrow_keys(event, board, screen) -> None:
    """
    Use the arrow keys to move the selected cell to corresponding direction.
    :param event: Pygame event
    :param board: `Board` class object
    :param screen: Pygame display window
    :return: None
    """
    # Get the location of the currently selected cell
    row, col = board.selected_cell
    # Check if any of the arrow keys is pressed
    if event.key == pygame.K_UP:
        row -= 1
    if event.key == pygame.K_DOWN:
        row += 1
    if event.key == pygame.K_LEFT:
        col -= 1
    if event.key == pygame.K_RIGHT:
        col += 1
    board.select_cell(row, col, screen)


def handle_number_keys(event, board):
    if event.key == pygame.K_1:
        board.change_value(1)
    if event.key == pygame.K_2:
        board.change_value(2)
    if event.key == pygame.K_3:
        board.change_value(3)
    if event.key == pygame.K_4:
        board.change_value(4)
    if event.key == pygame.K_5:
        board.change_value(5)
    if event.key == pygame.K_6:
        board.change_value(6)
    if event.key == pygame.K_7:
        board.change_value(7)
    if event.key == pygame.K_8:
        board.change_value(8)
    if event.key == pygame.K_9:
        board.change_value(9)
    if event.key == pygame.K_0 or event.key == pygame.K_BACKSPACE:
        board.change_value(10)


def draw_game_info(screen):
    font = pygame.font.SysFont("Comicsans", settings.FONT_SIZE_INFO)
    text1 = font.render(settings.info1, True, settings.BLACK)
    text2 = font.render(settings.info2, True, settings.BLACK)
    screen.blit(text1, ((settings.w_width - text1.get_width()) / 2, settings.height))
    screen.blit(text2, ((settings.w_width - text2.get_width()) / 2, settings.height + text1.get_height()))


def run_game():
    screen = pygame.display.set_mode((settings.w_width, settings.w_height))
    pygame.display.set_caption("Sudoku Solver")
    screen.fill(settings.WHITE)
    clock = pygame.time.Clock()
    run = True

    board = Board(screen)
    board.draw_cells(screen)

    while run:
        clock.tick(settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.clear_bg_colors()
                if event.button == 1:
                    handle_mouse_click(board, screen)
            if event.type == pygame.KEYDOWN:
                board.clear_bg_colors()
                handle_arrow_keys(event, board, screen)
                handle_number_keys(event, board)
                if event.key == pygame.K_s:
                    board.show_solution(solve(board.puzzle))
                if event.key == pygame.K_v:
                    board.solve_visually()
                if event.key == pygame.K_DELETE:
                    board.clear_cells()
                if event.key == pygame.K_ESCAPE:
                    run = False

        board.update_board(screen)


if __name__ == "__main__":
    run_game()
    pygame.quit()
    print("Sudoku solver closed")


# TODO: Add GUI for settings
# TODO: Add GUI for controls
# TODO: Database for saving the puzzles
