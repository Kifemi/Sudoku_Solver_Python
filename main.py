import os

import pygame
import settings
import copy
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:  # python 2
    import Tkinter as tk
    from Tkinter import messagebox

import puzzles_db
from solver import solve, is_possible, check_solution
import solver_visual


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.width = settings.width
        self.height = settings.height
        self.puzzle = puzzles_db.load_puzzle(1)
        self._current_puzzle = None
        self.cells = [[Cell(self.puzzle[i][j], i, j, self.width, self.height, self.screen) for j in range(9)] for i in
                      range(9)]
        self.selected_cell = (0, 0)

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

    def load_puzzle(self, puzzle=None, solution=None, clear_initials=False) -> None:
        """
        Initializes the starting position of a puzzle. If new puzzle is provided, load it and if no puzzle is provided
        load the current puzzle's starting position. If solution is given as an argument, load the solved board.
        :param puzzle: Starting position of the puzzle.
        :param solution: Solution for a current sudoku.
        :param clear_initials: True or False depending does the sudoku need completely be cleared.
        :return: None
        """
        # TODO: both puzzle and solution are None?
        # TODO: is clear initials required? solution is enough?
        if puzzle:
            self.puzzle = puzzle
            self.current_puzzle = self.puzzle
        self.clear_cells(clear_initials=clear_initials)
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j]:
                    self.cells[i][j].has_initial_value = True
                if solution is None:
                    self.cells[i][j].value = self.puzzle[i][j]
                else:
                    self.cells[i][j].value = solution[i][j]
        if solution:
            self.current_puzzle = solution
        self.update_board(self.screen)

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
            else:
                for row, col in errors:
                    self.cells[row][col].show_error = True
                    self.cells[row][col].draw_cell(self.screen)

    def clear_cells(self, clear_initials=False) -> None:
        """
        Clear every cell except the ones with initial values.
        :param clear_initials: Determine if the initial values are cleared.
        :return: None
        """
        self.current_puzzle = self.puzzle
        for i in range(9):
            for j in range(9):
                if not self.cells[i][j].has_initial_value:
                    self.cells[i][j].value = 0
                elif clear_initials:
                    self.cells[i][j].value = 0
                    self.cells[i][j].has_initial_value = False

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
                self.update_board(self.screen)
                show_end_screen("Congratulations! You solved the sudoku")
        elif value == 10:
            self.current_puzzle[row][col] = 0

    def show_solution(self, solution):
        if solution is None:
            show_end_screen("Sudoku is impossible to solve")
            return
        self.load_puzzle(solution=solution)
        show_end_screen("Sudoku solved by non-visual backtracking")

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
        else:
            value_found = False
        self.update_board(self.screen)
        return value_found

    def solve_visually(self):
        run = True
        color = list(settings.DARK_BLUE)

        while run:
            possible_values = [[solver_visual.get_possible_values(self.current_puzzle, i, j) for j in range(9)]
                               for i in range(9)]

            if self.solve_unique_values(solver_visual.fill_unique, possible_values, color):
                continue
            if self.solve_unique_values(solver_visual.fill_square, possible_values, color):
                continue
            if self.solve_unique_values(solver_visual.fill_row, possible_values, color):
                continue
            if self.solve_unique_values(solver_visual.fill_col, possible_values, color):
                continue

            if not check_solution(self.current_puzzle):
                solver_visual.backtracking(self, self.screen)
                self.clear_bg_colors()
                self.draw_cells(self.screen)
                self.update_board(self.screen)

            run = False

        if check_solution(self.current_puzzle):
            show_end_screen("Sudoku solved by visual backtracking")
        else:
            show_end_screen("Impossible sudoku (Visual backtracking)")
            self.clear_cells()


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


class Button:
    def __init__(self, screen, text, pos):
        self.screen = screen

        # Colors
        self.top_color = settings.btn_top_color
        self.bottom_color = settings.btn_bottom_color
        # Text
        self.text = text
        self.text_font = pygame.font.SysFont("comicsans", 20)
        self.text_render = self.text_font.render(str(self.text), True, settings.BLACK)
        self.text_rect = self.text_render.get_rect()
        # Location
        self.pos_x, self.pos_y = pos
        self.top_part = pygame.Rect(self.pos_x, self.pos_y, settings.btn_width,
                                    settings.btn_height - settings.btn_relief)
        self.bottom_part = pygame.Rect(self.pos_x, self.pos_y + settings.btn_relief, settings.btn_width,
                                       settings.btn_height - settings.btn_relief)
        # Disabled
        # TODO: No effect yet
        if self.text != "Save":
            self.is_disabled = False
        else:
            self.is_disabled = True

    def draw_button(self):
        self.text_rect.center = self.top_part.center
        if self.is_disabled:
            self.top_color = settings.btn_top_disabled
            self.bottom_color = settings.btn_bottom_disabled
        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_part, border_radius=15)
        pygame.draw.rect(self.screen, self.top_color, self.top_part, border_radius=15)
        self.screen.blit(self.text_render, self.text_rect)

    def check_click(self):
        self.top_color = settings.btn_bottom_color
        self.bottom_color = settings.BLACK
        self.draw_button()
        pygame.display.update()

    def reset_click(self):
        self.top_color = settings.btn_top_color
        self.bottom_color = settings.btn_bottom_color
        self.draw_button()


