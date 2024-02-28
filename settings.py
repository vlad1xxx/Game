import pygame
from screeninfo import get_monitors

pygame.init()

FONT_25 = pygame.font.Font('fonts/PixelCode.ttf', 25)
WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height
TILE_SIZE = 80
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

