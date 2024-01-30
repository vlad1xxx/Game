from screeninfo import get_monitors
import pygame

pygame.init()

WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height
FONT_25 = pygame.font.Font(None, 25)