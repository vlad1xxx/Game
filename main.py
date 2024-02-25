import math
import pytmx
import pygame
import sys
import os
import random
from settings import FONT_25, FONT_50

WIDTH = 1920
HEIGHT = 1040
TILE_SIZE = 80
PLAYER_LVL = 0
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
    9, 10, 12, 13, 16, 20, 21, 22, 28, 29, 15
]
BAD_PLATFORMS = [
    81, 82, 83, 84, 66, 91
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, group, x, y, player_lvl):
        super().__init__(group)
        if player_lvl == 0:
            self.image = load_image('upgrade.png')
            self.dialogue = 'Нажмите Shift для Рывка'
            self.upg_lvl = 1
        elif player_lvl == 1:
            self.image = load_image('upgrade.png')
            self.dialogue = 'Двойной прыжок'
            self.upg_lvl = 2
        else:
            self.image = load_image('upgrade.png')
            self.dialogue = 'хз'

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MainHero(pygame.sprite.Sprite):

    def __init__(self, group, x, y, level):
        super().__init__(group)
        self.run_anim_right = [load_image('player_animation/player_run/right/player_run1_right.png'),
                               load_image('player_animation/player_run/right/player_run2_right.png'),
                               load_image('player_animation/player_run/right/player_run3_right.png'),
                               load_image('player_animation/player_run/right/player_run4_right.png'),
                               load_image('player_animation/player_run/right/player_run5_right.png'),
                               load_image('player_animation/player_run/right/player_run6_right.png'),
                               load_image('player_animation/player_run/right/player_run7_right.png'),
                               load_image('player_animation/player_run/right/player_run8_right.png')]

        self.run_anim_left = [load_image('player_animation/player_run/left/player_run1_left.png'),
                              load_image('player_animation/player_run/left/player_run2_left.png'),
                              load_image('player_animation/player_run/left/player_run3_left.png'),
                              load_image('player_animation/player_run/left/player_run4_left.png'),
                              load_image('player_animation/player_run/left/player_run5_left.png'),
                              load_image('player_animation/player_run/left/player_run6_left.png'),
                              load_image('player_animation/player_run/left/player_run7_left.png'),
                              load_image('player_animation/player_run/left/player_run8_left.png')]

        self.stay_anim_right = [load_image('player_animation/player_stay/right/player_stay1_right.png'),
                                load_image('player_animation/player_stay/right/player_stay2_right.png'),
                                load_image('player_animation/player_stay/right/player_stay3_right.png'),
                                load_image('player_animation/player_stay/right/player_stay4_right.png'),
                                load_image('player_animation/player_stay/right/player_stay5_right.png'),
                                load_image('player_animation/player_stay/right/player_stay6_right.png'),
                                load_image('player_animation/player_stay/right/player_stay7_right.png'),
                                load_image('player_animation/player_stay/right/player_stay8_right.png')]

        self.stay_anim_left = [load_image('player_animation/player_stay/left/player_stay1_left.png'),
                               load_image('player_animation/player_stay/left/player_stay2_left.png'),
                               load_image('player_animation/player_stay/left/player_stay3_left.png'),
                               load_image('player_animation/player_stay/left/player_stay4_left.png'),
                               load_image('player_animation/player_stay/left/player_stay5_left.png'),
                               load_image('player_animation/player_stay/left/player_stay6_left.png'),
                               load_image('player_animation/player_stay/left/player_stay7_left.png'),
                               load_image('player_animation/player_stay/left/player_stay8_left.png')]

        self.jump_anim_right = [load_image('player_animation/player_jump/right/player_jump1_right.png'),
                                load_image('player_animation/player_jump/right/player_jump2_right.png'),
                                load_image('player_animation/player_jump/right/player_jump3_right.png'),
                                load_image('player_animation/player_jump/right/player_jump4_right.png'),
                                load_image('player_animation/player_jump/right/player_jump5_right.png'),
                                load_image('player_animation/player_jump/right/player_jump6_right.png'),
                                load_image('player_animation/player_jump/right/player_jump7_right.png'),
                                load_image('player_animation/player_jump/right/player_jump8_right.png')]

        self.jump_anim_left = [load_image('player_animation/player_jump/left/player_jump1_left.png'),
                               load_image('player_animation/player_jump/left/player_jump2_left.png'),
                               load_image('player_animation/player_jump/left/player_jump3_left.png'),
                               load_image('player_animation/player_jump/left/player_jump4_left.png'),
                               load_image('player_animation/player_jump/left/player_jump5_left.png'),
                               load_image('player_animation/player_jump/left/player_jump6_left.png'),
                               load_image('player_animation/player_jump/left/player_jump7_left.png'),
                               load_image('player_animation/player_jump/left/player_jump8_left.png')]

        self.shoot_anim_right = [load_image('player_animation/player_shoot/right/player_shoot1_right.png'),
                                 load_image('player_animation/player_shoot/right/player_shoot2_right.png'),
                                 load_image('player_animation/player_shoot/right/player_shoot3_right.png'),
                                 load_image('player_animation/player_shoot/right/player_shoot4_right.png')]

        self.shoot_anim_left = [load_image('player_animation/player_shoot/left/player_shoot1_left.png'),
                                load_image('player_animation/player_shoot/left/player_shoot2_left.png'),
                                load_image('player_animation/player_shoot/left/player_shoot3_left.png'),
                                load_image('player_animation/player_shoot/left/player_shoot4_left.png')]

        self.image = self.stay_anim_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 8
        self.gravity = 0
        self.on_block = True
        self.is_moving = False
        self.walk_index = 0
        self.is_jumping = False
        self.jump_index = 0
        self.stay_index = 0
        self.clicked_mouse = False
        self.shoot_index = 0
        self.direction = 'right'
        self.is_dash = False
        self.is_dashing = False
        self.dash_avaible = True
        self.level = level

    def update(self, fires, all_sprites):
        if self.clicked_mouse:  # Проверяем, стреляет ли игрок
            mouseX, mouseY = pygame.mouse.get_pos()
            if mouseX > self.rect.x:
                self.direction = 'right'
            elif mouseX < self.rect.x:
                self.direction = 'left'
            if self.direction == 'right':
                self.image = self.shoot_anim_right[self.shoot_index]
                self.shoot_index = (self.shoot_index + 1) % len(self.shoot_anim_right)
            elif self.direction == 'left':
                self.image = self.shoot_anim_left[self.shoot_index]
                self.shoot_index = (self.shoot_index + 1) % len(self.shoot_anim_left)
            if self.shoot_index == 2:  # Если анимация выстрела завершилась
                player_pos = (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2)
                angle = math.atan2(mouseY - player_pos[1], mouseX - player_pos[0])
                fire = Fire(player_pos[0], player_pos[1], angle)
                fires.add(fire)
                all_sprites.add(fire)
            if self.shoot_index == 0:
                self.clicked_mouse = False
        elif self.is_jumping:
            if self.direction == 'right':
                self.image = self.jump_anim_right[self.jump_index]
                self.jump_index = (self.jump_index + 1) % len(self.jump_anim_right)
            elif self.direction == 'left':
                self.image = self.jump_anim_left[self.jump_index]
                self.jump_index = (self.jump_index + 1) % len(self.jump_anim_left)
        elif self.is_moving:
            if self.direction == 'right':
                self.image = self.run_anim_right[self.walk_index]
                self.walk_index = (self.walk_index + 1) % len(self.run_anim_right)
            elif self.direction == 'left':
                self.image = self.run_anim_left[self.walk_index]
                self.walk_index = (self.walk_index + 1) % len(self.run_anim_left)
        else:
            if self.direction == 'right':
                self.image = self.stay_anim_right[self.stay_index]
                self.stay_index = (self.stay_index + 1) % len(self.stay_anim_right)
            elif self.direction == 'left':
                self.image = self.stay_anim_left[self.stay_index]
                self.stay_index = (self.stay_index + 1) % len(self.stay_anim_left)


