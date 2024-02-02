import pygame
import sys
import os
from settings import WIDTH, HEIGHT, FONT_25

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 100


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
    screen.fill((100, 200, 250))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_w:
                    return True

        pygame.display.flip()
        clock.tick(FPS)


class MainHero(pygame.sprite.Sprite):

    def __init__(self, group, x, y, name, hp, armor, coins):
        super().__init__(group)
        self.image = load_image("mario.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.hp = hp
        self.armor = armor
        self.coins = coins
        self.speed = 8


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
