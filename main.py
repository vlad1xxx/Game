import math
import pytmx
import pygame
import sys
import os
import random
from settings import FONT_25

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
    9, 10, 12, 13, 16, 20, 21, 22, 28, 29, 15, 52, 44, 37, 36, 72, 78
]
BAD_PLATFORMS = [
    81, 82, 83, 84, 66, 91, 64
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, group, x, y, player_lvl):
        super().__init__(group)
        if player_lvl == 0:
            self.image = load_image('upgrade_dash.png')
            self.dialogue = 'Нажмите Shift для Рывка'
            self.upg_lvl = 1
        elif player_lvl == 1:
            self.image = load_image('upgrade_doublejump.png')
            self.dialogue = 'Теперь вам доступен двойной прыжок'
            self.upg_lvl = 2
        elif player_lvl == 2:
            self.image = load_image('upgrade_dash.png')
            self.dialogue = 'Ключ от Огненного подземелья'
            self.upg_lvl = 3
        else:
            self.image = load_image('upgrade_dash.png')
            self.dialogue = 'Ключ от Огненного подземелья'
            self.upg_lvl = 3
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
        self.slow_motion = False
        self.coll = False
        self.target_x = 0
        self.double_jump_available = False
        self.space_pressed = False

    def update_movement(self, sprites):
        global FPS
        if not self.on_block:
            self.gravity += 1
            if self.is_dashing:
                self.gravity = 0
            self.rect.y += self.gravity

            for ls in sprites:
                for elem in ls:
                    if self.rect.colliderect(elem.rect):
                        if isinstance(elem, Platform):
                            if elem.isbad:
                                return False
                        self.on_block = True
                        self.rect.y -= self.gravity
                        self.gravity = 0
        else:
            self.rect.y += 1
            self.coll = False
            self.dash_avaible = True
            for ls in sprites:
                for elem in ls:
                    if self.rect.colliderect(elem.rect):
                        self.coll = True
                        if isinstance(elem, Platform):
                            if elem.isbad:
                                return False
            if not self.coll:
                self.on_block = False
            else:
                self.rect.y -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not self.is_dashing:
            self.rect.x -= self.speed
            self.is_moving = True
            self.direction = 'left'
        elif keys[pygame.K_d] and not self.is_dashing:
            self.rect.x += self.speed
            self.is_moving = True
            self.direction = 'right'
        else:
            self.is_moving = False
            self.walk_index = 0

        if keys[pygame.K_SPACE] and not self.space_pressed:  # Проверяем, что клавиша пробела не была нажата ранее
            if self.on_block and self.coll:
                self.rect.y -= 1
                self.gravity = -20
                self.is_jumping = True
                if self.level > 1:
                    self.double_jump_available = True
            elif self.double_jump_available:
                self.rect.y -= 1
                self.gravity = -20
                self.is_jumping = True
                self.double_jump_available = False
            self.space_pressed = True
        elif self.on_block:
            self.is_jumping = False
            self.jump_index = 0
        if not keys[pygame.K_SPACE]:
            self.space_pressed = False

        if keys[pygame.K_LSHIFT] and not self.is_dashing and self.dash_avaible and self.level > 0:
            self.is_dash = False
            self.dash_avaible = False
            self.dash_distance = 240  # Distance for dash
            self.target_x = self.rect.x - self.dash_distance \
                if self.direction == 'left' else self.rect.x + self.dash_distance

            # Calculate the distance and direction for the dash
            self.dash_distance = abs(self.target_x - self.rect.x)
            if self.target_x < self.rect.x:
                self.dash_direction = -1
            else:
                self.dash_direction = 1

            # Set up flags for dash state
            self.is_dashing = True
            self.dash_step = self.speed * 2 * self.dash_direction

        elif not keys[pygame.K_LSHIFT]:
            self.is_dash = True

        # Continue the dash movement if the player is dashing
        if self.is_dashing:
            self.slow_motion = False
            FPS = 60
            if abs(self.rect.x - self.target_x) <= abs(self.dash_step):
                self.rect.x = self.target_x
                self.is_dashing = False
            else:
                self.rect.x += self.dash_step

        mouse_buttons = pygame.mouse.get_pressed()
        if not self.clicked_mouse and mouse_buttons[0]:
            self.clicked_mouse = True

        for ls in sprites:
            for elem in ls:
                if self.rect.colliderect(elem.rect):
                    if isinstance(elem, Platform):
                        if elem.isbad:
                            return False
                    if self.rect.centerx < elem.rect.left:  # Персонаж движется справа налево
                        self.rect.right = elem.rect.left  # Корректируем его позицию
                        self.is_dashing = False
                    elif self.rect.centerx > elem.rect.right:  # Персонаж движется слева направо
                        self.rect.left = elem.rect.right
                        self.is_dashing = False  # Корректируем его позицию
                    elif self.rect.centery < elem.rect.top:  # Персонаж движется снизу вверх
                        self.rect.bottom = elem.rect.top
                        self.is_dashing = False  # Корректируем его позицию
                    elif self.rect.centery > elem.rect.bottom:  # Персонаж движется сверху вниз
                        self.rect.top = elem.rect.bottom
                        self.is_dashing = False  # Корректируем его позицию
        return True

    def update(self, fires, all_sprites, fire_available):
        if pygame.mouse.get_pressed()[0]:
            self.clicked_mouse = True
        if not fire_available:
            self.clicked_mouse = False
        if self.clicked_mouse:  # Проверяем, стреляет ли игрок
            if fires is not None:
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)


