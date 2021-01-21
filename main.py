# Тута нужно добавлять саму отрисовку


import pygame as pg
import random as rn
from objects import *


def read_map(file, N):
    for i in range(N):
        objects = list(file.readline().split())
        for j in range(len(objects)):
            # Обычные объекты на поле
            if objects[j] == 'b':
                Tile((N - j - 1, N - i - 1), iron=False)
            if objects[j] == 'i':
                Tile((N - j - 1, N - i - 1), iron=True)
            # Связанные объекты на поле, танки и базы
            if objects[j] == 'C1':
                Tower((N - j - 1, N - i - 1), 1)
            if objects[j] == 'C2':
                Tower((N - j - 1, N - i - 1), 2)
            if objects[j] == 'T1':
                Tank((N - j - 1, N - i - 1), 1, (0, 1))
            if objects[j] == 'T2':
                Tank((N - j - 1, N - i - 1), 2, (0, 1))
    return


def spawn_buster(filename, N):
    flag = True
    while flag:
        file = open(filename)
        ri = rn.randint(0, N - 1)
        for i in range(N):
            objects = list(file.readline().split())
            if i == ri:
                rj = rn.randint(0, len(objects) - 1)
                if objects[rj] == 'r':
                    type = rn.randint(1, 3)
                    Buster((ri, rj), type)
                    flag = False
                    break
                else:
                    break
        file.close()


selected_map, running, started = open('levels/level1.txt'), True, 0
size = int(selected_map.readline())
screen = pg.display.set_mode((850, 850))
screen.fill((0, 255, 0))
fon = load_image('Заставка.png')
screen.blit(fon, (0, 0))
pg.display.flip()
read_map(selected_map, size)
selected_map.close()

fps = 60
clock = pg.time.Clock()
pg.init()
counter = 0

SPAWNBUSTER = pg.USEREVENT + 1

while running:
    if started:
        if started == 1:
            pg.time.set_timer(SPAWNBUSTER, 1 * 10 * 1000)
        started = 2
        road = load_image('дорога.png')
        for i in range(size):
            for j in range(size):
                screen.blit(road, (i * 50, j * 50))
        all_sprites.draw(screen)

    pressed = pg.key.get_pressed()
    if pressed[pg.K_w]:
        tanks.update(team=1, direction=(0, 1))
    elif pressed[pg.K_d]:
        tanks.update(team=1, direction=(1, 0))
    elif pressed[pg.K_s]:
        tanks.update(team=1, direction=(0, -1))
    elif pressed[pg.K_a]:
        tanks.update(team=1, direction=(-1, 0))

    if pressed[pg.K_UP]:
        tanks.update(team=2, direction=(0, 1))
    elif pressed[pg.K_RIGHT]:
        tanks.update(team=2, direction=(1, 0))
    elif pressed[pg.K_DOWN]:
        tanks.update(team=2, direction=(0, -1))
    elif pressed[pg.K_LEFT]:
        tanks.update(team=2, direction=(-1, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # Горячие клавиши
        if event.type == pg.KEYUP and event.key == pg.K_SPACE:
            started = 1
        if event.type == SPAWNBUSTER:
            spawn_buster('levels/level1.txt', size)
        if event.type == pg.KEYDOWN and event.key == pg.K_f:
            tanks.update(team=1, shoot=True)
        if event.type == pg.KEYDOWN and event.key == pg.K_m:
            tanks.update(team=2, shoot=True)

    all_sprites.update()
    pg.display.flip()
    clock.tick(fps)
