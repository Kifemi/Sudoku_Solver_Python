import pygame
import settings
import copy
from solver import solve, is_possible

pygame.font.init()


class Board:
    def __init__(self):
        self.width = settings.width
        self.height = settings.height
        self.puzzle = settings.puzzle
        # TODO: Check if the values written by user are valid
        self.current_puzzle = copy.deepcopy(self.puzzle)
        self.cells = [[Cell(self.puzzle[i][j], i, j, self.width, self.height) for j in range(9)] for i in range(9)]
        self.selected_cell = (0, 0)
        self.solution = None

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
        Change the selected cell while resetting the previous values
        :param row: Selected cell's row
        :param col: Selected cell's column
        :param screen: Pygame display window
        :return: None
        """
        # Reset other cells
        for i in range(9):
            for j in range(9):
                self.cells[i][j].is_selected = False

        row %= 9
        col %= 9
        self.cells[row][col].is_selected = True
        self.selected_cell = (row, col)
        # self.cells[self.selected_cell[0]][self.selected_cell[1]].is_selected = True

        # Draw the cells to update the screen.
        self.draw_cells(screen)

    # TODO: at the moment doesn't do anything
    # def update_cells(self):
    #     for i in range(9):
    #         for j in range(9):
    #             self.cells[i][j].value = self.puzzle[i][j]

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

    def clear_errors(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].show_error = False

    def update_puzzle(self, value, row, col) -> None:
        if 0 < value < 10:
            self.current_puzzle[row][col] = value
        elif value == 10:
            self.current_puzzle[row][col] = 0

    def show_solution(self, solution):
        if solution is not None:
            self.solution = solution
            self.current_puzzle = solution
        else:
            print("Puzzle is impossible to solve")
            return
        for i in range(9):
            for j in range(9):
                if not self.cells[i][j].has_initial_value:
                    self.cells[i][j].value = self.solution[i][j]


class Cell:
    def __init__(self, value, row, col, width, height):
        self._value = value
        self.row = row
        self.col = col
        self.cell_width = width // 9
        self.cell_height = height // 9
        self.is_selected = False
        self.has_initial_value = True if self.value else False
        self.show_error = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        if 0 < x < 10:
            self._value = x
        else:
            self._value = 0

    def draw_cell(self, screen) -> None:
        """
        Draw a new value in the cell in question
        :param screen: Pygame display screen
        :return: None
        """

        # Check if the cell is selected and choose corresponding color
        if self.is_selected:
            color = settings.SELECTED_COLOR
        elif self.show_error:
            color = settings.RED
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


def handle_mouse_click(board, screen):
    x, y = pygame.mouse.get_pos()
    row = y // settings.cell_size
    col = x // settings.cell_size
    board.select_cell(row, col, screen)


def handle_arrow_keys(event, board, screen):
    row, col = board.selected_cell
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
    value = 0
    if event.key == pygame.K_1:
        value = 1
    if event.key == pygame.K_2:
        value = 2
    if event.key == pygame.K_3:
        value = 3
    if event.key == pygame.K_4:
        value = 4
    if event.key == pygame.K_5:
        value = 5
    if event.key == pygame.K_6:
        value = 6
    if event.key == pygame.K_7:
        value = 7
    if event.key == pygame.K_8:
        value = 8
    if event.key == pygame.K_9:
        value = 9
    if event.key == pygame.K_0 or event.key == pygame.K_BACKSPACE:
        value = 10
    if value != 0:
        row = board.selected_cell[0]
        col = board.selected_cell[1]
        if not board.cells[row][col].has_initial_value:
            possible = True
            errors = []
            if value != 10:
                possible, errors = is_possible(board.current_puzzle, value, row, col)
            if possible:
                board.cells[row][col].value = value
                board.update_puzzle(value, row, col)
            else:
                for row, col in errors:
                    board.cells[row][col].show_error = True


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

    board = Board()

    while run:
        clock.tick(settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.clear_errors()
                if event.button == 1:
                    handle_mouse_click(board, screen)
            if event.type == pygame.KEYDOWN:
                board.clear_errors()
                handle_arrow_keys(event, board, screen)
                handle_number_keys(event, board)
                if event.key == pygame.K_s:
                    # TODO: check if solver return proper solution
                    board.show_solution(solve(board.puzzle))
                if event.key == pygame.K_DELETE:
                    board.clear_cells()
                if event.key == pygame.K_ESCAPE:
                    run = False

        board.draw_cells(screen)
        board.draw_lines(screen)
        draw_game_info(screen)
        pygame.display.update()


if __name__ == "__main__":
    run_game()
    pygame.quit()