class Door:
    def __init__(self, x, y, name, dialogue):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - 80, self.y - 160, 160, 240)
        self.name = name
        self.dialogue = dialogue


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


def guide():
    global PLAYER_LVL, FPS

    def render_dialog(dialogs, completed, pos):
        x = pos[0]
        y = pos[1]
        if completed:
            color = 'green'
        else:
            color = 'white'
        if type(dialogs) is list:
            for i in dialogs:
                dialog = FONT_25.render(i, True, color)
                screen.blit(dialog, (x, y))
                y += 50
        elif type(dialogs) is str:
            dialog = FONT_25.render(dialogs, True, color)
            screen.blit(dialog, (x, y))

    level_to_update = pytmx.load_pygame('maps/guide.1.tmx')
    running = True
    tasks = {
        'Нажмите клавишу A чтобы двигаться влево': [pygame.K_a, False, (100, 100)],
        'Нажмите клавишу D чтобы двигаться вправо': [pygame.K_d, False, (100, 200)],
        'Нажмите клавишу SPACE чтобы прыгнуть': [pygame.K_SPACE, False, (100, 300)]
    }

    examples_passed = None

    counter_fps = 0

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    units_group = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    fires = pygame.sprite.Group()

    lvl_map = pytmx.load_pygame(f'maps/guide.tmx')

    player = MainHero(units_group, 12 * TILE_SIZE, 7 * TILE_SIZE, PLAYER_LVL)
    timer = Timer(10, 800, 20)
    generate_level(lvl_map, all_sprites, platforms)

    render_incorrect_block_ = False
    render_examples = False
    render_timer = False
    final_exam = False

    is_guide_over = False
    render_death = False
    is_dead = False

    while running:
        screen.fill('gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                render_death = False
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_n:
                    return True

        player.update_movement([platforms, blocks])

        # Обновление выстрелов
        for fire in fires:
            fire.update()
        update_example = False
        final_update = False
        hits = pygame.sprite.groupcollide(blocks, fires, True, True)
        for key in hits.keys():
            if key.is_correct:
                if final_exam:
                    for block in blocks:
                        blocks.remove(block)
                    final_exam = False
                    final_update = False
                    for s in all_sprites:
                        all_sprites.remove(s)
                    for p in platforms:
                        platforms.remove(p)
                    generate_level(lvl_map, all_sprites, platforms)
                    render_incorrect_block_ = True
                    examples_passed = 0
                    update_example = True
                    blocks_need_delete.clear()
                else:
                    render_incorrect_block_ = True
                    render_examples = False
                    examples_passed = 0
                    for block in generate_random_algebraic_conversions(2, 1, 1, 9 * TILE_SIZE, 3 * TILE_SIZE,
                                                                       'horizontal'):
                        blocks.add(block)
            elif not key.is_correct:
                for block in blocks:
                    blocks.remove(block)
                examples_passed += 1
                if examples_passed < 4:
                    render_examples = True
                    update_example = True
                elif not final_exam and examples_passed == 4:
                    for s in all_sprites:
                        all_sprites.remove(s)
                    for p in platforms:
                        platforms.remove(p)
                    generate_level(level_to_update, all_sprites, platforms)
                    final_exam = True
                    final_update = True
                if final_exam:
                    final_exam = False
                    for block in blocks:
                        blocks.remove(block)
                    is_guide_over = True

                render_timer = False
                timer.timer = timer.max_seconds

        blocks_need_delete = []
        for key in hits.keys():
            for block in blocks:
                if block.num_group == key.num_group:
                    if block.is_correct:
                        blocks_need_delete.append(block)
                        timer.timer = timer.max_seconds
                    else:
                        break

        for block in blocks_need_delete:
            blocks.remove(block)

        pygame.sprite.groupcollide(fires, platforms, True, False)

        if player.rect.right >= WIDTH or player.rect.left <= 0 or player.rect.bottom >= HEIGHT:
            return False

        all_sprites.update()
        all_sprites.draw(screen)
        if counter_fps % 8 == 0:
            player.update(fires, all_sprites, True)
            for fire in fires:
                fire.update_animation()
        units_group.draw(screen)
        blocks.draw(screen)

        counter_fps += 1
        if blocks:
            timer.update()
            if timer.timer <= 0:
                if final_exam:
                    final_exam = False
                    platforms.empty()
                    all_sprites.empty()
                    generate_level(lvl_map, all_sprites, platforms)
                    final_update = False
                render_timer = True
                render_examples = False
                render_incorrect_block_ = False
                for block in blocks:
                    blocks.remove(block)
                for block in generate_random_algebraic_conversions(2, 1, 1, 9 * TILE_SIZE, 3 * TILE_SIZE, 'horizontal'):
                    blocks.add(block)
                timer.timer = timer.max_seconds
                examples_passed = 0
        if counter_fps == 60:
            counter_fps = 0

        task_need_to_delete = True
        if render_death:
            render_dialog(['Ваш персонаж не умеет плавать!', 'Нажмите любую кнопу чтобы продолжить'
                           ],
                          False, (100, 100))

        keys = pygame.key.get_pressed()

        if not render_death:
            for task in tasks.keys():
                if keys[tasks[task][0]]:
                    tasks[task][1] = True
                if not tasks[task][1]:
                    task_need_to_delete = False
                render_dialog(task, tasks[task][1], tasks[task][2])
            if not tasks:
                task_need_to_delete = False

            if task_need_to_delete:
                tasks.clear()
                for block in generate_random_algebraic_conversions(2, 1, 1, 9 * TILE_SIZE, 3 * TILE_SIZE, 'horizontal'):
                    blocks.add(block)
                examples_passed = 0

        if update_example:
            for block in generate_random_algebraic_conversions(2, 1, 1, 9 * TILE_SIZE, 3 * TILE_SIZE, 'horizontal'):
                blocks.add(block)

        if render_timer:
            render_dialog(['По истечении таймера вы проигрываете!',
                           'Попробуйте ещё раз'],
                          False, (100, 100))

        if examples_passed == 0 and not render_incorrect_block_ \
                and not render_examples and not render_timer and not tasks:
            render_dialog(['Это математические блоки, они будут мешать вам во время прохождения уровней.',
                           'Чтобы их уничтожить, нужно выстрелить с помощью ЛКМ в тот блок который противоречит '
                           'равенству.'], False, (100, 100))

        if render_incorrect_block_ and not render_examples:
            render_dialog(['Вы выстрелили в верный блок и нарушили равенство!',
                           'Попробуйте еще раз'],
                          False, (100, 100))
            examples_passed = 0
        if render_examples:
            render_dialog([f'Так держать! уничтожьте еще {4 - examples_passed} блока.',
                           ],
                          False, (100, 100))
        if examples_passed == 4:
            final_exam = True
            render_examples = False
            render_incorrect_block_ = False
            render_timer = False

        if final_exam:
            render_dialog([f'А вы довольно хорошо справились!',
                           'Но математические блоки иногда могут преграждать вам дорогу',
                           'Разрушьте последний математический блок чтобы покинуть обучение'
                           ],
                          False, (100, 100))
        if final_update:
            for block in generate_random_algebraic_conversions(2, 1, 1, 23 * TILE_SIZE, 1 * TILE_SIZE, 'vertical'):
                blocks.add(block)

        if is_guide_over and not final_exam:
            render_dialog([f'Поздравляю вы прошли обучение!'],
                          False, (100, 100))

        if is_dead:
            render_death = True
            for unit in units_group:
                units_group.remove(unit)
            player = MainHero(units_group, 12 * TILE_SIZE, 7 * TILE_SIZE, PLAYER_LVL)
            render_incorrect_block_ = False
            render_examples = False
            render_timer = False
            final_exam = False

            is_guide_over = False
            is_dead = False
            for s in all_sprites:
                all_sprites.remove(s)
            for p in platforms:
                platforms.remove(p)
            generate_level(lvl_map, all_sprites, platforms)
            for block in blocks:
                blocks.remove(block)

            tasks = {
                'Нажмите клавишу A чтобы двигаться влево': [pygame.K_a, False, (100, 100)],
                'Нажмите клавишу D чтобы двигаться вправо': [pygame.K_d, False, (100, 200)],
                'Нажмите клавишу SPACE чтобы прыгнуть': [pygame.K_SPACE, False, (100, 300)]
            }

        pygame.draw.rect(screen, 'red', player.rect, 5)

        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (1920, 1080))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                m_x = pos[0]
                m_y = pos[1]

                if event.button == 1 and 190 < m_x < 611 and 190 < m_y < 409:
                    return True

                if event.button == 1 and 190 < m_x < 760 and 490 < m_y < 709:
                    return guide()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()

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