class Door:
    def __init__(self, x, y, name, dialogue):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - 80, self.y - 240, 160, 320)
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
            conversions.insert(random.randrange(len(conversions) + 1), Block(0, 0, False, num_group, incorrect_num))
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


def show_level(map_name, player_cords, pos_blocks, levels_to_update, upgrade_pos=None):
    global PLAYER_LVL, FPS

    def render_use():
        text = FONT_25.render('Нажмите "E", чтобы Взаимодействовать', True, (255, 255, 255))
        screen.blit(text, (WIDTH - 400, 5))

    def render_dialog(upg):
        dialog = FONT_50.render(upg.dialogue, True, (255, 255, 255))
        screen.blit(dialog, (upg.rect.x - 60, upg.rect.y - 100))

    updated_lvl_index = 0
    running = True

    timer = 5
    counter_fps = 0
    slow_motion = False

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    units_group = pygame.sprite.Group()
    upgrade_group = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    fires = pygame.sprite.Group()

    upgrade = None

    for ls in pos_blocks:
        for block in generate_random_algebraic_conversions(ls[0], ls[1], ls[2], ls[3] * 80, ls[4] * 80, ls[5]):
            blocks.add(block)

    lvl_map = pytmx.load_pygame(f'maps/{map_name}')
    pl_crds = player_cords.copy()
    pl_crds[0] *= 80
    pl_crds[1] *= 80
    player = MainHero(units_group, pl_crds[0], pl_crds[1], PLAYER_LVL)
    generate_level(lvl_map, all_sprites, platforms)

    if upgrade_pos and player.level == 0:
        upgrade = Upgrade(upgrade_group, upgrade_pos[0] * TILE_SIZE + 20, upgrade_pos[1] * TILE_SIZE + 20, PLAYER_LVL)

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

        if not player.on_block:
            player.gravity += 1
            if player.is_dashing:
                player.gravity = 0
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
            player.dash_avaible = True
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
        if keys[pygame.K_a] and not player.is_dashing:
            player.rect.x -= player.speed
            player.is_moving = True
            player.direction = 'left'
        elif keys[pygame.K_d] and not player.is_dashing:
            player.rect.x += player.speed
            player.is_moving = True
            player.direction = 'right'
        else:
            player.is_moving = False
            player.walk_index = 0

        if keys[pygame.K_SPACE] and player.on_block and coll:
            player.rect.y -= 1
            player.gravity -= 20
            player.is_jumping = True
        elif player.on_block:
            player.is_jumping = False
            player.jump_index = 0

        if keys[pygame.K_LSHIFT] and not player.is_dashing and player.dash_avaible and player.level > 0:
            player.is_dash = False
            player.dash_avaible = False
            if slow_motion:
                slow_motion = False
                FPS = 60
            dash_distance = 240  # Distance for dash
            target_x = player.rect.x - dash_distance if player.direction == 'left' else player.rect.x + dash_distance

            # Calculate the distance and direction for the dash
            dash_distance = abs(target_x - player.rect.x)
            dash_direction = -1 if target_x < player.rect.x else 1

            # Set up flags for dash state
            player.is_dashing = True
            player.dash_step = player.speed * 2 * dash_direction

        elif not keys[pygame.K_LSHIFT]:
            player.is_dash = True

        # Continue the dash movement if the player is dashing
        if player.is_dashing:
            if abs(player.rect.x - target_x) <= abs(player.dash_step):
                player.rect.x = target_x
                player.is_dashing = False
            else:
                player.rect.x += player.dash_step

        mouse_buttons = pygame.mouse.get_pressed()
        if not player.clicked_mouse and mouse_buttons[0]:
            player.clicked_mouse = True

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
                        timer = 5
                    else:
                        break

        need_to_update = False
        for block in blocks_need_delete:
            blocks.remove(block)
            need_to_update = True

        if need_to_update:
            if levels_to_update:
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
                        player.is_dashing = False
                    elif player.rect.centerx > elem.rect.right:  # Персонаж движется слева направо
                        player.rect.left = elem.rect.right
                        player.is_dashing = False  # Корректируем его позицию
                    elif player.rect.centery < elem.rect.top:  # Персонаж движется снизу вверх
                        player.rect.bottom = elem.rect.top
                        player.is_dashing = False  # Корректируем его позицию
                    elif player.rect.centery > elem.rect.bottom:  # Персонаж движется сверху вниз
                        player.rect.top = elem.rect.bottom
                        player.is_dashing = False  # Корректируем его позицию

        if player.rect.right >= WIDTH or player.rect.left <= 0 or player.rect.bottom >= HEIGHT:
            return True

        if upgrade:
            if pygame.sprite.collide_rect(player, upgrade):
                PLAYER_LVL = upgrade.upg_lvl
                player.level = upgrade.upg_lvl
                slow_motion = True
                upgrade_group.empty()

        if slow_motion:
            FPS = 10

        all_sprites.update()
        all_sprites.draw(screen)
        if counter_fps % 8 == 0:
            player.update(fires, all_sprites)
        units_group.draw(screen)
        blocks.draw(screen)

        counter_fps += 1
        if blocks:
            timer -= 0.01666667
            pygame.draw.rect(screen, 'grey', (800, 20, 300, 30))
            if timer < 2:
                pygame.draw.rect(screen, 'red', (800, 20, 60 * timer, 30))
            else:
                pygame.draw.rect(screen, 'yellow', (800, 20, 60 * timer, 30))
            if timer <= 0:
                return False
        if counter_fps == 60:
            counter_fps = 0
        pygame.draw.rect(screen, 'red', player.rect, 5)
        print(player.level)
        if updated_lvl_index == 2:
            if upgrade:

                upgrade_group.draw(screen)
                if pygame.sprite.collide_rect(player, upgrade):
                    render_use()
                    render_dialog(upgrade)
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
    def is_near_door(player_, npc_):
        return pygame.sprite.collide_rect(player_, npc_)

    def render_use():
        text = FONT_25.render('Нажмите "E", чтобы Войти', True, (255, 255, 255))
        screen.blit(text, (WIDTH - 400, 5))

    def render_dialog(near_npc_):
        dialog = FONT_25.render(near_npc_.dialogue, True, (255, 255, 255))
        screen.blit(dialog, (near_npc_.x - 60, near_npc_.y - 100))

    doors = [
        Door(5 * 80, 10 * 80, "Earth", "Пещера Земли"),
        Door(19 * 80, 10 * 80, "Sand", "Пещера песка"),
        Door(21 * 80, 2 * 80, "Fire", "Пещера лавы"),
        Door(3 * 80, 4 * 80, "Water", "Пещера воды")
    ]

    running = True

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    unit_group = pygame.sprite.Group()

    lvl_map = pytmx.load_pygame(f'maps/lobby.tmx')

    player = MainHero(unit_group, 12 * 80, 6 * 80, PLAYER_LVL)
    generate_level(lvl_map, all_sprites, platforms)
    counter_fps = 0

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

        if not player.on_block:
            player.gravity += 1
            if player.is_dashing:
                player.gravity = 0
            player.rect.y += player.gravity

            for ls in [platforms]:
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
            for ls in [platforms]:
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
        if keys[pygame.K_a] and not player.is_dashing:
            player.rect.x -= player.speed
            player.is_moving = True
            player.direction = 'left'
        elif keys[pygame.K_d] and not player.is_dashing:
            player.rect.x += player.speed
            player.is_moving = True
            player.direction = 'right'
        else:
            player.is_moving = False
            player.walk_index = 0

        if keys[pygame.K_SPACE] and player.on_block and coll:
            player.rect.y -= 1
            player.gravity -= 20
            player.is_jumping = True
        elif player.on_block:
            player.is_jumping = False
            player.jump_index = 0

        if keys[pygame.K_LSHIFT] and player.is_dash:
            player.is_dash = False
            dash_distance = 240  # Distance for dash
            target_x = player.rect.x - dash_distance if player.direction == 'left' else player.rect.x + dash_distance

            # Calculate the distance and direction for the dash
            dash_distance = abs(target_x - player.rect.x)
            dash_direction = -1 if target_x < player.rect.x else 1

            # Set up flags for dash state
            player.is_dashing = True
            player.dash_step = player.speed * 2 * dash_direction

        elif not keys[pygame.K_LSHIFT]:
            player.is_dash = True

        # Continue the dash movement if the player is dashing
        if player.is_dashing:
            if abs(player.rect.x - target_x) <= abs(player.dash_step):
                player.rect.x = target_x
                player.is_dashing = False
            else:
                player.rect.x += player.dash_step

        for ls in [platforms]:
            for elem in ls:
                if player.rect.colliderect(elem.rect):
                    if isinstance(elem, Platform):
                        if elem.isbad:
                            return False
                    if player.rect.centerx < elem.rect.left:  # Персонаж движется справа налево
                        player.rect.right = elem.rect.left  # Корректируем его позицию
                        player.is_dashing = False
                    elif player.rect.centerx > elem.rect.right:  # Персонаж движется слева направо
                        player.rect.left = elem.rect.right
                        player.is_dashing = False  # Корректируем его позицию
                    elif player.rect.centery < elem.rect.top:  # Персонаж движется снизу вверх
                        player.rect.bottom = elem.rect.top
                        player.is_dashing = False  # Корректируем его позицию
                    elif player.rect.centery > elem.rect.bottom:  # Персонаж движется сверху вниз
                        player.rect.top = elem.rect.bottom
                        player.is_dashing = False  # Корректируем его позицию

        all_sprites.update()
        all_sprites.draw(screen)
        if counter_fps % 8 == 0:
            player.update(None, None)
        unit_group.draw(screen)

        if player.rect.right >= WIDTH or player.rect.left <= 0 or player.rect.bottom >= HEIGHT:
            return True

        for door in doors:
            if is_near_door(player, door):
                near_door = door
                break
            else:
                near_door = None

        if near_door is not None and keys[pygame.K_e]:
            return near_door.name

        elif near_door is not None:
            render_use()
            render_dialog(near_door)

        counter_fps += 1
        if counter_fps == 60:
            counter_fps = 0
        pygame.display.flip()
        clock.tick(FPS)


