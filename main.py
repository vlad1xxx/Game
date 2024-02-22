import math
import pytmx
import pygame
import sys
import os
import random
from settings import FONT_25

WIDTH = 1920
HEIGHT = 1040
IMAGES = {'0': 'blocks/number1.png',
          '1': 'blocks/number2.png',
          '2': 'blocks/number3.png',
          '3': 'blocks/number4.png',
          '4': 'blocks/number5.png',
          '5': 'blocks/number6.png',
          '6': 'blocks/number7.png',
          '7': 'blocks/number8.png',
          '8': 'blocks/number9.png',
          '9': 'blocks/number10.png',
          '+': 'blocks/symbol_plus.png',
          '=': 'blocks/symbol_equal.png',
          '-': 'blocks/symbol_minus.png',
          '*': 'blocks/symbol_mult.png'}

GOOD_PLATFORMS = [
    9, 10, 12, 13, 16, 20, 22, 28, 29
]
BAD_PLATFORMS = [
    81, 82, 83, 84
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60


class MainHero(pygame.sprite.Sprite):

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = load_image("character.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 8
        self.gravity = 0
        self.on_block = True


class NPC:
    def __init__(self, x, y, name, dialogue):
        self.x = x
        self.y = y
        self.name = name
        self.dialogue = dialogue


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


def load_image(name):
    fullname = os.path.join('images/', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def generate_random_algebraic_conversions(count_correct_num, count_incorrect_num, num_group, x, y, direction):
    conversions = []
    random_num = random.choices(['1', '2', '3', '4', '5', '6', '7', '8', '9'], k=count_correct_num)
    for num in random_num:
        conversions.append(Block(0, 0, True, num_group, num))
    conversions.insert(random.randrange(1, len(conversions)),
                       Block(0, 0, True, num_group, random.choice(['+', '-', '*'])))
    line = ''
    for elem in conversions:
        line += elem.value
    result = eval(line)
    conversions.append(Block(0, 0, True, num_group, '='))
    for num in str(result):
        conversions.append(Block(0, 0, True, num_group, num))

    while count_incorrect_num != 0:
        flag = True
        incorrect_num = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        for elem in conversions:
            if incorrect_num == elem.value:
                flag = False
                break
        if flag:
            conversions.insert(random.randrange(count_correct_num + 1), Block(0, 0, False, num_group, incorrect_num))
            count_incorrect_num -= 1

    if direction == 'horizontal':
        for i in range(len(conversions)):
            conversions[i].rect.x = x + i * 80
            conversions[i].rect.y = y
    elif direction == 'vertical':
        for i in range(len(conversions)):
            conversions[i].rect.x = x
            conversions[i].rect.y = y + i * 80
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


def generate_level(level, all_group, group_plats):
    for y in range(level.height):
        s = ''
        for x in range(level.width):

            image = level.get_tile_image(x, y, 0)
            lvl_id = level.tiledgidmap[level.get_tile_gid(x, y, 0)]
            s += str(lvl_id) + ' '
            if lvl_id in BAD_PLATFORMS:
                all_group.add(Platform(x * level.tilewidth, y * level.tilewidth, image, True))
                group_plats.add(Platform(x * level.tilewidth, y * level.tilewidth, image, True))
            elif lvl_id in GOOD_PLATFORMS:
                all_group.add(Platform(x * level.tilewidth, y * level.tilewidth, image))
                group_plats.add(Platform(x * level.tilewidth, y * level.tilewidth, image))
            else:
                all_group.add(Platform(x * level.tilewidth, y * level.tilewidth, image))


def update_level(lvl, all_group, plat_group):
    lvl_map = pytmx.load_pygame(f'maps/{lvl}')
    all_group.empty()
    plat_group.empty()
    generate_level(lvl_map, all_group, plat_group)


def show_level(map_name, player_cords, pos_blocks, levels_to_update):
    updated_lvl_index = 0
    running = True

    timer = 5
    counter_fps = 0

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    units_group = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    fires = pygame.sprite.Group()

    for ls in pos_blocks:
        for block in generate_random_algebraic_conversions(ls[0], ls[1], ls[2], ls[3] * 80, ls[4] * 80, ls[5]):
            blocks.add(block)

    lvl_map = pytmx.load_pygame(f'maps/{map_name}')
    pl_crds = player_cords.copy()
    pl_crds[0] *= 80
    pl_crds[1] *= 80
    player = MainHero(units_group, pl_crds[0], pl_crds[1])
    generate_level(lvl_map, all_sprites, platforms)
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

            for ls in [platforms, blocks]:
                for elem in ls:
                    if player.rect.colliderect(elem.rect):
                        if isinstance(elem, Platform):
                            if elem.isbad:
                                return False
                        player.on_block = True
                        player.rect.y -= player.gravity
                        player.gravity = 0
        else:
            player.rect.y += 1
            coll = False
            for ls in [platforms, blocks]:
                for elem in ls:
                    if player.rect.colliderect(elem.rect):
                        coll = True
                        if isinstance(elem, Platform):
                            if elem.isbad:
                                return False
            if not coll:
                player.on_block = False
            else:
                player.rect.y -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.rect.x -= player.speed
        if keys[pygame.K_d]:
            player.rect.x += player.speed
        if keys[pygame.K_SPACE] and player.on_block and coll:
            player.rect.y -= 1
            player.gravity -= 20

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

        hits = pygame.sprite.groupcollide(blocks, fires, True, True)
        for key in hits.keys():
            if key.is_correct:
                return False

        blocks_need_delete = []
        for key in hits.keys():
            for block in blocks:
                if block.num_group == key.num_group:
                    if block.is_correct:
                        blocks_need_delete.append(block)
                    else:
                        break

        need_to_update = False
        for block in blocks_need_delete:
            blocks.remove(block)
            need_to_update = True

        if need_to_update:

            update_level(levels_to_update[updated_lvl_index], all_sprites, platforms)
            updated_lvl_index += 1

        pygame.sprite.groupcollide(fires, platforms, True, False)

        for ls in [platforms, blocks]:
            for elem in ls:
                if player.rect.colliderect(elem.rect):
                    if isinstance(elem, Platform):
                        if elem.isbad:
                            return False
                    if player.rect.centerx < elem.rect.left:  # Персонаж движется справа налево
                        player.rect.right = elem.rect.left  # Корректируем его позицию
                    elif player.rect.centerx > elem.rect.right:  # Персонаж движется слева направо
                        player.rect.left = elem.rect.right  # Корректируем его позицию
                    elif player.rect.centery < elem.rect.top:  # Персонаж движется снизу вверх
                        player.rect.bottom = elem.rect.top  # Корректируем его позицию
                    elif player.rect.centery > elem.rect.bottom:  # Персонаж движется сверху вниз
                        player.rect.top = elem.rect.bottom  # Корректируем его позицию

        if player.rect.right >= WIDTH or player.rect.left <= 0:
            return True

        pygame.draw.rect(screen, (255, 0, 0), (960, 20, timer * 2, 30))
        all_sprites.update()
        all_sprites.draw(screen)
        units_group.update()
        units_group.draw(screen)
        blocks.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


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
    def is_near_npc(player_, npc_):
        distance = ((player_.rect.x - npc_.x) ** 2 + (player_.rect.y - npc_.y) ** 2) ** 0.5
        return distance < 75

    def render_use():
        text = FONT_25.render('Нажмите "E", чтобы взаимодействовать', True, (0, 0, 0))
        screen.blit(text, (WIDTH - 400, 5))

    def render_dialog(near_npc_):
        dialog = FONT_25.render(near_npc_.dialogue, True, (0, 0, 0))
        screen.blit(dialog, (near_npc_.x + 50, near_npc_.y - 50))

    all_sprites = pygame.sprite.Group()

    npcs = [
        NPC(200, 200, "Bob", "Hello, traveler!"),
        NPC(262, 706, "Alice", "Nice to meet you!"),
        NPC(1588, 166, "Charlie", "How can I help you?"),
        NPC(1084, 724, "Doctor", "Do you want to be treated?")
    ]

    player = MainHero(all_sprites, 500, 500)

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
            return near_npc.name
        elif near_npc is not None:  # Открывает диалог с NPC
            render_use()
            render_dialog(near_npc)
        pygame.display.flip()
        clock.tick(FPS)


LEVELS = {
    'Bob': [{'map1.tmx': [[[12, 6]], False, [[2, 1, 1, 9, 2, 'horizontal']], ['map1.1.tmx']],
             'map2.tmx': [[[2, 2]], False, [[2, 1, 1, 12, 3, 'horizontal'],
                                            [2, 1, 2, 3, 5, 'vertical']], ['map2.1.tmx', 'map2.2.tmx']]}, False]
}


def main():
    start_screen()
    running = True
    while running:
        curr_npc = main_page()

        if curr_npc:
            for lvl in LEVELS[curr_npc][0].keys():
                player_cords = LEVELS[curr_npc][0][lvl][0][0]
                pos_blocks = LEVELS[curr_npc][0][lvl][2]
                levels_to_update = LEVELS[curr_npc][0][lvl][3]

                if show_level(lvl, player_cords, pos_blocks, levels_to_update) is True:
                    LEVELS[curr_npc][0][lvl][1] = True
                else:
                    break
        else:
            terminate()

        for npc in LEVELS.keys():
            is_npc_levels_passed = True
            for lvl in LEVELS[npc][0].keys():
                if LEVELS[npc][0][lvl][1] is False:
                    is_npc_levels_passed = False
                    break

            LEVELS[npc][1] = is_npc_levels_passed
        are_all_npc_passed = True
        for npc in LEVELS.keys():
            if LEVELS[npc][1] is False:
                are_all_npc_passed = False
                break

        GAME_OVER = are_all_npc_passed

        if GAME_OVER:
            running = False

    final_page()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
