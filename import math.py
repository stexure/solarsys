import math
from random import *
import pygame


class Ball1:
    def __init__(self, screen, obj):
        self.screen = screen
        self.x = obj.x
        self.y = obj.y
        self.r = 10
        self.vx = 10
        self.vy = 10
        self.color = (0,0,0)
        self.live = 1

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x >= 1200:
            self.live -=1
        if self.x <= 0:
            self.live -= 1
        if self.y >= 900:
            self.live -=1
        if self.y <= 0:
            self.live -=1


    def draw(self):
        surf = pygame.image.load('images/mk1.png').convert_alpha()
        surf.set_colorkey((0, 0, 0))
        rect = surf.get_rect(center=(self.x, self.y))
        self.screen.blit(surf, rect)

    def hittest(self, obj):
        return ((obj.x+50 - self.x-10) ** 2 + (obj.y+30 - self.y-10) ** 2) ** 0.5 <= obj.r + self.r


class Ball2(Ball1):

    def draw(self):
        surf = pygame.image.load('images/mk2.png').convert_alpha()
        surf.set_colorkey((0, 0, 0))
        rect = surf.get_rect(center=(self.x, self.y))
        self.screen.blit(surf, rect)




class GunH:
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.r = 80
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.live = 1
        self.image = pygame.image.load('images/Harkonnen_Devastator.png').convert_alpha()

    def new_devos(self,x,y):
        x = self.x = x
        y = self.y = y
        r = self.r = 80
        color = self.color = RED
        self.live = 1


    def fire2_start(self, event):
        self.f2_on = 1


    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        new_ball = Ball1(self.screen, self)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10


    def targetting(self, event):
        if event:
            self.an = math.degrees(math.atan((event.pos[1] - self.y - 0.00001) / (event.pos[0] - self.x - 0.00001)))


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1

    def move(self, event, player_speed, plen):
        if keys[pygame.K_a] and self.x > 30 and plen == False:
            self.x -= player_speed
        if keys[pygame.K_d] and self.x < 1000 and plen == False:
            self.x += player_speed
        if keys[pygame.K_w] and self.y > 20 and plen == False:
            self.y -= player_speed
        if keys[pygame.K_s] and self.y < 800 and plen == False:
            self.y += player_speed
        '''while(keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d]):
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('music/engine.mp3'))'''

    def draw(self):
        devos = pygame.image.load('images/Harkonnen_Devastator.png').convert_alpha()
        rect = devos.get_rect(center=(0, 0))
        rot = pygame.transform.rotate(devos, -self.an)
        rot_rect = rot.get_rect(center=(self.x + 40, self.y - 30))
        '''screen.blit(self.image, (self.x, self.y))'''
        self.screen.blit(rot, rot_rect)



class GunS:
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.r = 80
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.live = 1
        self.image = pygame.image.load('images/sonic.png').convert_alpha()

    def new_sonic(self, x, y):
        self.x = x
        self.y = y
        r = self.r = 80
        color = self.color = RED
        self.live = 1


    def fire2_start(self, event):
        self.f2_on = 1


    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        new_ball = Ball2(self.screen, self)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10


    def targetting(self, event):
        if event:
            if event.pos[0] != 20:
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
            elif event.pos[1] != 450:
                self.an = math.atan((event.pos[0] - 20) / (event.pos[1] - 450))
            else:
                self.an = 0
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def move(self, event, enemy_speed, plen):
        if keys[pygame.K_a] and self.x > -20 and plen == True:
            self.x -= enemy_speed
        if keys[pygame.K_d] and self.x < 1000 and plen == True:
            self.x += enemy_speed
        if keys[pygame.K_w] and self.y > -20 and plen == True:
            self.y -= enemy_speed
        if keys[pygame.K_s] and self.y < 770 and plen == True:
            self.y += enemy_speed


    def draw(self):
        sonic = pygame.image.load('images/sonic.png').convert_alpha()
        rect = sonic.get_rect(center=(0, 0))
        rot = pygame.transform.rotate(sonic, -self.an)
        rot_rect = rot.get_rect(center=(self.x + 40, self.y - 30))
        '''screen.blit(self.image, (self.x, self.y))'''
        self.screen.blit(rot, rot_rect)








