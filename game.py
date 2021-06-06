import sys, time
import pygame as pg

class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    row_col = 9

    def __init__(self, board_size, offset=10):
        self.board_size = board_size - (2 * offset)
        self.offset = offset

    def draw_background(self, win):
        win.fill(pg.Color('white'))

        pg.draw.rect(
            win, 
            pg.Color('black'), 
            pg.Rect(self.offset, self.offset, self.board_size, self.board_size), 
            4
        )

        gap = self.board_size / self.row_col
        for i in range(1, self.row_col):
            thicc = 1 if i % 3 else 4
            pg.draw.line(
                win, 
                pg.Color('black'), 
                (self.offset, i*gap+self.offset), 
                (self.offset+self.board_size, i*gap+self.offset), 
                thicc
            )
            pg.draw.line(
                win, 
                pg.Color('black'), 
                (i*gap+self.offset, self.offset), 
                (i*gap+self.offset, self.offset+self.board_size), 
                thicc
            )


class Cube:
    row_col = 9

    def __init__(self, board_size, val, x, y):
        self.board_size = board_size
        self.val = val
        self.x = x
        self.y = y

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

def main():
    pg.init()
    win_size = (540, 600)
    win = pg.display.set_mode(win_size)
    pg.display.set_caption("Sudoku Solver")
    board = Grid(win_size[0])

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        board.draw_background(win)
        pg.display.update()


if __name__ == '__main__':
    main()