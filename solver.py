def clearBoard(board, tiles):
    for col in range(9):
        for row in range(9):
            for i in range(5):
                if board.board[col][row][i] != 0 and not tiles[row * 9 + col].preset:
                    board.board[col][row][i] = 0


def grid(board, tiles, win, events, draw, running):
    if running:
        for row in range(9):
            for col in range(9):
                if board.board[col][row][0] == 0 and not tiles[row * 9 + col].preset:
                    for num in range(1, 10):

                        preNum = board.board[col][row][0]
                        board.board[col][row][0] = num
                        draw(win, tiles, board, True)
                        running = events(board, tiles, win, running, True)

                        if board.isSafe(tiles[row * 9 + col], tiles):

                            if grid(board, tiles, win, events, draw, running):
                                return True

                            board.board[col][row][0] = 0
                        else:
                            board.board[col][row][0] = preNum
                    return False
        if board.finish:
            return True
        return False


def solve(board, tiles, win, events, draw, running):
    clearBoard(board, tiles)
    if grid(board, tiles, win, events, draw, running):
        print("Sudoku has been solved")
    else:
        print("Did not find a solution")