def handle_mouse_click(board, screen, buttons) -> None:
    """
    Calculate which cell is clicked and select it. If the click is outside the
    board, do nothing.
    :param board: `Board` class object
    :param screen: Pygame display window
    :param buttons: List of all `Button` class objects
    :return: None
    """
    # Get mouse click coordinates
    x, y = pygame.mouse.get_pos()
    # Check if the click is inside the board
    if y < settings.height:
        # Calculate which row and column contain the clicked cell
        row = y // settings.cell_size
        col = x // settings.cell_size
        # Select new cell
        board.select_cell(row, col, screen)
    elif settings.height <= y <= settings.w_height:
        game_settings, controls, create, save, puzzles, close = buttons
        if game_settings.top_part.collidepoint(x, y):
            game_settings.check_click()
            open_settings()
        elif controls.top_part.collidepoint(x, y):
            controls.check_click()
            show_controls()
        elif create.top_part.collidepoint(x, y):
            setup_puzzle(board)
        elif save.top_part.collidepoint(x, y):
            # if not save.is_disabled:
            save_puzzle(board)
        elif puzzles.top_part.collidepoint(x, y):
            puzzles.check_click()
            puzzle_id = open_puzzles_db()
            if puzzle_id is not None:
                new_puzzle = puzzles_db.load_puzzle(puzzle_id)
                board.load_puzzle(puzzle=new_puzzle, clear_initials=True)
        elif close.top_part.collidepoint(x, y):
            exit()
        for button in buttons:
            button.reset_click()


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


def handle_number_keys(event, board) -> None:
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


def draw_buttons(buttons) -> None:
    for button in buttons:
        button.draw_button()


def center_tk_window(window, width, height) -> None:
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_x = (screen_width - width) / 2
    window_y = (screen_height - height) / 2

    window.geometry("%dx%d+%d+%d" % (width, height, window_x, window_y))


def center_pygame_window(screen_info) -> tuple:
    window_x = (screen_info.current_w - settings.w_width) // 2
    window_y = (screen_info.current_h - settings.w_height) // 2

    return window_x, window_y


