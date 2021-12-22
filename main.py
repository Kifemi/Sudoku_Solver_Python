import pygame
import settings
from solver import solve

pygame.font.init()


class Board:
    def __init__(self):
        self.width = settings.width
        self.height = settings.height
        self.puzzle = settings.puzzle
        self.cells = [[Cell(self.puzzle[i][j], i, j, self.width, self.height) for j in range(9)] for i in range(9)]
        self.selected_cell = (0, 0)

    def draw_lines(self, screen):
        # Draw horizontal and vertical lines
        cell_size = self.width // 9
        for i in range(10):
            width = 1
            if i % 3 == 0:
                width = 5
            start_pos_horizontal = (0, i * cell_size)
            end_pos_horizontal = (self.width, i * cell_size)
            pygame.draw.line(screen, settings.BLACK, start_pos_horizontal, end_pos_horizontal, width)
            start_pos_vertical = (i * cell_size, 0)
            end_pos_vertical = (i * cell_size, self.height)
            pygame.draw.line(screen, settings.BLACK, start_pos_vertical, end_pos_vertical, width)

    def draw_cells(self, screen):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw_cell(screen)

    def select_cell(self, row, col, screen):
        # Reset other cells
        for i in range(9):
            for j in range(9):
                self.cells[i][j].is_selected = False

        row %= 9
        col %= 9
        self.cells[row][col].is_selected = True
        self.selected_cell = (row, col)
        # print(self.selected_cell)
        self.draw_cells(screen)


class Cell:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.cell_width = width // 9
        self.cell_height = height // 9
        self.is_selected = False
        self.has_initial_value = True if self.value else False

    def draw_cell(self, screen):
        if self.is_selected:
            color = settings.SELECTED_COLOR
        else:
            color = settings.WHITE
        cell = pygame.Rect(self.col * self.cell_width, self.row * self.cell_height, self.cell_width, self.cell_height)
        pygame.draw.rect(screen, color, cell)
        if self.value:
            self.draw_value(screen)

    def draw_value(self, screen):
        color = settings.BLACK if self.has_initial_value else settings.GREY
        size = settings.FONT_SIZE_LARGE if self.has_initial_value else settings.FONT_SIZE_NORMAL
        font = pygame.font.SysFont("comicsans", size)
        text = font.render(str(self.value), True, color)
        width_adjustment = (self.cell_width - text.get_width()) // 2
        height_adjustment = (self.cell_height - text.get_height()) // 2
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


def handle_number_keys(event, board, screen):
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
    if event.key == pygame.K_0:
        value = 10
    if event.key == pygame.K_BACKSPACE:
        value = 10
    if value and not board.cells[board.selected_cell[0]][board.selected_cell[1]].has_initial_value:
        if value == 10:
            board.cells[board.selected_cell[0]][board.selected_cell[1]].value = 0
        else:
            board.cells[board.selected_cell[0]][board.selected_cell[1]].value = value




def run_game():
    screen = pygame.display.set_mode((settings.width, settings.height))
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
                if event.button == 1:
                    handle_mouse_click(board, screen)
            if event.type == pygame.KEYDOWN:
                handle_arrow_keys(event, board, screen)
                handle_number_keys(event, board, screen)

        board.draw_cells(screen)
        board.draw_lines(screen)
        pygame.display.update()


if __name__ == "__main__":
    run_game()
    pygame.quit()
