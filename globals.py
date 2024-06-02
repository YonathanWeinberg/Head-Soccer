import pygame
from sys import argv
from os.path import join

# Needed Paths
PROJECT_PATH = "\\".join(argv[0].split("/")[:-1])
IMAGES_PATH = join(PROJECT_PATH, "images")

# Images
INTRO_IMAGE = pygame.image.load(join(IMAGES_PATH, "intro.gif"))
INTRO2_IMAGE = pygame.image.load(join(IMAGES_PATH, "intro2.gif"))
BG_IMAGE = pygame.image.load(join(IMAGES_PATH, "bg.gif"))
LEFT_GOAL_IMAGE = pygame.image.load(join(IMAGES_PATH, "goal2.gif"))
RIGHT_GOAL_IMAGE = pygame.image.load(join(IMAGES_PATH, "goal1.gif"))
BALL_IMAGE = pygame.image.load(join(IMAGES_PATH, "ball.gif"))

LEFT_CHAR_IMAGE = pygame.image.load(join(IMAGES_PATH, "LeftChar.gif"))
LEFT_CHAR_KICK1_IMAGE = pygame.image.load(join(IMAGES_PATH, "LeftChar_kick1.gif"))
LEFT_CHAR_KICK2_IMAGE = pygame.image.load(join(IMAGES_PATH, "LeftChar_kick2.gif"))

RIGHT_CHAR_IMAGE = pygame.image.load(join(IMAGES_PATH, "RightChar.gif"))
RIGHT_CHAR_KICK1_IMAGE = pygame.image.load(join(IMAGES_PATH, "RightChar_kick1.gif"))
RIGHT_CHAR_KICK2_IMAGE = pygame.image.load(join(IMAGES_PATH, "RightChar_kick2.gif"))

# Game Constants
WIDTH, HEIGHT = 1200, 600
PAD_X, PAD_Y = 10, 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Variables
player_moves = []
current_move = []
opponent_moves = []
