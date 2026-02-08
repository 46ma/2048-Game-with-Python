import pygame
import math
from constants import *

class Tile:
    COLORS = [
        (237, 229, 218), (238, 225, 201), (243, 178, 122),
        (246, 150, 101), (247, 124, 95), (247, 95, 59),
        (237, 208, 115), (237, 204, 99), (236, 202, 80),
        (236, 196, 63), (236, 193, 46)
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        if color_index < len(self.COLORS):
            return self.COLORS[color_index]
        return self.COLORS[-1]

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))
        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(text, (self.x + (RECT_WIDTH/2 - text.get_width()/2),
                           self.y + (RECT_HEIGHT/2 - text.get_height()/2)))

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]