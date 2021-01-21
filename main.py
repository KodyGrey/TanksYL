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
            started = 2
            road = load_image('дорога.png')
            for i in range(size):
                for j in range(size):
                    screen.blit(road, (i * 50, j * 50))
            pg.time.set_timer(SPAWNBUSTER, 2 * 60 * 1000)
        all_sprites.draw(screen)
        pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # Горячие клавиши
        if event.type == pg.KEYUP and event.key == pg.K_SPACE:
            started = 1
        if event.type == SPAWNBUSTER:
            spawn_buster('levels/level1.txt', size)
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_w, pg.K_UP]:
                team = 1 if event.key == pg.K_w else 2
                tanks.update(team=team, direction=(0, 1))

    all_sprites.draw(screen)
    clock.tick(fps)
