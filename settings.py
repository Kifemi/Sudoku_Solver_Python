# Constants
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SELECTED_COLOR = (0, 255, 0)
GREY = (120, 120, 120)
RED = (255, 0, 0)
BLUE = (71, 185, 230)
DARK_BLUE = (0, 0, 255)

FONT_SIZE_LARGE = 50
FONT_SIZE_NORMAL = 40
FONT_SIZE_INFO = 20

# window settings
w_width = 540
w_height = 640

info1 = "C: Show controls || S: Show settings"

# board settings
width = 540
height = 540
cell_size = width // 9

# button settings
btn_width = width / 2
btn_height = (w_height - height) / 2
btn_relief = 5
btn_top_color = "#348ceb"
btn_bottom_color = "#3434eb"


# controls
controls = {"Select cell": "Arrow keys",
            "Clear cell": "0 or Backspace",
            "Clear board": "Del",
            "Close game": "Esc",
            "Solve": "Space",
            "Solve visually": "V",
            }




# puzzles
puzzle_normal = [
    [0, 0, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 0, 0, 1, 3],
    [6, 0, 0, 0, 0, 0, 8, 5, 7],
    [2, 8, 0, 9, 0, 0, 5, 6, 0],
    [0, 1, 0, 0, 0, 0, 0, 7, 0],
    [9, 0, 5, 0, 0, 0, 0, 0, 0],
    [3, 0, 9, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 9, 6, 0, 0, 0],
    [0, 0, 1, 0, 0, 3, 2, 0, 0],
]

puzzle_easy = [
    [6, 0, 9, 5, 0, 4, 0, 0, 1],
    [0, 0, 5, 0, 2, 0, 8, 0, 4],
    [0, 0, 0, 0, 0, 6, 5, 9, 0],
    [0, 0, 0, 2, 5, 9, 3, 0, 0],
    [5, 0, 3, 1, 0, 0, 0, 8, 0],
    [9, 0, 1, 0, 0, 0, 7, 2, 5],
    [1, 0, 0, 4, 0, 8, 9, 0, 0],
    [0, 9, 0, 0, 1, 0, 6, 5, 0],
    [8, 0, 2, 0, 0, 0, 0, 4, 0],
]

puzzle_hard = [
    [0, 0, 8, 0, 0, 5, 0, 9, 0],
    [0, 2, 0, 0, 0, 8, 1, 0, 5],
    [7, 1, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 4, 0, 9, 0, 0, 0, 7],
    [3, 0, 0, 0, 0, 6, 0, 0, 4],
    [0, 0, 0, 8, 7, 0, 5, 0, 1],
    [0, 6, 0, 5, 0, 0, 0, 0, 0],
]

puzzle_empty = [[0 for _ in range(9)] for _ in range(9)]

puzzle_impossible = [
    [0, 0, 0, 0, 8, 0, 0, 0, 8],
    [0, 0, 0, 5, 0, 0, 0, 1, 3],
    [6, 0, 0, 0, 0, 0, 8, 5, 7],
    [2, 8, 0, 9, 0, 0, 5, 6, 0],
    [0, 1, 0, 0, 0, 0, 0, 7, 0],
    [9, 0, 5, 0, 0, 0, 0, 0, 0],
    [3, 0, 9, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 9, 6, 0, 0, 0],
    [0, 0, 1, 0, 0, 3, 2, 0, 0],
]

puzzle_very_hard = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
]

puzzle_anti_backtracking = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 8, 5],
    [0, 0, 1, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 7, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 1, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 7, 3],
    [0, 0, 2, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 9],
]