def show_level(map_name, player_cords, pos_blocks, levels_to_update, upgrade_pos=None, endless=False):
    global PLAYER_LVL, FPS

    def render_dialog(upg):
        dialog = FONT_25.render(upg.dialogue, True, (255, 255, 255))
        screen.blit(dialog, (100, 100))

    updated_lvl_index = 0
    running = True

    counter_fps = 0

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    units_group = pygame.sprite.Group()
    upgrade_group = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    fires = pygame.sprite.Group()

    if not endless:
        for ls in pos_blocks:
            for block in generate_random_algebraic_conversions(ls[0], ls[1], ls[2], ls[3] * 80, ls[4] * 80, ls[5]):
                blocks.add(block)
    else:
        count_destroyed_blocks = 0
        score = 0
    upgrade = None

    lvl_map = pytmx.load_pygame(f'maps/{map_name}')
    pl_crds = player_cords.copy()
    pl_crds[0] *= 80
    pl_crds[1] *= 80
    player = MainHero(units_group, pl_crds[0], pl_crds[1], PLAYER_LVL)

    if endless:
        timer = Timer(8, 25, 20)
    else:
        timer = Timer(5, 800, 20)
    generate_level(lvl_map, all_sprites, platforms)
    if player.level == 3:
        player.level = 4
    if upgrade_pos and upgrade_pos[1] == 0:
        upgrade = Upgrade(upgrade_group, upgrade_pos[0][0] * TILE_SIZE + 20, upgrade_pos[0][1] * TILE_SIZE + 20,
                          PLAYER_LVL)
    elif upgrade_pos and upgrade_pos[1] == 1:
        upgrade = Upgrade(upgrade_group, upgrade_pos[0][0] * TILE_SIZE + 20, upgrade_pos[0][1] * TILE_SIZE + 20,
                          PLAYER_LVL)
    elif upgrade_pos and upgrade_pos[1] == 2:
        upgrade = Upgrade(upgrade_group, upgrade_pos[0][0] * TILE_SIZE + 20, upgrade_pos[0][1] * TILE_SIZE + 20,
                          PLAYER_LVL)

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

        if endless and not blocks:
            ls = random.choice(pos_blocks)
            for block in generate_random_algebraic_conversions(ls[0], ls[1], ls[2], ls[3] * 80, ls[4] * 80, ls[5]):
                blocks.add(block)

        status = player.update_movement([blocks, platforms])
        if not status:
            return False

        if player.rect.right >= WIDTH or player.rect.left <= 0 \
                or player.rect.bottom >= HEIGHT or player.rect.bottom <= 0:
            return True

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
                        if endless:
                            score += 10
                            count_destroyed_blocks += 1
                            score += int(timer.timer * 5)
                        timer.timer = timer.max_seconds

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

        if upgrade:
            if pygame.sprite.collide_rect(player, upgrade):
                if player.level == 0:
                    player.slow_motion = True
                PLAYER_LVL = upgrade.upg_lvl
                player.level = upgrade.upg_lvl
                upgrade_group.empty()

        if player.slow_motion:
            FPS = 10
        all_sprites.update()
        all_sprites.draw(screen)
        if counter_fps % 8 == 0:
            player.update(fires, all_sprites, True)
            for fire in fires:
                fire.update_animation()
        units_group.draw(screen)
        blocks.draw(screen)

        if endless:
            score_text = FONT_25.render(f'Score: {score}', False, (255, 255, 255))
            screen.blit(score_text, (25, 50))

        counter_fps += 1
        if blocks:
            if not timer.update():
                return False
        pygame.draw.rect(screen, 'red', player.rect, 5)
        if updated_lvl_index == 2 and player.level == 0:
            if upgrade:
                upgrade_group.draw(screen)
                if pygame.sprite.collide_rect(player, upgrade):
                    render_dialog(upgrade)
        if player.slow_motion:
            if upgrade:
                render_dialog(upgrade)
        if map_name == 'cloud_map2.tmx':
            if upgrade:
                if player.level == 3:
                    render_dialog(upgrade)
                else:
                    upgrade_group.draw(screen)

        if player.level == 2 and map_name == 'map4.tmx':
            if upgrade:
                render_dialog(upgrade)
        if player.level == 1 and updated_lvl_index != 2:
            if upgrade:
                upgrade_group.draw(screen)
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
        Door(5 * 80, 10 * 80, "Earth", "Подземелье земли"),
        Door(19 * 80, 10 * 80, "Fire", "Пещера огня"),
        Door(21 * 80, 3 * 80, "Cloud", "Облачное подземелье"),
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
                    return False

        status = player.update_movement([platforms])
        if not status:
            return False

        all_sprites.update()
        all_sprites.draw(screen)
        unit_group.draw(screen)

        keys = pygame.key.get_pressed()

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

        if counter_fps % 8 == 0:
            player.update(None, None, False)

        counter_fps += 1
        if counter_fps == 60:
            counter_fps = 0

        pygame.display.flip()
        clock.tick(FPS)


