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

            cur_chess = chess
            for i in range(2, 6):
                cur_chess = cur_chess.left(board)
                if cur_chess not in history:
                    break
                if not isinstance(cur_chess, type(chess)):
                    break
            else:
                if isinstance(chess, BlackChess):
                    state = blackwin
                else:
                    state = whitewin

            cur_chess = chess
            for i in range(2, 6):
                cur_chess = cur_chess.up(board)
                if cur_chess not in history:
                    break
                if not isinstance(cur_chess, type(chess)):
                    break
            else:
                if isinstance(chess, BlackChess):
                    state = blackwin
                else:
                    state = whitewin

            cur_chess = chess
            for i in range(2, 6):
                cur_chess = cur_chess.up(board).left(board)
                if cur_chess not in history:
                    break
                if not isinstance(cur_chess, type(chess)):
                    break
            else:
                if isinstance(chess, BlackChess):
                    state = blackwin
                else:
                    state = whitewin

            cur_chess = chess
            for i in range(2, 6):
                cur_chess = cur_chess.up(board).right(board)
                if cur_chess not in history:
                    break
                if not isinstance(cur_chess, type(chess)):
                    break
            else:
                if isinstance(chess, BlackChess):
                    state = blackwin
                else:
                    state = whitewin

# 初始化pygame
pygame.init()
# 创建窗口
size = width, height = (1000, 700)
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
back = Back()
bg = Bg()

chess_down = pygame.mixer.Sound('Down.wav')

pygame.display.set_caption("五子棋")

# MainLoop
clock = pygame.time.Clock()
state = None
running = True
while running:
    clock.tick(30)
    screen.fill((192, 128, 0))
    screen.blit(bg.image, bg.rect)
    if state is None:
        # 在屏幕内部
        if pygame.mouse.get_focused() != 0:
            pos = pygame.mouse.get_pos()
            if 25 <= pos[0] < 675 and 25 <= pos[1] < 675:
                screen.blit(pickbox.image, pickbox.rect)
        screen.blit(back.image, back.rect)
    if state is not None:
        screen.blit(state.image, state.rect)
    for row in board:
        for chess in row:
            if chess in history:
                screen.blit(chess.image, chess.rect)
    pickbox.flush()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back.rect.collidepoint(event.pos):
                history.pop()
                pickbox.switch()
            elif state is None and (25 <= event.pos[0] < 675 and
                                    25 <= event.pos[1] < 675):
                # x是left，y是top
                x, y = pickbox.rect.topleft
                row1 = x // 50
                col1 = y // 50
                if board[col1][row1] not in history:
                    board[col1][row1] = pickbox.turn()
                    board[col1][row1].rect.topleft = x, y
                    history.append(board[col1][row1])
                    pickbox.switch()
                    chess_down.play()
    is_five()
    pygame.display.flip()
pygame.quit()
