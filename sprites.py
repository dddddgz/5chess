import pygame

class PickBox(pygame.sprite.Sprite):
    def __init__(self):
        """
        选择框
        """
        pygame.sprite.Sprite.__init__(self)
        # 像素范围是[0, width)
        width = 50
        self.turn = BlackChess
        self.images = [pygame.Surface((width,) * 2).convert_alpha() for _ in [1, 2]]
        self.image = self.images[0]
        # 不同系统间图片的默认背景色可能会有所差异，提前设置好
        # (r, g, b, a)
        self.image.fill((0, 50, 0, 255))
        # 留border个像素出来
        border = 3
        self.image.fill((0, 0, 0, 0), (border,) * 2 + (width - 1 - border,) * 2)
        self.image = self.images[1]
        self.image.fill((255, 255, 255, 255))
        self.image.fill((0, 0, 0, 0), (border,) * 2 + (width - 1 - border,) * 2)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def switch(self):
        """
        切换黑白
        :return: 新的黑白状态
        """
        if self.turn == WhiteChess:
            self.turn = BlackChess
        else:
            self.turn = WhiteChess
        self.flush_image()

    def flush_image(self):
        """
        刷新图像
        :return: None
        """
        self.image = self.images[[BlackChess, WhiteChess].index(self.turn)]

    def flush_pos(self):
        """
        刷新坐标位置
        :return: None
        """
        # 一格的宽度
        grid = 50
        x, y = pygame.mouse.get_pos()
        x -= (x - grid // 2) % grid
        y -= (y - grid // 2) % grid
        self.rect.topleft = x, y

    def flush(self):
        """
        一次性执行所有刷新操作
        :return: None
        """
        self.flush_image()
        self.flush_pos()

class Chess(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50)).convert_alpha()
        # 本来是黑色背景，现在换成透明背景
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(
            self.image, color, (25, 25), 20
        )
        self.rect = self.image.get_rect()

    @property
    def row(self):
        """
        获取这枚棋子的行数（0开始）
        :return: 行数
        """
        return self.rect.top // 50

    @property
    def col(self):
        """
        获取这枚棋子的列数（0开始）
        :return: 列数
        """
        return self.rect.left // 50

    def left(self, board):
        """
        获取当前棋子的左侧棋子
        :return: left chess of "self"
        """
        row, col = self.row, self.col
        try:
            return board[row][col - 1]
        except IndexError:
            pass

    def up(self, board):
        """
        获取当前棋子的上边棋子
        :return: up chess of "self"
        """
        row, col = self.row, self.col
        try:
            return board[row - 1][col]
        except IndexError:
            return None

    def right(self, board):
        """
        获取当前棋子的右边棋子
        :return: up chess of "self"
        """
        row, col = self.row, self.col
        try:
            return board[row][col + 1]
        except IndexError:
            return None

class WhiteChess(Chess):
    def __init__(self):
        Chess.__init__(self, (255, 255, 255))

class BlackChess(Chess):
    def __init__(self):
        Chess.__init__(self, (0, 0, 0))

class EmptyChess(Chess):
    def __init__(self):
        Chess.__init__(self, (0, 0, 0, 0))

    def __bool__(self):
        return False

class WinMessage(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("arial", 50)
        self.image = self.font.render("Win", False, color)
        self.rect = self.image.get_rect()
        self.rect.topright = 600, 10

class WhiteWin(WinMessage):
    def __init__(self):
        WinMessage.__init__(self, (255, 255, 255))

class BlackWin(WinMessage):
    def __init__(self):
        WinMessage.__init__(self, (0, 0, 0))

class Back(pygame.sprite.Sprite):
    def __init__(self):
        """
        悔棋按钮
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((200, 100))
        self.image.fill((192, 192, 192))
        font = pygame.font.SysFont("microsoftyaheiui", 50)
        surf = font.render("悔棋", False, (0, 0, 0))
        rect = surf.get_rect()
        rect.center = self.image.get_rect().center
        self.image.blit(surf, rect)
        self.rect = self.image.get_rect()
        self.rect.midright = 900, 350

class Bg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((700, 700)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        # 棋盘大小从14x14变成了13x13，然后每个格子的位置也移了
        # 主要这个700是懒得写676，不想算
        for x in range(25, 700, 50):
            pygame.draw.line(self.image, (0, 0, 0, 255), (x, 0), (x, 700), 1)
        for y in range(25, 700, 50):
            pygame.draw.line(self.image, (0, 0, 0, 255), (0, y), (700, y), 1)
        self.rect = self.image.get_rect()
