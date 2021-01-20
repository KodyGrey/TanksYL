# Тута хранятся все объекты


import pygame as pg
import os
import sys

pg.init()

size = width, height = 500, 500
screen = pg.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pg.sprite.Group()
tiles = pg.sprite.Group()
bullets = pg.sprite.Group()
tanks = pg.sprite.Group()
busters = pg.sprite.Group()
towers = pg.sprite.Group()

winner = 0


class Tile(pg.sprite.Sprite):
    destroyed = False

    def __init__(self, pos, iron=False):
        super().__init__(tiles, all_sprites)
        self.pos = pos
        self.iron = iron
        if iron:
            self.image = load_image('железный_блок.png')
        else:
            self.image = load_image('Кирпич.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        for bullet in bullets:
            collide = pg.sprite.collide_mask(self, bullet)
            if collide is not None:
                if bullet.ultimate and not self.iron:
                    bullet.update(crashed=True)
                    tiles.remove(self)
                    all_sprites.remove(self)
                    break


class Bullet(pg.sprite.Sprite):
    def __init__(self, coords, direction, ultimate=False):
        super().__init__(bullets, all_sprites)
        self.ultimate = ultimate
        self.coords = coords
        self.direction = direction
        if ultimate:
            self.image = load_image('стенобойная_пуля.png')
        else:
            self.image = load_image('Пуля.png')
        if direction == (1, 0):
            self.image = pg.transform.rotate(self.image, 90)
        elif direction == (0, -1):
            self.image = pg.transform.rotate(self.image, 180)
        elif direction == (-1, 0):
            self.image = pg.transform.rotate(self.image, 270)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def update(self, crashed=False):
        if crashed:
            bullets.remove(self)
            all_sprites.remove(self)
        else:
            self.rect.x += self.direction[0]
            self.rect.y += self.direction[1]


class Tank(pg.sprite.Sprite):
    def __init__(self, pos, team, direction):
        super().__init__(tanks, all_sprites)
        self.pos = pos
        self.direction = direction
        self.ultimate = 0
        self.fast = 0
        if team == 1:
            self.image = load_image('Танк1.png')
        elif team == 2:
            self.image = load_image('Танк2.png')
        self.team = team
        self.hp = 3
        if direction == (1, 0):
            self.image = pg.transform.rotate(self.image, 90)
        elif direction == (0, -1):
            self.image = pg.transform.rotate(self.image, 180)
        elif direction == (-1, 0):
            self.image = pg.transform.rotate(self.image, 270)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50

    def update(self, shoot=False, broken=False, direction=(0, 0)):
        if broken:
            self.hp -= 1
            if self.hp == 0:
                global winner
                winner = self.team % 2 + 1
        if shoot:
            coords = ((self.pos[0] + self.direction[0]) * 50,
                      (self.pos[1] + self.direction[1]) * 50)
            if direction == (0, 1):
                coords[0] += 23
                coords[1] += 44 if self.ultimate == 0 else 42
            elif direction == (1, 0):
                coords[1] += 23
            elif direction == (0, -1):
                coords[0] += 23
            elif direction == (-1, 0):
                coords[0] += 44 if self.ultimate == 0 else 42
                coords[1] += 23

            bullet = Bullet(coords, self.direction,
                            ultimate=True if self.ultimate > 0 else False)
        # some for's


class Buster(pg.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__(busters, all_sprites)
        self.pos = pos
        self.type = type
        if type == 1:
            self.image = load_image('бустер_скорости.png')
        elif type == 2:
            self.image = load_image('жизнь.png')
        elif type == 3:
            self.image = load_image('стенобойная_пуля.png')
            self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50
        self.mask = pg.mask.from_surface(self.image)

    def update(self, took=False):
        if took:
            busters.remove(self)
            all_sprites.remove(self)


class Tower(pg.sprite.Sprite):
    def __init__(self, pos, team):
        super().__init__(towers, all_sprites)
        self.pos = pos
        self.team = team
        self.image = load_image('Целая_крепость.png')
        self.hp = 3
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50

    def update(self):
        for bullet in bullets:
            collide = pg.sprite.collide_mask(self, bullet)
            if collide is not None:
                bullet.update(crashed=True)
                towers.remove(self)
                all_sprites.remove(self)
                break
