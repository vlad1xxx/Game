import pygame
import math
import os
import sys
from settings import WIDTH, HEIGHT, IMAGES

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image, dial, upg):
        super().__init__(group)
        self.image = load_image(image)
        self.dialogue = dial
        self.upg_lvl = upg
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)


class Door:
    def __init__(self, x, y, name, dialogue, status):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - 80, self.y - 160, 160, 240)
        self.name = name
        self.dialogue = dialogue
        if status:
            self.color = 'green'
        else:
            self.color = 'white'


class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.angle = angle
        self.speed = 10  # Скорость выстрела
        self.anim = [load_image('fire_animation/fire1.png'),
                     load_image('fire_animation/fire2.png'),
                     load_image('fire_animation/fire3.png'),
                     load_image('fire_animation/fire4.png')]
        self.index_anim = 0
        self.image = self.anim[self.index_anim]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += (self.speed * math.cos(self.angle)) / 2
        self.rect.y += (self.speed * math.sin(self.angle)) / 2

    def update_animation(self):
        self.image = self.anim[self.index_anim]
        self.index_anim = (self.index_anim + 1) % len(self.anim)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, is_correct, num_group, value):
        super().__init__()
        if value in IMAGES:
            self.image = load_image(IMAGES[value])
        else:
            self.image = pygame.Surface((70, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_correct = is_correct
        self.num_group = num_group
        self.value = value


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image, isbad=False):
        super().__init__()
        self.isbad = isbad
        if not image:
            self.image = pygame.Surface((160, 160))
            self.image.fill('blue')
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Timer:
    def __init__(self, seconds, x, y):
        self.max_seconds = seconds
        self.x = x
        self.y = y
        self.timer = seconds
        self.counter_fps = 0

    def update(self):
        self.timer -= 0.01666667
        pygame.draw.rect(screen, 'grey', (self.x, self.y, 60 * self.max_seconds, 30))
        if self.timer < 2:
            pygame.draw.rect(screen, 'red', (self.x, self.y, 60 * self.timer, 30))
        else:
            pygame.draw.rect(screen, 'yellow', (self.x, self.y, 60 * self.timer, 30))
        if self.timer <= 0:
            return False
        return True


def load_image(name):
    fullname = os.path.join('images/', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
