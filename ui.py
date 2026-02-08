import pygame
from constants import*

# --- Drawing Functions ---
def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
    for col in range(1, COLUMS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)
    for tile in tiles.values():
        tile.draw(window)
    draw_grid(window)

def draw_message(window, message, button_rect):
    # Black Overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    window.blit(overlay, (0, 0))
    
    # Text
    GAME_FONT = pygame.font.SysFont("comicsansms", 80, bold=True)
    text = GAME_FONT.render(message, 1, BUTTON_TEXT_COLOR)
    window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2 - 50))

    # Button
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(window, color, button_rect, 0, 10)
    
    BUTTON_FONT = pygame.font.SysFont("comicsansms", 40, bold=True)
    btn_text = BUTTON_FONT.render("Play Again", 1, BUTTON_TEXT_COLOR)
    window.blit(btn_text, (button_rect.x + (button_rect.width/2 - btn_text.get_width()/2),
                           button_rect.y + (button_rect.height/2 - btn_text.get_height()/2)))