import pygame
import random
from constants import*
from tile import Tile
from ui import draw, draw_message

# --- Initialization
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


# --- Helper Functions ---
def get_random_pos(tiles):
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLUMS)
        if f"{row}{col}" not in tiles:
            return row, col

def empty_spaces(tiles):
    return len(tiles) < ROWS * COLUMS

def can_merge(tiles):
    for row in range(ROWS):
        for col in range(COLUMS):
            tile = tiles.get(f"{row}{col}")
            if not tile: continue
            # Checked same number
            for dr, dc in [(0, 1), (1, 0)]:
                next_tile = tiles.get(f"{row + dr}{col + dc}")
                if next_tile and next_tile.value == tile.value:
                    return True
    return False

def end_move(tiles):
    if any(tile.value >= 2048 for tile in tiles.values()):
        return "win"
    
    if empty_spaces(tiles):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
        # Checked game state before random new tile
        if not empty_spaces(tiles) and not can_merge(tiles):
            return "lost"
        return "continue"
    
    if not can_merge(tiles):
        return "lost"
    return "continue"

def update_tiles(window, tiles):
    tiles.clear()
    #Dictionary
    for tile in list(all_tiles_list):
        if tile.value > 0:
            tile.set_pos()
            tiles[f"{tile.row}{tile.col}"] = tile
    draw(window, tiles)

# --- Core Logic ---
def move_tiles(window, tiles, clock, direction):
    global all_tiles_list
    updated = True
    any_move = False
    blocks = set()

    # Moving Left Condition
    if direction == "left":
        sort_func = lambda x: x.col
        reverse, delta, ceil = False, (-MOVE_VEL, 0), True
        boundary_check = lambda t: t.col == 0
        get_next_tile = lambda t: tiles.get(f"{t.row}{t.col - 1}")
        merge_check = lambda t, nt: t.x > nt.x + MOVE_VEL
        move_check = lambda t, nt: t.x > nt.x + RECT_WIDTH + MOVE_VEL
    # Moving Right Condition
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse, delta, ceil = True, (MOVE_VEL, 0), False
        boundary_check = lambda t: t.col == COLUMS - 1
        get_next_tile = lambda t: tiles.get(f"{t.row}{t.col + 1}")
        merge_check = lambda t, nt: t.x < nt.x - MOVE_VEL
        move_check = lambda t, nt: t.x + RECT_WIDTH + MOVE_VEL < nt.x
    # Moving Up Condition
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse, delta, ceil = False, (0, -MOVE_VEL), True
        boundary_check = lambda t: t.row == 0
        get_next_tile = lambda t: tiles.get(f"{t.row - 1}{t.col}")
        merge_check = lambda t, nt: t.y > nt.y + MOVE_VEL
        move_check = lambda t, nt: t.y > nt.y + RECT_HEIGHT + MOVE_VEL
    # Moving Down Condition
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse, delta, ceil = True, (0, MOVE_VEL), False
        boundary_check = lambda t: t.row == ROWS - 1
        get_next_tile = lambda t: tiles.get(f"{t.row + 1}{t.col}")
        merge_check = lambda t, nt: t.y < nt.y - MOVE_VEL
        move_check = lambda t, nt: t.y + RECT_HEIGHT + MOVE_VEL < nt.y

    all_tiles_list = list(tiles.values())

    while updated:
        clock.tick(FPS)
        updated = False
        all_tiles_list.sort(key=sort_func, reverse=reverse)

        for tile in all_tiles_list:
            if tile.value == 0 or boundary_check(tile): continue
            next_tile = get_next_tile(tile)
            
            if not next_tile:
                tile.move(delta)
                updated = any_move = True
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):
                    tile.move(delta)
                    updated = any_move = True
                else:
                    next_tile.value *= 2
                    tile.value = 0
                    blocks.add(next_tile)
                    updated = any_move = True
            elif move_check(tile, next_tile):
                tile.move(delta)
                updated = any_move = True
            
            tile.set_pos(ceil)

        #Update Dictionary
        temp_tiles = {}
        for t in all_tiles_list:
            if t.value > 0:
                t.set_pos(ceil)
                temp_tiles[f"{t.row}{t.col}"] = t
        tiles.clear()
        tiles.update(temp_tiles)

        #Draw and Animation
        draw(window, tiles)
        pygame.display.update()

        pygame.event.pump() 

    if any_move:
        return end_move(tiles)
    return "continue"

def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)
    return tiles

# --- Main Loop ---
def main(window):
    clock = pygame.time.Clock()
    tiles = generate_tiles()
    game_state = "running"
    
    btn_rect = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 + 100, 200, 60)

    while True:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Restart Button Clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state != "running" and btn_rect.collidepoint(event.pos):
                    tiles = generate_tiles()
                    game_state = "running"

            # Keyboard press
            if game_state == "running" and event.type == pygame.KEYDOWN:
                direction = None
                if event.key == pygame.K_LEFT: direction = "left"
                elif event.key == pygame.K_RIGHT: direction = "right"
                elif event.key == pygame.K_UP: direction = "up"
                elif event.key == pygame.K_DOWN: direction = "down"

                if direction:
                    result = move_tiles(window, tiles, clock, direction)
                    if result in ["win", "lost"]:
                        game_state = result

        # --- Draw ---
        draw(window, tiles) 
        
        if game_state != "running":
            message = "You Win!" if game_state == "win" else "Game Over!"
            draw_message(window, message, btn_rect)
            
        pygame.display.update()
        
if __name__ == "__main__":
    main(WINDOW)