LEVELS = {
    'Earth': [{'map1.tmx': [[[12, 6]], False, [[2, 1, 1, 9, 2, 'horizontal']], ['map1.1.tmx']],
               'map2.tmx': [[[2, 2]], False, [[2, 1, 1, 12, 3, 'horizontal'],
                                              [2, 1, 2, 3, 5, 'vertical']], ['map2.1.tmx', 'map2.2.tmx'], [5, 6]]},
              False],
    'Sand': [{'map1.tmx': [[[12, 6]], False, [[2, 1, 1, 9, 2, 'horizontal']], ['map1.1.tmx']],
              'map2.tmx': [[[2, 2]], False, [[2, 1, 1, 12, 3, 'horizontal'],
                                             [2, 1, 2, 3, 5, 'vertical']], ['map2.1.tmx', 'map2.2.tmx']]}, False],
    'Fire': [{'map1.tmx': [[[12, 6]], False, [[2, 1, 1, 9, 2, 'horizontal']], ['map1.1.tmx']],
              'map2.tmx': [[[2, 2]], False, [[2, 1, 1, 12, 3, 'horizontal'],
                                             [2, 1, 2, 3, 5, 'vertical']], ['map2.1.tmx', 'map2.2.tmx']]}, False],
    'Water': [{'map3.tmx': [[[5, 3]], False, [[2, 1, 1, 8, 0, 'vertical'], [2, 1, 2, 16, 4, 'horizontal']], []],
               'map4.tmx': [[[3, 0]], False, [[2, 1, 1, 6, 6, 'vertical'], [2, 1, 2, 11, 5, 'horizontal']], []]
               }, False]
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
                upgrade_pos = None
                if len(LEVELS[curr_npc][0][lvl]) > 4:
                    upgrade_pos = LEVELS[curr_npc][0][lvl][4]

                if show_level(lvl, player_cords, pos_blocks, levels_to_update, upgrade_pos) is True:
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
