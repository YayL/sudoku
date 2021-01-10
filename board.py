#TODO:
# Puzzle maker:
#  1) Place numbers randomly and check if number is allowed to be there, otherwise loop until found another number or move on
#  2) Solve that puzzle
#  3) Remove squares randomly; Amount removed depends on the difficulty

import pygame
import math


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (20, 20, 20)
        self.board = [[[0 for k in range(5)] for j in range(9)] for i in range(9)]
        self.type = 0  # [0] Main [1] Top-Left [2] Top-Right [3] Bottom-Right [4] Bottom-Left
        # -- States --
        self.presetMode = False
        self.finish = False
        # -- Tile Colors --
        self.normalColors = [(60, 60, 60), (65, 65, 65)]
        self.finishColor = [(37, 115, 40), (45, 130, 42)]
        self.errorColor = (153, 0, 0)
        self.presetColor = (35, 74, 112)
        self.selectedColor = (207, 105, 93)

    def setUp(self, tiles):
        num = [[1, 0, 7], [3, 0, 9], [5, 0, 4], [6, 0, 5], [8, 0, 1],
               [5, 1, 7], [6, 1, 6],
               [3, 2, 6], [4, 2, 1], [5, 2, 3], [8, 2, 7],
               [1, 3, 5], [2, 3, 7], [5, 3, 2], [7, 3, 9], [8, 3, 6],
               [0, 4, 3], [2, 4, 6], [3, 4, 7], [5, 4, 5], [6, 4, 2],
               [1, 5, 8], [3, 5, 1], [4, 5, 9], [6, 5, 7],
               [1, 6, 1], [7, 6, 6], [8, 6, 2],
               [0, 7, 9], [1, 7, 2], [2, 7, 8], [3, 7, 5], [5, 7, 1], [8, 7, 4],
               [1, 8, 6], [3, 8, 4], [7, 8, 8], [8, 8, 5]]

        for l in num:
            self.board[l[0]][l[1]][0] = l[2]
            tiles[l[1] * 9 + l[0]].preset = True

    def getSquare(self, t):
        xInd, yInd = math.floor(t.xInd / 3) * 3, math.floor(t.yInd / 3) * 3
        square = []
        for y in range(3):
            for x in range(3):
                if (xInd + x != t.xInd or yInd + y != t.yInd) and self.board[xInd + x][yInd + y][0] != 0:
                    square.append(self.board[xInd + x][yInd + y][0])
        return square

    def checkFinished(self, tiles):
        for t in tiles:
            if self.board[t.xInd][t.yInd][0] == 0:
                self.finish = False
                return
            if not self.isSafe(t, tiles):
                self.finish = False
                return

        self.finish = True

    def printBoard(self):
        print("---------------------------------------")
        string = ""
        for row in range(len(self.board)):
            if row % 3 == 0 and row != 0:
                string += ("- " + " - "*2 + (" + " + " - "*3)*2 + "\n")
            for col in range(len(self.board[row])):
                if col % 3 == 0 and col != 0:
                    string += "|  "
                string += str(self.board[col][row][0]) + "  "
            string += "\n"
        print(string)

    def isSafe(self, t, tiles):
        x, y = t.xInd, t.yInd
        if self.board[t.xInd][t.yInd][0] != 0:
            for s in self.getSquare(t):
                if s == self.board[x][y][0]:
                    return False
            for temp in tiles:
                if not (temp.xInd == x and temp.yInd == y):
                    if (temp.xInd == x or temp.yInd == y) and self.board[temp.xInd][temp.yInd][0] == self.board[x][y][0] and self.board[x][y][0] != 0:
                        return False

        return True

    def drawBoard(self, win):
        pygame.draw.line(win, [self.color[i]+30 for i in range(3)], (self.width/3 - 1, self.height), (self.width/3 - 1, 0), 2)
        pygame.draw.line(win, [self.color[i]+30 for i in range(3)], ((self.width/3)*2 - 1, self.height), ((self.width/3)*2 - 1, 0), 2)

        pygame.draw.line(win, [self.color[i] + 30 for i in range(3)], (0, self.height/3), (self.width, self.height / 3), 2)
        pygame.draw.line(win, [self.color[i] + 30 for i in range(3)], (0, (self.height/3) * 2 - 1), (self.width, (self.height / 3) * 2 - 1), 2)
