import pygame
import random


# 初始化pygame
pygame.init()

# 设置游戏窗口大小
WIDTH, HEIGHT = 640, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('贪吃蛇')

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 蛇的初始位置和大小
snake_block = 10
snake_speed = 15

# 字体设置
font_style = pygame.font.SysFont(None, 50)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [WIDTH / 2 - 100, HEIGHT / 2])


def game_loop():
    game_over = False
    game_close = False

    # 蛇头的初始位置
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    # 蛇头移动的初始方向
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # 食物的初始位置
    foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            win.fill(BLACK)
            message("you lost！ press Q - exit， press C - restart", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # 检查蛇是否撞到边界
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        win.fill(BLACK)
        pygame.draw.rect(win, RED, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 检查蛇是否撞到自己
        for x in snake_List[: -1]:
            if x == snake_Head:
                game_close = True

        for segment in snake_List:
            pygame.draw.rect(win, WHITE, [segment[0], segment[1], snake_block, snake_block])

        pygame.display.update()

        # 检查蛇是否吃到食物
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock = pygame.time.Clock()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_loop()