LEVELS = {
    'Earth': [{'map1.tmx': [[[12, 6]], False, [[2, 1, 1, 9, 2, 'horizontal']], ['map1.1.tmx']],
               'map2.tmx': [[[2, 2]], False, [[2, 1, 1, 12, 3, 'horizontal'],
                                              [2, 1, 2, 3, 5, 'vertical']], ['map2.1.tmx', 'map2.2.tmx'], [[5, 6], 1]]},
              False, False],
    'Cloud': [{'cloud_map1.tmx': [[[6, 11]], False, [[2, 1, 1, 2, 0, 'horizontal']], []],
               'cloud_map2.tmx': [[[4, 10]], False, [[2, 1, 1, 9, 0, 'vertical']], [], [[21, 2], 2]],
               'cloud_map3.tmx': [[[17, 0]], False, [[2, 1, 1, 23, 0, 'vertical']], []]}, False, False],
    'Fire': [{'endless_map.tmx': [[[11, 11]], False, [[2, 1, 1, 8, 0, 'horizontal'],
                                                      [2, 1, 1, 7, 1, 'vertical'],
                                                      [2, 1, 1, 16, 1, 'vertical'],
                                                      [2, 1, 1, 1, 5, 'vertical'],
                                                      [2, 1, 1, 22, 5, 'vertical']], []]}, False, True],
    'Water': [{'map3.tmx': [[[5, 3]], False, [[2, 1, 1, 8, 0, 'vertical'], [2, 1, 2, 16, 4, 'horizontal']], []],
               'map4.tmx': [[[3, 0]], False, [[2, 1, 1, 6, 6, 'vertical'], [2, 1, 2, 11, 5, 'horizontal']], [],
                            [[22, 8], 1]]
               }, False, False]
}


