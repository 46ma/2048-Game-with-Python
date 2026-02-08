import pygame
pygame.init()

# --- Configuration ---
FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS, COLUMS = 4, 4
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLUMS

# --- Colors ---
OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)
BUTTON_COLOR = (143, 122, 102)
BUTTON_HOVER_COLOR = (180, 150, 120)
BUTTON_TEXT_COLOR = (255, 255, 255)

# --- Font ---
FONT = pygame.font.SysFont("comicsansms", 60, bold=True)

# --- Game Rule ---
MOVE_VEL = 20 # For moving tiles