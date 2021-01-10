from board import *

pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans', 80)
myfont2 = pygame.font.SysFont('Comic Sans', 30)


class Tiles:

    def __init__(self, x, y, width, height):
        self.xInd = x
        self.yInd = y
        self.x = x*width
        self.y = y*height
        self.width = width
        self.height = height
        self.selected = False
        # -- States --
        self.error = False
        self.preset = False

    def tilesRender(self, win, board, color):
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))

        for i in range(5):
            val = board.board[self.xInd][self.yInd][i]
            if i >= 1:
                text = myfont2.render(str(val), False, (190, 190, 190))
            else:
                text = myfont.render(str(val), False, (190, 190, 190))

            width = text.get_width()
            height = text.get_height()

            if i == 0:
                pos = (self.x + (self.width-width)/2, self.y + (self.height-height)/2)
            elif i == 1:
                pos = (self.x + 5, self.y + 5)
            elif i == 2:
                pos = (self.x + self.width - width - 5, self.y + 5)
            elif i == 3:
                pos = (self.x + 5, self.y + self.height - height - 5)
            else:
                pos = (self.x + self.width - width - 5, self.y + self.height - height - 5)

            if val != 0:
                win.blit(text, pos)

    def tilesUpdate(self, win, board, mouse, click, tiles, optional=True):
        if self.x+self.width > mouse[0] > self.x and self.y+self.height > mouse[1] > self.y:  # If mouse is in button
            if click[2] == 1 and self.selected:
                self.selected = False
            if click[0] == 1:
                board.type = 0
            if click[0] == 1 or self.selected:
                for j in range(9*9):
                    if tiles[j] != self:
                        tiles[j].selected = False
                    self.selected = True
                if optional:
                    self.tilesRender(win, board, board.selectedColor)
            else:
                self.tilesRender(win, board, (55, 55, 55))
