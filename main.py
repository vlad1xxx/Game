import math

import pygame
import sys
import os
from settings import WIDTH, HEIGHT, FONT_25

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('images/', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def show_level():
    class Fire(pygame.sprite.Sprite):
        def __init__(self, x, y, angle):
            super().__init__()
            self.angle = angle
            self.speed = 100 # Скорость выстрела
            self.image = pygame.Surface((5, 5))
            self.image.fill('red')
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            self.rect.x += (self.speed * math.cos(self.angle)) / 20
            self.rect.y += (self.speed * math.sin(self.angle)) / 20

    class Block(pygame.sprite.Sprite):
        def __init__(self, x, y, is_correct):
            super().__init__()
            self.image = pygame.Surface((50, 70))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.is_correct = is_correct
            if is_correct:
                self.image.fill('green')
            else:
                self.image.fill('red')

    class Platform:
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.color = 'blue'
            self.rect = pygame.Rect(x, y, w, h)

        def draw(self):
            self.rect.x = self.x
            pygame.draw.rect(screen, self.color, self.rect)

    running = True

    algebraic_conversions = {'2+23=4': [Block(100, 100, True),
                                        Block(200, 100, True),
                                        Block(300, 100, True),
                                        Block(400, 100, False),
                                        Block(500, 100, True),
                                        Block(600, 100, True)]}
    platforms = []
    platforms.append(Platform(0, HEIGHT // 3 * 2, WIDTH // 2, 50))
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    fires = pygame.sprite.Group()
    player = MainHero(all_sprites, 50, 100, 50, 50, 50, 50)

    for block in algebraic_conversions['2+23=4']:
        all_sprites.add(block)
        blocks.add(block)

    clicked_mouse = False

    while running:
        screen.fill('gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_n:
                    return True

        for block in platforms:
            block.draw()

        if not player.on_block:
            player.gravity += 1
            player.rect.y += player.gravity
            coll = False
            for block in platforms:
                if player.rect.colliderect(block.rect):
                    player.on_block = True
                    player.rect.y -= player.gravity
                    player.gravity = 0
        else:
            player.rect.y += 1
            coll = False
            for block in platforms:
                if player.rect.colliderect(block.rect):
                    coll = True
            if not coll:
                player.on_block = False
            else:
                player.rect.y -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.rect.left >= 0:
            player.rect.x -= player.speed
        if keys[pygame.K_d] and player.rect.right <= WIDTH:
            player.rect.x += player.speed
        if keys[pygame.K_SPACE] and player.on_block:
            player.rect.y -= 1
            player.gravity -= 15

        mouse_buttons = pygame.mouse.get_pressed()
        if not clicked_mouse and mouse_buttons[0]:
            clicked_mouse = True
            mouseX, mouseY = pygame.mouse.get_pos()
            player_pos = (player.rect.x + player.rect.width // 2, player.rect.y + player.rect.height // 2)
            angle = math.atan2(mouseY - player_pos[1], mouseX - player_pos[0])
            fire = Fire(player_pos[0], player_pos[1], angle)
            fires.add(fire)
            all_sprites.add(fire)
        if not mouse_buttons[0]:
            clicked_mouse = False

        # Обновление выстрелов
        for fire in fires:
            fire.update()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(blocks, fires, True, True)
        for key in hits.keys():
            if key.is_correct:
                return False

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class MainHero(pygame.sprite.Sprite):

    def __init__(self, group, x, y, name, hp, armor, coins):
        super().__init__(group)
        self.image = load_image("player2.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.hp = hp
        self.armor = armor
        self.coins = coins
        self.speed = 8
        self.gravity = 0
        self.vel = 5
        self.jump = False
        self.jump_count = 0
        self.is_jumping = False
        self.on_block = True


class NPC:
    def __init__(self, x, y, name, dialogue):
        self.x = x
        self.y = y
        self.name = name
        self.dialogue = dialogue
        # self.dialogue_shown = False  # Флаг для отслеживания показа диалога


def final_page():
    fon = pygame.transform.scale(load_image('final.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)


def main_page():
    def show_info_about_hero():
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, player.hp * 2, 20))
        pygame.draw.rect(screen, (0, 0, 0), (7, 7, 203, 23), 3)
        info = FONT_25.render(str(player.hp), True, (255, 0, 0))
        screen.blit(info, (215, 10))

    def is_near_npc(player, npc):
        distance = ((player.rect.x - npc.x) ** 2 + (player.rect.y - npc.y) ** 2) ** 0.5
        return distance < 75

    def render_use():
        text = FONT_25.render('Нажмите "E", чтобы взаимодействовать', True, (0, 0, 0))
        screen.blit(text, (WIDTH - 400, 5))

    def render_dialog(near_npc):
        dialog = FONT_25.render(near_npc.dialogue, True, (0, 0, 0))
        screen.blit(dialog, (near_npc.x + 50, near_npc.y - 50))

    all_sprites = pygame.sprite.Group()

    bg = load_image('sand.bmp')

    npcs = [
        NPC(200, 200, "Bob", "Hello, traveler!"),
        NPC(262, 706, "Alice", "Nice to meet you!"),
        NPC(1588, 166, "Charlie", "How can I help you?"),
        NPC(1084, 724, "Doctor", "Do you want to be treated?")
    ]

    player = MainHero(all_sprites, 500, 500, 'Deyan', 50, 2, 50)

    running = True
    near_npc = None

    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

        # Перемещение игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.rect.x > 0:
            player.rect.x -= player.speed
        if keys[pygame.K_d] and player.rect.x + 30 < WIDTH:
            player.rect.x += player.speed
        if keys[pygame.K_w] and player.rect.y > 0:
            player.rect.y -= player.speed
        if keys[pygame.K_s] and player.rect.y + 30 < HEIGHT:
            player.rect.y += player.speed

        # Cоздание NPC
        for npc in npcs:
            pygame.draw.circle(screen, (0, 0, 255), (npc.x, npc.y), 20)

        # Создание Игрока
        all_sprites.draw(screen)

        # Находит ближайшено NPC
        for npc in npcs:
            if is_near_npc(player, npc):
                near_npc = npc
                break
            else:
                near_npc = None

        if near_npc is not None and keys[pygame.K_e]:
            if near_npc.name == 'Doctor':
                if player.coins >= 50:
                    player.hp = 100
            elif near_npc.name == 'Bob':
                return 1
        elif near_npc is not None:  # Открывает диалог с NPC
            render_use()
            render_dialog(near_npc)
        show_info_about_hero()
        pygame.display.flip()
        clock.tick(FPS)


LVL = {None: terminate, 1: show_level}


def main():
    GAME_OVER = False
    start_screen()
    running = True
    while running:
        running_level = LVL[main_page()]
        if running_level is not None:
            GAME_OVER = running_level()
        if GAME_OVER:
            running = False

    final_page()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()