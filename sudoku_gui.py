import pygame
from math import sqrt
from colors import BLACK, GREY, WHITE

pygame.font.init()

# Test Sudoku Board
# CREDIT: https://en.wikipedia.org/wiki/Sudoku
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


# Main Class That Defines Each Cell of the Grid (9*9)
class Cell:
    def __init__(self, value, position):
        self.color = GREY
        self.value = value
        self.size = (56, 56)
        self.position = self.x, self.y = position
        self.font = pygame.font.SysFont("comicsans", 50)
        self.rect = pygame.Rect(self.position, self.size)

    def draw(self, window):

        """
        Responsible for Drawing the Cell based on the Class's Value

        Args:
            window: Main Window that you want the cell drawn upon
        """

        pygame.draw.rect(window, WHITE, self.rect, 0)
        pygame.draw.rect(window, self.color, self.rect, 1)

        if self.value != 0:
            text = self.font.render(str(self.value), 1, self.color)
            window.blit(
                text, ((self.x + text.get_width()), (self.y + text.get_height() // 3)),
            )


class Grid:
    def __init__(self, window, width, height, board, instant):
        self.window = window
        self.width = width
        self.height = height
        self.board = board

        self.side_buffer = 48
        self.wait_time = 50
        if instant:
            self.wait_time = 0

        self.cells = [
            [
                Cell(board[row][col], (col * 56 + 48, row * 56 + 48))
                for col in range(len(self.board))
            ]
            for row in range(len(self.board))
        ]

    def draw_grid(self):

        """Responsible for calling every Cell in Cells and calling their Draw Method"""

        for row in self.cells:
            for cell in row:
                cell.draw(self.window)
        self.draw_lines()

    def draw_lines(self):

        """Draws all of the lines that make up the 3 * 3 Grid's main Squares"""

        x = y = self.side_buffer

        for row in range(len(self.board)):
            for col in range(len(self.board)):

                if col % 3 == 0 and col != 0:
                    pygame.draw.line(
                        self.window,
                        BLACK,
                        (x, y),
                        (x, self.height - self.side_buffer),
                        5,
                    )

                x += 56

            x = self.side_buffer
            y += 56

            if (row + 1) % 3 == 0 and row != 8:
                pygame.draw.line(
                    self.window, BLACK, (x, y), (self.width - self.side_buffer, y), 5
                )

    def solve(self):

        """Backtracking Algorithm that solves Sudoku Board"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if not (empty_position := self.check_board()):
            return True

        x, y = empty_position

        for num in range(1, 10):
            if self.is_valid(num, empty_position):
                self.board[x][y] = num
                self.cells[x][y].value = num

                self.draw_grid()

                pygame.display.update()
                pygame.time.delay(self.wait_time)

                if self.solve():
                    return True

                self.board[x][y] = 0
                self.cells[x][y].value = 0

                self.draw_grid()

                pygame.display.update()
                pygame.time.delay(self.wait_time)

        return False

    def is_valid(self, value, position):

        """
        Checks whether given Value is valid based on Position

        Args:
            value (int): Value to be tested
            position (tuple): X and Y Coordinates of a Cell

        Returns:
            bool: True if Value is valid and False if not valid
        """

        x, y = position
        max_length = len(self.board)

        for num in range(len(self.board)):
            if (self.board[x][num] == value and y != num) or (
                self.board[num][y] == value and x != num
            ):
                return False

        box_x = x // int(sqrt(max_length))
        box_y = y // int(sqrt(max_length))

        for row in range(box_x * 3, box_x * 3 + 3):
            for col in range(box_y * 3, box_y * 3 + 3):
                if self.board[row][col] == value and (row, col) != position:
                    return False

        return True

    def check_board(self):

        """Checks for an empty position"""

        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[row_index])):
                if not self.board[row_index][col_index]:
                    return row_index, col_index
        return None


class SudokuSolver:
    def __init__(self, width, height, instant=False):
        self.size = self.width, self.height = width, height
        self.window = pygame.display.set_mode(self.size)
        self.bk_color = WHITE
        self.grid = Grid(self.window, self.width, self.height, sudoku_board, instant)

        self.run()

    def run(self):

        """Main Run Method"""

        while True:
            self.window.fill(self.bk_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.grid.solve()

            self.grid.draw_grid()

            pygame.display.update()


if __name__ == "__main__":
    SudokuSolver(600, 600, instant=True)
