import pygame
import sys
from settings import WIDTH, HEIGHT, FONT_TEXT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class MainHero:
    def __init__(self, x, y, name, hp, armor):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.armor = armor


class NPC:
    def __init__(self, x, y, name, dialogue):
        self.x = x
        self.y = y
        self.name = name
        self.dialogue = dialogue
        # self.dialogue_shown = False  # Флаг для отслеживания показа диалога


def is_near_npc(player, npc):
    distance = ((player.x - npc.x) ** 2 + (player.y - npc.y) ** 2) ** 0.5
    return distance < 75


def render_use():
    text = FONT_TEXT.render('Нажмите "Space", чтобы взаимодействовать', True, (0, 0, 0))
    screen.blit(text, (WIDTH - 400, 5))


def render_dialog(near_npc):
    dialog = FONT_TEXT.render(near_npc.dialogue, True, (0, 0, 0))
    screen.blit(dialog, (near_npc.x + 50, near_npc.y - 50))


def main():
    player = pygame.Rect(100, 100, 30, 30)
    bg = pygame.image.load('images/sand.bmp')
    npcs = [
        NPC(200, 200, "Bob", "Hello, traveler!"),
        NPC(262, 706, "Alice", "Nice to meet you!"),
        NPC(1588, 166, "Charlie", "How can I help you?"),
        NPC(1084, 724, "bomboblud", "Hello")
    ]  # Список NPC

    clock = pygame.time.Clock()
    running = True
    near_npc = None
    press_space = False

    while running:

        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Перемещение игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= 6
        if keys[pygame.K_RIGHT] and player.x + 30 < WIDTH:
            player.x += 6
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= 6
        if keys[pygame.K_DOWN] and player.y + 30 < HEIGHT:
            player.y += 6

        # Создание Игрока
        pygame.draw.rect(screen, (255, 0, 0), player)

        # Cоздание NPC
        for npc in npcs:
            pygame.draw.circle(screen, (0, 0, 255), (npc.x, npc.y), 20)

        # Находит ближайшено NPC
        for npc in npcs:
            if is_near_npc(player, npc):
                near_npc = npc
                break
            else:
                near_npc = None

        if near_npc is not None and keys[pygame.K_e]:  # Начало уровня
            pass
        # TODO: при нажатии открывается новый уровень
        elif near_npc is not None:  # Открывает диалог с NPC
            render_use()
            render_dialog(near_npc)
        pygame.display.flip()
        clock.tick(100)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