def show_story():
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    unit_group = pygame.sprite.Group()
    player = MainHero(unit_group, 1600, 880, 0)
    player.direction = 'left'
    index_text = 0
    text = ['Эта история произошла давным\n давно в очень далеком месте...',
            'Молодой ученый по имени Эдвард,\n обнаружил магический плащ,\n способный открывать порталы\n в '
            'различные миры.',
            'Однажды, проведя эксперимент\n с плащом, Эдвард оказывается\n в загадочном мире,\n где математика '
            'является\n ключом ко всему.',
            'Он встречает древнего мудреца,\n который сообщает ему,\n что мир находится под\n угрозой темных сил,'
            '\n которые хотят использовать\n математические знания для\n своих эгоистичных целей.',
            'Для того чтобы спасти мир\n и вернуться домой,\n Эдварду предстоит пройти\n через различные '
            'математические\n испытания и задачи,\n получив ключи и мудрость\n для остановки зла.',
            'Вместе с плащом,\n который дает ему способности\n решать сложные\n математические задачи, '
            'Эдвард\n отправляется в увлекательное\n приключение.']
    counter_fps = 0

    lvl_map = pytmx.load_pygame(f'maps/tower.tmx')
    generate_level(lvl_map, all_sprites, platforms)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                index_text += 1
                if index_text == len(text):
                    return True

        all_sprites.draw(screen)
        unit_group.draw(screen)
        if counter_fps % 8 == 0:
            player.update(None, None, False)
        counter_fps += 1
        if counter_fps == 60:
            counter_fps = 0

        y = 0
        for elem in text[index_text].split('\n'):
            dialog = FONT_25.render(elem, False, (255, 255, 255))
            screen.blit(dialog, (700, y * 50 + 150))
            y += 1
        dialog = FONT_25.render('Нажмите ЛКМ, чтобы продолжить', False, (255, 255, 255))
        screen.blit(dialog, (1380, 1030))
        pygame.display.flip()
        clock.tick(FPS)


def main():
    game_not_over = True
    while game_not_over:

        running = start_screen()
        show_story()
        while running:
            curr_npc = main_page()

            if curr_npc:
                for lvl in LEVELS[curr_npc][0].keys():
                    player_cords = LEVELS[curr_npc][0][lvl][0][0]
                    pos_blocks = LEVELS[curr_npc][0][lvl][2]
                    levels_to_update = LEVELS[curr_npc][0][lvl][3]
                    endless = LEVELS[curr_npc][2]
                    upgrade_pos = None
                    if len(LEVELS[curr_npc][0][lvl]) > 4:
                        upgrade_pos = LEVELS[curr_npc][0][lvl][4]

                    if show_level(lvl, player_cords, pos_blocks, levels_to_update, upgrade_pos,
                                  endless=endless) is True:
                        LEVELS[curr_npc][0][lvl][1] = True
                    else:
                        break
            else:
                running = False

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
