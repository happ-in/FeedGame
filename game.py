import pygame
import sys
import random

from pygame.locals import *

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT / GRID_SIZE

WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
ORANGE = (250, 150, 0)
GRAY = (100, 100, 100)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FPS = 10


class Python(object):
    def __init__(self):
        self.create()
        self.color = GREEN

    def create(self):
        self.length = 2
        self.positions = [((WINDOW_WIDTH/2), (WINDOW_HEIGHT/2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def control(self, xy):
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy

    def move(self):
        cur = self.positions[0]
        x,y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WINDOW_WIDTH), (cur[1] + (y * GRID_SIZE)) % WINDOW_HEIGHT)

        #  자신의 몸에 충돌 했을 경우, 새롭게 시작
        if new in self.positions[2:]:
            self.create()
        else:
            # 전체를 움직이지 않고 맨 앞에 insert, 마지막에 pop을 해줘서 움직인 것처럼 보이게 함
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def eat(self):
        self.length += 1

    def draw(self, surface):
        for p in self.positions:
            # 표면 객체를 그리는 부분
            draw_object(surface, self.color, p)


class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.create()

    def create(self):
        # 먹이를 random하게 나오게 함
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        draw_object(surface, self.color, self.position)


# Functions
def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, color, r)


# 머리가 음식을 먹을 때의 동작
def check_eat(python, feed):
    if python.positions[0] == feed.position:
        python.eat()
        feed.create()


# 뱀의 길이의 스피드를 나타내 줌
def show_info(length, speed, surface):
    font = pygame.font.Font(None, 34)
    text = font.render("Length: " + str(length) + "     Speed: " + str(round(speed, 2)), 1, GRAY)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text, pos)


if __name__ == '__main__':
    python = Python()
    feed = Feed()

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Python Game')
    surface = pygame.Surface(window.get_size())
    surface = surface.convert()
    surface.fill(WHITE)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 40)
    window.blit(surface, (0, 0))

while True:
    # pygame.event.get()은 키보드나 마우스의 행동을 가져옴
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                python.control(UP)
            elif event.key == K_DOWN:
                python.control(DOWN)
            elif event.key == K_LEFT:
                python.control(LEFT)
            elif event.key == K_RIGHT:
                python.control(RIGHT)

    surface.fill(WHITE)
    python.move()
    check_eat(python, feed)
    speed = (FPS + python.length) / 2
    show_info(python.length, speed, surface)
    python.draw(surface)
    feed.draw(surface)
    window.blit(surface, (0, 0))

    # 변환되는 상태를 빠르게 지우고 그리기를 반복해줌
    pygame.display.flip()
    pygame.display.update()
    clock.tick(speed)
