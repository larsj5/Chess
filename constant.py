import pygame
from pygame.locals import *

pygame.init()

# dimensions
WINDOW_WIDTH = 900
WIDTH, HEIGHT = 750, 750
ROWS, COLS = 8, 8
SQUARE_SIZE = (WIDTH-100)//COLS
MARGIN = (WINDOW_WIDTH - WIDTH) / 2

# pixel width and height of sprite.png
IMG_WIDTH = int(450 / 6)
IMG_HEIGHT = int(150 / 2)
UNQ_PIECES = 6

# colors
BG_COLOR = (80, 80, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
LIGHT_RED = (200, 10, 10)
GREEN = (0, 150, 0)
LIGHT_GREEN = (10, 255, 10)
BLUE = (102, 178, 255)
PURPLE = (50, 0, 150)
LIGHT_PURPLE = (100, 0, 200)
DARK_BROWN = (110, 70, 30)
LIGHT_BROWN = (190, 140, 60)
SELECTED_DARK_BROWN = (200, 100, 60)
SELECTED_LIGHT_BROWN = (210, 140, 60)
# fonts
MAIN_FONT = pygame.font.SysFont('arial', 50)
SUB_FONT = pygame.font.SysFont('arial', 30)
SUB_FONT2 = pygame.font.SysFont('arial', 20)
BUTTON_FONT = pygame.font.SysFont('arial', 20)
HELP_FONT = pygame.font.SysFont('arial', 15)

# number of pieces for each class
NUM_PAWNS = 8
NUM_KING = 1
NUM_QUEEN = 1
NUM_ROOKS = 2
NUM_BISHOPS = 2
NUM_KNIGHTS = 2
