import re

from tiles import *
import solver

WIDTH, HEIGHT = 900, 900

pattern = "[1-9]"


def draw(win, tiles, board, isSolving=False):
    win.fill((20, 20, 20))

    board.checkFinished(tiles)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for t in tiles:
        if not board.finish:
            if not board.isSafe(t, tiles):
                t.error = True
            elif t.error:
                t.error = False

            if t.error:
                t.tilesRender(win, board, board.errorColor)
            elif t.preset:
                t.tilesRender(win, board, board.presetColor)
            elif t.selected and not isSolving:
                t.tilesRender(win, board, board.selectedColor)
            elif (t.yInd*9 + t.xInd) % 2 == 0:
                t.tilesRender(win, board, board.normalColors[1])
            else:
                t.tilesRender(win, board, board.normalColors[0])
            if (t.error or t.preset) and not isSolving:
                t.tilesUpdate(win, board, mouse, click, tiles, False)
                continue
            if not isSolving:
                t.tilesUpdate(win, board, mouse, click, tiles)
        else:
            if (t.yInd*9 + t.xInd) % 2 == 0:
                t.tilesRender(win, board, board.finishColor[0])
            else:
                t.tilesRender(win, board, board.finishColor[1])

    board.drawBoard(win)

    pygame.display.update()


def events(board, tiles, win, running):

    for event in pygame.event.get():

        # -- Quit game handling --
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        # -- Key press handling --
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                for t in tiles:
                    if t.selected and (not t.preset or board.presetMode):
                        t.error = False
                        t.preset = False
                        for i in range(5):
                            board.board[t.xInd][t.yInd][i] = 0
            key = pygame.key.name(event.key)
            if re.match(pattern, key):
                for t in tiles:
                    if t.selected and (not t.preset or board.presetMode):
                        board.board[t.xInd][t.yInd][board.type] = int(key)
                        if board.presetMode:
                            t.preset = True
            if event.key == pygame.K_TAB:
                board.presetMode = True if board.presetMode is False else False
            elif event.key == pygame.K_w:
                board.type = 0
            elif event.key == pygame.K_q:
                board.type -= 1 if board.type >= 1 else board.type-4
            elif event.key == pygame.K_e:
                board.type += 1 if board.type <= 3 else 1-board.type
            elif event.key == pygame.K_BACKSPACE:
                for t in tiles:
                    if t.selected:
                        board.board[t.xInd][t.yInd][board.type] = 0
                        t.preset = False
            elif event.key == pygame.K_s:
                solver.solve(board, tiles, win, events, draw)
            elif event.key == pygame.K_x:
                board.setUp(tiles)
            elif event.key == pygame.K_p:
                board.printBoard()

    return running


def main():
    board = Board(WIDTH, HEIGHT)
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    tiles = [Tiles(i % 9, math.floor(i / 9), WIDTH / 9, HEIGHT / 9) for i in range(9 * 9)]
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        running = events(board, tiles, win, running)
        draw(win, tiles, board)


main()