def locate_puzzle_list(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_x = (screen_width + settings.w_width) / 2
    window_y = (screen_height - settings.p_height) / 2 - 30

    return settings.p_width, settings.p_height, window_x, window_y
    # window.geometry("%dx%d+%d+%d" % (settings.p_width, settings.p_height, window_x, window_y))


def setup_puzzle(board) -> None:
    board.puzzle = [[0 for _ in range(9)] for _ in range(9)]
    board.clear_cells(clear_initials=True)


def save_puzzle(board) -> None:
    def save():
        nonlocal name
        name = entry.get().strip()
        nonlocal saving

        if not name:
            messagebox.showwarning(title="Warning!", message="Invalid name")
            entry.delete(0, tk.END)
        else:
            saving = True
            window.destroy()

    def close():
        window.destroy()

    saving = False
    name = None

    window = tk.Tk()
    window.title("Save puzzle")
    center_tk_window(window, 250, 50)
    entry = tk.Entry(window, width=20)
    save_btn = tk.Button(window, text="Save", command=save)
    close_btn = tk.Button(window, text="Close", command=close)
    entry.insert(0, "Name")

    entry.pack(pady=2)
    # TODO: fix button placement
    save_btn.pack(pady=2, padx=58, side=tk.LEFT)
    close_btn.pack(pady=2, side=tk.LEFT)
    window.mainloop()

    if saving:
        if puzzles_db.check_name(name):
            puzzles_db.add_puzzle(name, board.current_puzzle)
            board.load_puzzle(puzzle=board.current_puzzle)
        else:
            messagebox.showwarning("Name is already taken")


def show_controls() -> None:
    """
    Open a Tkinter window where all the control buttons are displayed
    :return: None
    """
    window = tk.Tk()
    window.title("Controls")
    center_tk_window(window, 200, 150)
    controls_image = tk.PhotoImage(file="settings.png")
    window.iconphoto(True, controls_image)

    row = 0
    for key, value in settings.controls.items():
        tk.Label(window, text=f"{key}: ").grid(row=row, column=0)
        tk.Label(window, text=f"{value}").grid(row=row, column=1)
        row += 1

    window.mainloop()


def open_settings() -> None:
    window = tk.Tk()
    window.title("Settings")
    center_tk_window(window, 400, 400)
    settings_image = tk.PhotoImage(file="settings.png")
    window.iconphoto(True, settings_image)

    window.mainloop()


def open_puzzles_db():
    def on_select(event):
        nonlocal _selected_puzzle
        if listbox.curselection()[0] >= 0:
            _selected_puzzle = listbox.curselection()[0] + 1

    def load():
        nonlocal _selected_puzzle, window, return_value
        if _selected_puzzle is None:
            pass
        else:
            return_value = _selected_puzzle
            window.destroy()

    return_value = None
    _selected_puzzle = None
    window = tk.Tk()
    window.title("Settings")
    window.geometry("%dx%d+%d+%d" % locate_puzzle_list(window))
    settings_image = tk.PhotoImage(file="settings.png")
    window.iconphoto(True, settings_image)

    window.columnconfigure(0, weight=2)

    window.rowconfigure(0, weight=0)
    window.rowconfigure(1, weight=5)
    window.rowconfigure(2, weight=1)

    tk.Label(window, text="Puzzles").grid(row=0, column=0)

    listbox = tk.Listbox(window)
    listbox.grid(row=1, column=0, sticky="nsew", padx=(30, 30))
    listbox.config(border=2, relief="sunken")

    scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.grid(row=1, column=0, sticky="nse", padx=(0, 30))
    listbox["yscrollcommand"] = scrollbar.set
    listbox.bind("<<ListboxSelect>>", on_select)

    load_btn = tk.Button(window, text="Load", command=load)
    load_btn.grid(row=2)
    load_btn.config(border=2)

    for puzzle in puzzles_db.load_puzzles():
        listbox.insert(tk.END, puzzle[0])

    window.mainloop()
    return return_value if return_value else None


def show_end_screen(text) -> None:
    window = tk.Tk()
    window.title("Sudoku")
    center_tk_window(window, 400, 80)

    message = tk.Label(window, text=text, padx=20, pady=10)
    message.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
    button = tk.Button(window, text="OK", command=lambda: window.destroy())
    button.pack(side=tk.BOTTOM, fill=tk.NONE, expand=tk.YES)
    window.mainloop()


def check_events(board, screen, buttons) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.clear_bg_colors()
            if event.button == 1:
                handle_mouse_click(board, screen, buttons)
        if event.type == pygame.KEYDOWN:
            board.clear_bg_colors()
            handle_arrow_keys(event, board, screen)
            handle_number_keys(event, board)
            if event.key == pygame.K_SPACE:
                board.show_solution(solve(board.puzzle))
            if event.key == pygame.K_v:
                board.solve_visually()
            if event.key == pygame.K_DELETE:
                board.clear_cells()
            if event.key == pygame.K_c:
                show_controls()
            if event.key == pygame.K_s:
                open_settings()
            if event.key == pygame.K_ESCAPE:
                return False
    return True


def run_game():
    screen_info = pygame.display.Info()
    os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % center_pygame_window(screen_info)
    screen = pygame.display.set_mode((settings.w_width, settings.w_height))
    pygame.display.set_caption("Sudoku Solver")

    screen.fill(settings.WHITE)
    clock = pygame.time.Clock()
    run = True

    board = Board(screen)
    board.draw_cells(screen)

    # Create Buttons
    btn_settings = Button(screen, "Settings", (0, settings.height))
    btn_controls = Button(screen, "Controls", (settings.btn_width, settings.height))
    btn_create = Button(screen, "Create", (0, settings.height + settings.btn_height))
    btn_save = Button(screen, "Save", (settings.btn_width, settings.height + settings.btn_height))
    btn_puzzles = Button(screen, "Puzzles", (0, settings.height + settings.btn_height * 2))
    btn_close = Button(screen, "Close", (settings.btn_width, settings.height + settings.btn_height * 2))
    buttons = [btn_settings, btn_controls, btn_create, btn_save, btn_puzzles, btn_close]
    draw_buttons(buttons)

    # main loop
    while run:
        clock.tick(settings.FPS)
        run = check_events(board, screen, buttons)
        board.update_board(screen)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    puzzles_db.initialize_db()
    run_game()
    pygame.quit()
    puzzles_db.close_db()
    print("Sudoku solver closed")
