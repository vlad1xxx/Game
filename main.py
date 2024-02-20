import math
import pytmx
import pygame
import sys
import os
import random
from settings import WIDTH, HEIGHT, FONT_25

WIDTH = 1920
HEIGHT = 1040
IMAGES = {'0': 'number_0.png',
          '1': 'number_1.png',
          '2': 'number_2.png',
          '3': 'number_3.png',
          '4': 'number_4.png',
          '5': 'number_5.png',
          '6': 'number_6.png',
          '7': 'number_7.png',
          '8': 'number_8.png',
          '9': 'number_9.png',
          '+': 'symbol_plus.png',
          '=': 'symbol_equal.png',
          '-': 'symbol_minus.png',
          '*': 'symbol_mult.png'}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60


class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.angle = angle
        self.speed = 10  # Скорость выстрела
        self.image = pygame.Surface((5, 5))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += (self.speed * math.cos(self.angle)) / 2
        self.rect.y += (self.speed * math.sin(self.angle)) / 2


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
        # if is_correct:
        #     self.image.fill('green')
        # else:
        #     self.image.fill('red')


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


def generate_random_algebraic_conversions_vertical(count_correct_num, count_incorrect_num, num_group, x, y, symbols):
    conversions = []
    random_num = random.choices(['1', '2', '3', '4', '5', '6', '7', '8', '9'], k=count_correct_num)
    for num in random_num:
        conversions.append(Block(x, 0, True, num_group, num))
    conversions.insert(random.randrange(1, len(conversions)), Block(0, y, True, num_group, random.choice(symbols)))
    line = ''
    for elem in conversions:
        line += elem.value
    result = eval(line)
    conversions.append(Block(x, 0, True, num_group, '='))
    for num in str(result):
        conversions.append(Block(x, 0, True, num_group, num))

    while count_incorrect_num != 0:
        incorrect_num = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        if incorrect_num not in conversions:
            conversions.insert(random.randrange(count_correct_num + 1), Block(x, 0, False, 1, incorrect_num))
            count_incorrect_num -= 1

    for i in range(len(conversions)):
        conversions[i].rect.y = y + i * 100
    return conversions


def generate_random_algebraic_conversions_horizontal(count_correct_num, count_incorrect_num, num_group, x, y, symbols):
    conversions = []
    random_num = random.choices(['1', '2', '3', '4', '5', '6', '7', '8', '9'], k=count_correct_num)
    for num in random_num:
        conversions.append(Block(0, y, True, num_group, num))
    conversions.insert(random.randrange(1, len(conversions)), Block(0, y, True, num_group, random.choice(symbols)))
    line = ''
    for elem in conversions:
        line += elem.value
    result = eval(line)
    conversions.append(Block(0, y, True, num_group, '='))
    for num in str(result):
        conversions.append(Block(0, y, True, num_group, num))

    while count_incorrect_num != 0:
        incorrect_num = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        if incorrect_num not in conversions:
            conversions.insert(random.randrange(count_correct_num + 1), Block(0, y, False, 1, incorrect_num))
            count_incorrect_num -= 1

    for i in range(len(conversions)):
        conversions[i].rect.x = x + i * 70
    return conversions


def all_blocks_correct(blocks_group):
    for block in blocks_group:
        if not block.is_correct:
            return False
    return True


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
    running = True

    timer = 5
    counter_fps = 0

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    units_group = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    fires = pygame.sprite.Group()

    for elem in generate_random_algebraic_conversions_horizontal(2, 1, 1, 720, 360, ['+', '-', '*']):
        blocks.add(elem)

    def generate_level(level):
        player_cords = None
        for y in range(level.height):
            s = ''
            for x in range(level.width):

                image = lvl_map.get_tile_image(x, y, 0)
                lvl_id = lvl_map.get_tile_gid(x, y, 0)
                s += str(lvl_id) + ' '
                if lvl_id in bad_platform_ids:
                    all_sprites.add(Platform(x * tile_size, y * tile_size, image, True))
                    platforms.add(Platform(x * tile_size, y * tile_size, image, True))

                elif lvl_map.get_tile_gid(x, y, 0) in platform_ids:
                    all_sprites.add(Platform(x * tile_size, y * tile_size, image))
                    platforms.add(Platform(x * tile_size, y * tile_size, image))
                else:
                    all_sprites.add(Platform(x * tile_size, y * tile_size, image))
            print(s)

    #bad_platform_ids = [              1 lvl
    #    19, 20, 21, 22
    #]
    #platform_ids = [
    #    2, 3, 4, 8, 9, 10, 12, 13
    #]

    bad_platform_ids = [
        12
    ]
    platform_ids = [
        2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    ]

    lvl_map = pytmx.load_pygame('maps/map3.tmx')
    height = lvl_map.height
    width = lvl_map.width
    tile_size = lvl_map.tilewidth
    #player_cords = (920, 560) 1 lvl
    player_cords = (160, 160)
    player = MainHero(units_group, player_cords[0], player_cords[1], 50, 50, 50, 50)
    generate_level(lvl_map)
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

        counter_fps += 1
        if counter_fps == 60:
            timer -= 1
            counter_fps = 0

        if not player.on_block:
            player.gravity += 1
            player.rect.y += player.gravity
            coll = False
            for platform in platforms:
                if player.rect.colliderect(platform.rect):
                    if platform.isbad:
                        return False
                    player.on_block = True
                    player.rect.y -= player.gravity
                    player.gravity = 0
        else:
            player.rect.y += 1
            coll = False
            for platform in platforms:
                if player.rect.colliderect(platform.rect):
                    coll = True
                    if platform.isbad:
                        return False
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

        hits = pygame.sprite.groupcollide(platforms, fires, False, True)
        hits = pygame.sprite.groupcollide(blocks, fires, True, True)
        for key in hits.keys():
            if key.is_correct:
                return False

        blocks_need_delete = []
        all_correct = True
        for key in hits.keys():
            for block in blocks:
                if block.num_group == key.num_group:
                    if block.is_correct:
                        blocks_need_delete.append(block)
                    else:
                        all_correct = False
                        break

        if all_correct:
            for block in blocks_need_delete:
                blocks.remove(block)

        for block in blocks:
            if player.rect.colliderect(block.rect):
                if player.rect.centerx < block.rect.left:  # Персонаж движется справа налево
                    player.rect.right = block.rect.left  # Корректируем его позицию
                elif player.rect.centerx > block.rect.right:  # Персонаж движется слева направо
                    player.rect.left = block.rect.right  # Корректируем его позицию
                elif player.rect.centery < block.rect.top:  # Персонаж движется снизу вверх
                    player.rect.bottom = block.rect.top  # Корректируем его позицию
                elif player.rect.centery > block.rect.bottom:  # Персонаж движется сверху вниз
                    player.rect.top = block.rect.bottom  # Корректируем его позицию

        for platform in platforms:
            if player.rect.colliderect(platform.rect):
                if platform.isbad:
                    return False
                if player.rect.centerx < platform.rect.left:
                    player.rect.right = platform.rect.left
                elif player.rect.centerx > platform.rect.right:
                    player.rect.left = platform.rect.right
                elif player.rect.centery < platform.rect.top:
                    player.rect.bottom = platform.rect.top
                elif player.rect.centery > platform.rect.bottom:
                    player.rect.top = platform.rect.bottom
        pygame.draw.rect(screen, (255, 0, 0), (960, 20, timer * 2, 30))
        all_sprites.update()
        all_sprites.draw(screen)
        units_group.update()
        units_group.draw(screen)
        blocks.draw(screen)
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

        # Находит ближайшего NPC
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
