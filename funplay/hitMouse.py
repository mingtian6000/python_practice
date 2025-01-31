import pygame
import random


pygame.init()

pygame.mixer.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("打地鼠游戏")


try:
    grassland_image = pygame.image.load('grassland.jpg')
    grassland_image = pygame.transform.scale(grassland_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    print("无法加载草地背景图片，请检查图片路径和文件名。")
    pygame.quit()
    quit()
try:
    mole_image = pygame.image.load('mole.png')
    mole_image = pygame.transform.scale(mole_image, (100, 100))  # 调整图片大小
except pygame.error:
    print("无法加载老鼠图片，请检查图片路径和文件名。")
    pygame.quit()
    quit()

try:
    hit_sound = pygame.mixer.Sound('hit.wav')  # 击中音效
    pop_sound = pygame.mixer.Sound('pop.wav')  # 地鼠出现音效
except pygame.error:
    print("无法加载音效，请检查音效文件路径和文件名。")

holes = [(100, 100), (300, 100), (500, 100),
         (100, 300), (300, 300), (500, 300)]

# 随机选择一个地鼠位置
current_mole_pos = random.choice(holes)
pop_sound.play()  # 游戏开始时播放地鼠出现音效


score = 0
font = pygame.font.Font(None, 36)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            mole_rect = mole_image.get_rect(topleft=current_mole_pos)
            if mole_rect.collidepoint(mouse_x, mouse_y):
                score += 1
                hit_sound.play()  # 击中时播放音效
                current_mole_pos = random.choice(holes)
                pop_sound.play()  # 地鼠换位置后播放出现音效

    screen.fill((255, 255, 255))

    screen.blit(mole_image, current_mole_pos)

    score_text = font.render(f"分数: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(30)


pygame.mixer.quit()
pygame.quit()