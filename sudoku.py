import pygame as pg

class Board:
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
    offset = 10

    def __init__(self, win, board_size):
        self.win = win
        self.board_size = board_size - (2 * self.offset)
        self.cells = [[Cell(self.win, self.board_size, self.board[i][j], i, j) for j in range(self.row_col)] 
            for i in range(self.row_col)]
        self.selected = None

    def draw(self):
        pg.draw.rect(
            self.win, 
            pg.Color('white'), 
            pg.Rect(self.offset, self.offset, self.board_size, self.board_size), 
            0
        )
        pg.draw.rect(
            self.win, 
            pg.Color('black'), 
            pg.Rect(self.offset, self.offset, self.board_size, self.board_size), 
            4
        )

        gap = self.board_size / self.row_col
        for i in range(1, self.row_col):
            thicc = 1 if i % 3 else 4
            pg.draw.line(
                self.win, 
                pg.Color('black'), 
                (self.offset, i*gap+self.offset), 
                (self.offset+self.board_size, i*gap+self.offset), 
                thicc
            )
            pg.draw.line(
                self.win, 
                pg.Color('black'), 
                (i*gap+self.offset, self.offset), 
                (i*gap+self.offset, self.offset+self.board_size), 
                thicc
            )

        for i in range(self.row_col):
            for j in range(self.row_col):
                self.cells[i][j].draw()

    def place_val(self):
        if self.selected:
            i, j = self.selected
            if self.cells[i][j].tmp_val != 0 and self.cells[i][j].val == 0:
                if self.is_valid(i, j, self.cells[i][j].tmp_val, animated=True):
                    self.cells[i][j].val = self.cells[i][j].tmp_val

    def place_tmp_val(self, val):
        if self.selected:
            i, j = self.selected
            self.cells[i][j].tmp_val = val

    def clear(self):
        if self.selected:
            i, j = self.selected
            self.cells[i][j].clear()

    def select(self, row, col):
        if self.selected:
            i, j = self.selected
            self.cells[i][j].color = (-1, -1, -1)
            self.selected = None

        if self.cells[row][col].mutable:
            self.cells[row][col].color = (0, 0, 255)
            self.selected = (row, col)

    def click(self, pos):
        if pos[0] > self.offset and pos[0] < self.offset+self.board_size:
            if pos[1] > self.offset and pos[1] < self.offset+self.board_size:
                gap = self.board_size / self.row_col
                x = (int)((pos[0] - self.offset) // gap)
                y = (int)((pos[1] - self.offset) // gap)
                return (y, x)

    def solve(self, row, col):
        if row == self.row_col and col == 0:
            self.is_finished()
            return True
        if self.cells[row][col].val != 0:
            return self.solve(row+1 if col == 8 else row, 0 if col == 8 else col+1)

        for i in range(1, 10):
            if self.is_valid(row, col, i):
                self.cells[row][col].val = i
                self.cells[row][col].color = (0, 255, 0)
                self.draw()
                pg.display.update()
                pg.time.delay(100)

                if self.solve(row+1 if col == 8 else row, 0 if col == 8 else col+1):
                    return True

                self.cells[row][col].val = 0
                self.cells[row][col].color = (255, 0, 0)
                self.draw()
                pg.display.update()
                pg.time.delay(100)

        return False

    def is_valid(self, row, col, val, animated=False):
        valid = True
        for i in range(self.row_col):
            a, b = 3 * (row // 3) + i // 3, 3 * (col // 3) + i % 3
            checking = (self.cells[i][col], self.cells[row][i], self.cells[a][b])

            if animated:
                checking[0].color = (0, 255, 0)
                checking[1].color = (0, 255, 0)
                checking[2].color = (0, 255, 0)
                self.draw()
                pg.display.update()
                pg.time.delay(20)
            for cell in checking:
                if cell.val == val:
                    valid = False
                    if animated:
                        cell.color = (255, 0, 0)
                        self.draw()
                        pg.display.update()
                        pg.time.delay(1000)
                if not valid:
                    break
            if animated:
                checking[0].color = (-1, -1, -1)
                checking[1].color = (-1, -1, -1)
                checking[2].color = (-1, -1, -1)
                self.draw()
                pg.display.update()
            if not valid:
                break
        
        if animated and self.selected: 
            i, j = self.selected
            self.cells[i][j].color = (0, 0, 255)

        return valid

    def is_finished(self):
        for i in range(self.row_col):
            for j in range(self.row_col):
                if self.cells[i][j].val == 0: 
                    return False

        for i in range(self.row_col):
            for j in range(self.row_col):
                self.cells[i][j].color = (-1, -1, -1)
                self.cells[i][j].mutable = False
        return True

    def reset(self):
        for i in range(self.row_col):
            for j in range(self.row_col):
                self.cells[i][j].color = (-1, -1, -1)
                self.cells[i][j].clear()
        self.draw()
        pg.display.update()


class Cell:
    row_col = 9
    offset = 10

    def __init__(self, win, board_size, val, row, col, color=(-1, -1, -1)):
        self.win = win
        self.board_size = board_size
        self.val = val
        self.tmp_val = 0
        self.row = row
        self.col = col
        self.color = color
        self.initial = True if val != 0 else False
        self.mutable = True if val == 0 else False

    def draw(self):
        if self.initial:
            fnt = pg.font.Font("Aller_Std_Bd.ttf", 25)
        else:
            fnt = pg.font.Font("Aller_Std_LtIt.ttf", 25)

        gap = self.board_size / self.row_col
        x = self.col * gap + self.offset
        y = self.row * gap + self.offset

        if self.tmp_val != 0 and self.val == 0:
            text = fnt.render(str(self.tmp_val), 1, (200, 200, 200))
            self.win.blit(text, (x+4, y))
        elif self.val != 0:
            text = fnt.render(str(self.val), 1, pg.Color('black'))
            self.win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.color != (-1, -1, -1):
            pg.draw.rect(self.win, self.color, (x, y, gap, gap), 3)

    def clear(self):
        if self.mutable:
            self.val = 0
            self.tmp_val = 0