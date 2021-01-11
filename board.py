#TODO:
# Puzzle maker:
#  1) Place numbers randomly and check if number is allowed to be there, otherwise loop until found another number or move on
#  2) Solve that puzzle
#  3) Remove squares randomly; Amount removed depends on the difficulty
import random
import pygame
import math

import solver


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (20, 20, 20)
        self.board = [[[0 for k in range(5)] for j in range(9)] for i in range(9)]
        self.randomness = 30
        self.difficulty = 1
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

    def setUp(self, tiles, win, draw, events):
        solver.clearBoard(self, tiles)
        for row in range(9):
            for col in range(9):
                num = random.randint(1, 10 + self.randomness)
                if num < 10:
                    if self.isSafe(tiles[row * 9 + col], tiles, num):
                        self.board[col][row][0] = num
                        tiles[row * 9 + col].preset = True

        if not solver.start(self, tiles, win, draw, events, True):
            self.setUp(tiles, win, draw, events)

        for row in range(9):
            for col in range(9):
                if random.randint(0, math.floor((self.difficulty/2))+1) >= 1:
                    self.board[col][row][0] = 0
                    tiles[row*9 + col].preset = False
                else:
                    tiles[row * 9 + col].preset = True

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

    def isSafe(self, t, tiles, value=None):
        x, y = t.xInd, t.yInd

        if value is None:
            value = self.board[x][y][0]

        if value != 0:
            for s in self.getSquare(t):
                if s == value:
                    return False
            for temp in tiles:
                if not (temp.xInd == x and temp.yInd == y):
                    if (temp.xInd == x or temp.yInd == y) and self.board[temp.xInd][temp.yInd][0] == value:
                        return False

        return True

    def drawBoard(self, win):
        pygame.draw.line(win, [self.color[i]+30 for i in range(3)], (self.width/3 - 1, self.height), (self.width/3 - 1, 0), 2)
        pygame.draw.line(win, [self.color[i]+30 for i in range(3)], ((self.width/3)*2 - 1, self.height), ((self.width/3)*2 - 1, 0), 2)

        pygame.draw.line(win, [self.color[i] + 30 for i in range(3)], (0, self.height/3), (self.width, self.height / 3), 2)
        pygame.draw.line(win, [self.color[i] + 30 for i in range(3)], (0, (self.height/3) * 2 - 1), (self.width, (self.height / 3) * 2 - 1), 2)
