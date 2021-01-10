def clearBoard(board, tiles):
    for col in range(9):
        for row in range(9):
            for i in range(5):
                if board.board[col][row][i] != 0 and not tiles[row * 9 + col].preset:
                    board.board[col][row][i] = 0


def grid(board, tiles, win, events, draw):
    for row in range(9):
        for col in range(9):
            if board.board[col][row][0] == 0 and not tiles[row * 9 + col].preset:
                for num in range(1, 10):

                    if board.isSafe(tiles[row * 9 + col], tiles, num):

                        board.board[col][row][0] = num

                        draw(win, tiles, board, True)

                        if grid(board, tiles, win, events, draw):
                            return True

                        board.board[col][row][0] = 0
                return False
    if board.finish:
        return True
    return False


def solve(board, tiles, win, events, draw):
    clearBoard(board, tiles)
    if grid(board, tiles, win, events, draw):
        print("Sudoku has been solved")
    else:
        print("Did not find a solution")
