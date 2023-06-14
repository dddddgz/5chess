from sprites import *
import pygame

def is_five():
    """
    判断是否连成五个
    :return: sprites.WhiteChess or sprites.BlackChess
    """
    global state
    for row in board:
        for chess in row:
            # i：行索引
            # j：列索引
            if type(chess) == EmptyChess:
                continue
            chess2 = chess.left(board)
            if isinstance(chess2, type(chess)):
                chess3 = chess2.left(board)
                if isinstance(chess3, type(chess)):
                    chess4 = chess3.left(board)
                    if isinstance(chess4, type(chess)):
                        chess5 = chess4.left(board)
                        if isinstance(chess5, type(chess)):
                            if type(chess) == BlackChess:
                                state = blackwin
                            else:
                                state = whitewin
            chess2 = chess.up(board)
            if isinstance(chess2, type(chess)):
                chess3 = chess2.up(board)
                if isinstance(chess3, type(chess)):
                    chess4 = chess3.up(board)
                    if isinstance(chess4, type(chess)):
                        chess5 = chess4.up(board)
                        if isinstance(chess5, type(chess)):
                            if type(chess) == BlackChess:
                                state = blackwin
                            else:
                                state = whitewin
            chess2 = chess.up(board).left(board)
            if isinstance(chess2, type(chess)):
                chess3 = chess2.up(board).left(board)
                if isinstance(chess3, type(chess)):
                    chess4 = chess3.up(board).left(board)
                    if isinstance(chess4, type(chess)):
                        chess5 = chess4.up(board).left(board)
                        if isinstance(chess5, type(chess)):
                            if type(chess) == BlackChess:
                                state = blackwin
                            else:
                                state = whitewin
            chess2 = chess.up(board).right(board)
            if isinstance(chess2, type(chess)):
                chess3 = chess2.up(board).right(board)
                if isinstance(chess3, type(chess)):
                    chess4 = chess3.up(board).right(board)
                    if isinstance(chess4, type(chess)):
                        chess5 = chess4.up(board).right(board)
                        if isinstance(chess5, type(chess)):
                            if type(chess) == BlackChess:
                                state = blackwin
                            else:
                                state = whitewin

# 初始化pygame
pygame.init()
# 创建窗口
size = width, height = (700, 700)
screen = pygame.display.set_mode(size)

pickbox = PickBox()
board = [[EmptyChess() for j in range(14)] for i in range(14)]
for i, row in enumerate(board):
    for j, chess in enumerate(row):
        chess.rect.top = i * 50
        chess.rect.left = j * 50
whitewin = WhiteWin()
blackwin = BlackWin()
history = []

chess_down = pygame.mixer.Sound('Down.wav')

pygame.display.set_caption("五子棋")

# MainLoop
clock = pygame.time.Clock()
state = None
running = True
while running:
    clock.tick(30)
    screen.fill((192, 128, 0))
    if state is None:
        # 在屏幕内部
        if pygame.mouse.get_focused() != 0:
            if pygame.mouse.get_pos()[0] < 700:
                screen.blit(pickbox.image, pickbox.rect)
    if state is not None:
        screen.blit(state.image, state.rect)
    for row in board:
        for chess in row:
            screen.blit(chess.image, chess.rect)
    pickbox.flush()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state is None and event.pos[0] < 700:
                # x是left，y是top
                x, y = pickbox.rect.topleft
                row1 = x // 50
                col1 = y // 50
                if not board[col1][row1]:
                    board[col1][row1] = pickbox.turn()
                    board[col1][row1].rect.topleft = x, y
                    history.append(board[col1][row1])
                    pickbox.switch()
                    chess_down.play()
    is_five()
    pygame.display.flip()
pygame.quit()
