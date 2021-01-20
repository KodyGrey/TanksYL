# Тута нужно добавлять саму отрисовку


import pygame as pg
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


selected_map, running, started = open('levels/level1.txt'), True, 0
size = int(selected_map.readline())
screen = pg.display.set_mode((850, 850))
screen.fill((0, 255, 0))
fon = load_image('Заставка.png')
screen.blit(fon, (0, 0))
pg.display.flip()
read_map(selected_map, size)
while running:
    if started:
        if started == 1:
            started = 2
            road = load_image('дорога.png')
            for i in range(size):
                for j in range(size):
                    screen.blit(road, (i * 50, j * 50))
        all_sprites.draw(screen)
        pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # Горячие клавиши
        if event.type == pg.KEYUP and event.key == pg.K_SPACE:
            started = 1
