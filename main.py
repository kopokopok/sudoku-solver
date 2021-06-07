from sudoku import Board
import sys, time
import pygame as pg

def draw_game(win, board, time, completed):
    win.fill(pg.Color('white'))
    # Draw time
    fnt = pg.font.Font("Aller_Std_Bd.ttf", 25)
    text = fnt.render("Time:  " + format_time(time), 1, pg.Color('black'))
    win.blit(text, (540 - 150, 550))
    # Draw completed
    if completed:
        text = fnt.render("Completed!!", 1, pg.Color('black'))
        win.blit(text, (10, 550))
    # Draw sudoku board
    board.draw()


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    res = str(minute) + ":" + str(sec).zfill(2)
    return res


def main():
    pg.init()
    win_size = (540, 600)
    win = pg.display.set_mode(win_size)
    pg.display.set_caption("Sudoku Solver")
    board = Board(win, win_size[0])
    key = None
    start = time.time()
    play_time = 0
    completed = False

    while True:
        if not completed: play_time = round(time.time() - start)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_1 or event.key == pg.K_KP1:
                    key = 1
                elif event.key == pg.K_2 or event.key == pg.K_KP2:
                    key = 2
                elif event.key == pg.K_3 or event.key == pg.K_KP3:
                    key = 3
                elif event.key == pg.K_4 or event.key == pg.K_KP4:
                    key = 4
                elif event.key == pg.K_5 or event.key == pg.K_KP5:
                    key = 5
                elif event.key == pg.K_6 or event.key == pg.K_KP6:
                    key = 6
                elif event.key == pg.K_7 or event.key == pg.K_KP7:
                    key = 7
                elif event.key == pg.K_8 or event.key == pg.K_KP8:
                    key = 8
                elif event.key == pg.K_9 or event.key == pg.K_KP9:
                    key = 9
                elif event.key == pg.K_BACKSPACE:
                    board.clear()
                    key = None
                elif event.key == pg.K_RETURN:
                    board.place_val()
                    key = None
                    if board.is_finished():
                        play_time = round(time.time() - start)
                        completed = True
                elif event.key == pg.K_SPACE:
                    board.reset()
                    board.solve(0, 0)
                    play_time = round(time.time() - start)
                    completed = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.place_tmp_val(key)

        draw_game(win, board, play_time, completed)
        pg.display.update()


if __name__ == '__main__':
    main() 