import pygame
from math import sqrt

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 255, 100)
BLUE = (0, 0, 255)

board = [
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


class Cell:
    def __init__(self, value, position):
        self.value = value
        self.position = position
        self.size = (56, 56)
        self.color = BLACK
        self.font = pygame.font.SysFont("comicsans", 50)
        self.rect = pygame.Rect(self.position, self.size)

    def draw(self, window):
        pygame.draw.rect(window, WHITE, self.rect, 0)
        pygame.draw.rect(window, self.color, self.rect, 1)

        if self.value != 0:
            text = self.font.render(str(self.value), 1, BLUE)
            window.blit(text, self.position)


class Grid:
    def __init__(self, board):
        self.cell_list = [
            [
                Cell(board[row][col], (col * 56 + 48, row * 56 + 48))
                for col in range(len(board))
            ]
            for row in range(len(board))
        ]
        self.board = board

    def solve(self, window, width, height):

        if not (empty_position := self.check_board()):
            return True

        x, y = empty_position

        for num in range(1, 10):
            if self.is_valid(num, empty_position):
                self.board[x][y] = num
                self.cell_list[x][y].value = num
                self.cell_list[x][y].draw(window)
                draw_gird(window, width, height)
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve(window, width, height):
                    return True

                self.board[x][y] = 0
                self.cell_list[x][y].value = 0
                self.cell_list[x][y].draw(window)
                draw_gird(window, width, height)
                pygame.display.update()
                pygame.time.delay(100)

        return False

    def is_valid(self, value, position):
        x, y = position
        max_length = len(board)

        for num in range(len(self.board)):
            if (self.board[x][num] == value and y != num) or (
                self.board[num][y] == value and x != num
            ):
                return False

        box_x = x // int(sqrt(max_length))
        box_y = y // int(sqrt(max_length))

        for row in range(box_x * 3, box_x * 3 + 3):
            for col in range(box_y * 3, box_y * 3 + 3):
                if board[row][col] == value and (row, col) != position:
                    return False

        return True

    def check_board(self):
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[row_index])):
                if not self.board[row_index][col_index]:
                    return row_index, col_index
        return None


def draw_gird(window, width, height):

    x = 48
    y = 48

    for row in range(9):
        for col in range(9):

            if col % 3 == 0 and col != 0:
                pygame.draw.line(window, BLACK, (x, y), (x, height - 48), 5)

            x += 56

        x = 48
        y += 56

        if (row + 1) % 3 == 0 and row != 8:
            pygame.draw.line(window, BLACK, (x, y), (width - 48, y), 5)


class SudokuSolver:
    def __init__(self, width, height):
        self.size = self.width, self.height = width, height
        self.window = pygame.display.set_mode(self.size)
        self.bk_color = WHITE
        self.clock = pygame.time.Clock()
        self.grid = Grid(board)

        self.run()

    def run(self):
        while True:
            # self.clock.tick(60)
            self.event_loop()
            self.window.fill(self.bk_color)

            for row in self.grid.cell_list:
                for cell in row:
                    cell.draw(self.window)

            draw_gird(self.window, self.width, self.height)

            pygame.display.update()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.grid.solve(self.window, self.width, self.height)


if __name__ == "__main__":
    SudokuSolver(600, 600)