class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.r = 50
        self.live = 1
        self.new_target()
        self.image = pygame.image.load('images/orni.png').convert_alpha()

    def new_target(self):
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = 50
        vx = self.vx = randint(-10, 10)
        vy = self.vy = randint(-10, 10)
        color = self.color = RED
        self.live = 1

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x <= 20 + self.r:
            self.x = 20 + self.r
            self.vx = -self.vx
        if self.x >= 1100 - self.r:
            self.x = 1100 - self.r
            self.vx = -self.vx
        if self.y <= -10 + self.r:
            self.y = -10 + self.r
            self.vy = -self.vy
        if self.y >= 840 - self.r:
            self.y = 840 - self.r
            self.vy = -self.vy


    def draw(self):
        screen.blit(self.image, (self.x, self.y))



class Bomb(Ball1):
    def __init__(self, screen, obj):
        self.screen = screen
        self.live = 1
        self.x = obj.x
        self.y = obj.y
        self.vx = 0
        self.vy = 5
        self.r = 40

    def draw(self):
        surf = pygame.image.load('images/bomb.png').convert_alpha()
        surf = pygame.transform.scale(surf, (100, 100))
        surf.set_colorkey((0, 0, 0))
        rect = surf.get_rect(center=(self.x, self.y))
        self.screen.blit(surf, rect)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x >= 1200:
            self.live -=1
        if self.x <= 0:
            self.live -= 1
        if self.y >= 900:
            self.live -=1
        if self.y <= 0:
            self.live -=1

    def new_bomb(self,obj):
        x = self.x = obj.x
        y = self.y = obj.y
        r = self.r = 40
        vy = self.vy = 5
        color = self.color = RED
        self.live = 1


clock = pygame.time.Clock()

pygame.init()
pygame.mixer.music.load('music/bg.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

screen = pygame.display.set_mode((1200,900))
pygame.display.set_caption("Dune")

bullet = 0
balls = []
step = 0

FPS = 30

'''Background'''
bg = pygame.image.load('images/bg.jpg').convert()

'''Переключение'''
plen = False

'''Player'''
player_x = 220
player_y = 500
player_speed = 7

'''Enemy'''
enemy_x = 900
enemy_y = 500
enemy_speed = 7


'''Targets'''
RED = 0xFF0000
GREY = 0x7D7D7D
Devos = GunH(screen, player_x, player_y)
Sonic = GunS(screen, enemy_x, enemy_y)
target1 = Target(screen)
target2 = Target(screen)
bomb1 = Bomb(screen, target1)




running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    '''Вывод изображений'''
    screen.blit(bg, (0,0))
    Devos.draw()
    Sonic.draw()
    target1.draw()
    target2.draw()
    bomb1.draw()


    for b in balls:
        b.draw()



    '''Движение'''
    keys = pygame.key.get_pressed()
    '''Переключение: д - девостатор, с - соник'''
    if keys[pygame.K_c] and plen != True:
        plen = True
    if keys[pygame.K_l] and plen != False:
        plen = False

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if step % 2 == 0:
                Devos.fire2_start(event)
            else:
                Sonic.fire2_start(event)
            step += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if step % 2 == 0:
                Devos.fire2_end(event)
            else:
                Sonic.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            if step % 2 == 0:
                Devos.targetting(event)
            else:
                Sonic.targetting(event)


    '''Movement'''
    target1.move()
    target2.move()
    bomb1.move()
    Devos.move(keys,player_speed, plen)
    Sonic.move(keys, enemy_speed, plen)

    for b in balls:
        b.move()
        if b.hittest(target1):
            target1.live -= 1
        if target1.live == 0:
            target1.new_target()
        if b.hittest(target2):
            target2.live -= 1
        if target2.live == 0:
            target2.new_target()

    if bomb1.hittest(Devos):
        Devos.live -= 1
        bomb1.live -= 1
    if bomb1.hittest(Sonic):
        Sonic.live -= 1
        bomb1.live -= 1
    if bomb1.live == 0:
        bomb1.new_bomb(target1)
    if Devos.live == 0:
        Devos.new_devos(player_x,player_y)
    if Sonic.live == 0:
        Sonic.new_sonic(enemy_x,enemy_y)

    pygame.display.update()