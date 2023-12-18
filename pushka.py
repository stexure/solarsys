import math
from math import sqrt
from random import choice, randint as rnd

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
waiting_for_sleep_to_over = False


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.gravity = 1
        self.birth = pygame.time.get_ticks()

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        if self.x >= WIDTH - self.r or self.x <= self.r:
            if self.x > WIDTH - self.r:
                self.x = WIDTH - self.r
            if self.x < self.r:
                self.x = self.r
            self.vx *= -0.5
            self.vy *= 0.9
        if self.y >= HEIGHT - self.r:
            if self.y > HEIGHT - self.r:
                self.y = HEIGHT - self.r
            self.vy *= -0.5
            self.vx *= 0.5
            if abs(self.vy) <= 1.6:
                self.vy = 0
                self.gravity = 0

    def expired(self):
        if pygame.time.get_ticks() - self.birth > 2500:
            return True
        return False

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        return sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) <= obj.r + self.r


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y = 450
        self.speed = 5  # Adjust the speed as needed

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        if event:
            d = event.pos[0] - 20
            self.an = math.atan((event.pos[1] - 450) / d if d != 0 else 1)

        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def move_left(self):
        self.x -= self.speed
        self.draw()

    def move_right(self):
        self.x += self.speed
        self.draw()

    def move_up(self):
        self.y -= self.speed
        self.draw()

    def move_down(self):
        self.y += self.speed
        self.draw()

    def draw(self):
        pygame.draw.line(self.screen, self.color, [self.x, self.y],
                         [self.x + self.f2_power * math.cos(self.an),
                          self.y + self.f2_power * math.sin(self.an)], 10)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(10, 50)
        self.color = RED
        self.velocity = rnd(-10, 10)

    def new_target(self):
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(10, 50)

    def hit(self, points=1):
        self.points += points

    def draw(self):
        if waiting_for_sleep_to_over is not True:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.y += self.velocity
        if self.y >= HEIGHT - self.r or self.y <= self.r:
            self.velocity *= -1


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
finished = False
start_sleep = None

while not finished:
    screen.fill(WHITE)
    if start_sleep != None and pygame.time.get_ticks() - start_sleep < 1000 and bullet != 0:
        text = pygame.font.Font(None, 50).render('Вы попали в цель за ' + str(bullet) + " раз",
                                                 True, (0, 0, 0))
        screen.blit(text, (20, 500))
    elif start_sleep != None and pygame.time.get_ticks() - start_sleep >= 1000:
        waiting_for_sleep_to_over = False
        start_sleep = None
        bullet = 0
        target1.live = 1
        target2.live = 1
    gun.draw()
    if target1.live:
        target1.draw()
        target1.move()
    if target2.live:
        target2.draw()
        target2.move()
    text = pygame.font.Font(None, 50).render('Счёт:' + str(target1.points + target2.points),
                                              True, (0, 0, 0))
    screen.blit(text, (0, 0))

    expired = []
    for i in range(len(balls)):
        if balls[i].expired():
            expired.append(i)
    for i in expired:
        del balls[i]

    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and waiting_for_sleep_to_over is not True:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and waiting_for_sleep_to_over is not True and gun.f2_on != 0:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION and waiting_for_sleep_to_over is not True:
            gun.targetting(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gun.move_left()
            elif event.key == pygame.K_RIGHT:
                gun.move_right()
            elif event.key == pygame.K_UP:
                gun.move_up()
            elif event.key == pygame.K_DOWN:
                gun.move_down()

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
        if target1.live == 0 and target2.live == 0:
            start_sleep = pygame.time.get_ticks()
            waiting_for_sleep_to_over = True
            gun.f2_on = 0

    gun.power_up()

pygame.quit()