import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE]

WIDTH = 300
HEIGHT = 600
BLOCK_SIZE = 30
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("俄罗斯方块")
clock = pygame.time.Clock()

# 定义按钮类
class Button:
    def __init__(self, x, y, width, height, text, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class Tetris:
    def __init__(self, rate):
        self.rate = rate
        self.grid = [[0] * 10 for _ in range(20)]
        self.current_shape = random.choice(SHAPES)
        self.current_color = random.choice(COLORS)
        self.current_x = 5 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.score = 0
        self.game_over = False
        self.paused = False
        self.fall_time = 0
        self.fall_speed = 0.6 / rate
        
    def reset(self):
        self.grid = [[0] * 10 for _ in range(20)]
        self.current_shape = random.choice(SHAPES)
        self.current_color = random.choice(COLORS)
        self.current_x = 5 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.score = 0
        self.game_over = False
        self.paused = False
        self.fall_time = 0
        self.fall_speed = 0.6 / self.rate


    def draw_grid(self):
        for i in range(20):
            for j in range(10):
                if self.grid[i][j] != 0:
                    pygame.draw.rect(screen, COLORS[self.grid[i][j] - 1],
                                     (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for i in range(20):
            pygame.draw.line(screen, GRAY, (0, i * BLOCK_SIZE), (WIDTH, i * BLOCK_SIZE))
        for j in range(10):
            pygame.draw.line(screen, GRAY, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, HEIGHT))

    def draw_shape(self):
        for i in range(len(self.current_shape)):
            for j in range(len(self.current_shape[0])):
                if self.current_shape[i][j] == 1:
                    pygame.draw.rect(screen, self.current_color,
                                     ((self.current_x + j) * BLOCK_SIZE, (self.current_y + i) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def is_collision(self, shape, x, y):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    if (x + j < 0 or x + j >= 10 or y + i >= 20) or (
                            y + i >= 0 and self.grid[y + i][x + j] != 0):
                        return True
        return False

    def merge_shape(self):
        for i in range(len(self.current_shape)):
            for j in range(len(self.current_shape[0])):
                if self.current_shape[i][j] == 1:
                    self.grid[self.current_y + i][self.current_x + j] = COLORS.index(self.current_color) + 1

    def clear_lines(self):
        full_lines = []
        for i in range(20):
            if all(self.grid[i]):
                full_lines.append(i)
        for line in full_lines:
            del self.grid[line]
            self.grid = [[0] * 10] + self.grid
            self.score += 100

    def new_shape(self):
        self.current_shape = random.choice(SHAPES)
        self.current_color = random.choice(COLORS)
        self.current_x = 5 - len(self.current_shape[0]) // 2
        self.current_y = 0
        if self.is_collision(self.current_shape, self.current_x, self.current_y):
            self.game_over = True

    def rotate_shape(self):
        rotated_shape = list(map(list, zip(*self.current_shape[::-1])))
        if not self.is_collision(rotated_shape, self.current_x, self.current_y):
            self.current_shape = rotated_shape

    def move_left(self):
        if not self.is_collision(self.current_shape, self.current_x - 1, self.current_y):
            self.current_x -= 1

    def move_right(self):
        if not self.is_collision(self.current_shape, self.current_x + 1, self.current_y):
            self.current_x += 1

    def move_down(self):
        if not self.is_collision(self.current_shape, self.current_x, self.current_y + 1):
            self.current_y += 1
        else:
            self.merge_shape()
            self.clear_lines()
            self.new_shape()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.move_right()
                elif event.key == pygame.K_DOWN:
                    self.move_down()
                elif event.key == pygame.K_UP:
                    self.rotate_shape()

    def update(self, dt):
        if not self.paused and not self.game_over:
            self.fall_time += dt
            if self.fall_time >= self.fall_speed:
                self.move_down()
                self.fall_time = 0

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(text, (10, 10))

    def draw_game_over(self):
        if self.game_over:
            font = pygame.font.Font(None, 72)
            text = font.render("Game Over", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

    def pause(self):
        self.paused = not self.paused

# 选择速率
rate_buttons = [
    Button(50, 200, 80, 50, "Slow", GRAY, lambda: main(1)),
    Button(170, 200, 80, 50, "Fast", GRAY, lambda: main(3))
]

def main(rate):
    game = Tetris(rate)
    start_button = Button(50,  0, 80, 50, "Start", GRAY, game.reset)
    pause_button = Button(170,  0, 80, 50, "Pause", GRAY, game.pause)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            start_button.handle_event(event)
            pause_button.handle_event(event)

        game.handle_events(events)
        game.update(dt)

        screen.fill(BLACK)
        game.draw_grid()
        game.draw_shape()
        game.draw_score()
        game.draw_game_over()
        start_button.draw(screen)
        pause_button.draw(screen)

        pygame.display.flip()

    pygame.quit()

# 选择速率界面
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        for button in rate_buttons:
            button.handle_event(event)

    screen.fill(BLACK)
    for button in rate_buttons:
        button.draw(screen)
    pygame.display.flip()