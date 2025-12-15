import pygame
import random
import math

pygame.init()

#Framerate
FPS = 60

#Gamescreen
WIDTH, HEIGHT = 800,800

#tile and grid
ROWS = 4
COLUMS = 4
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLUMS

#Outline
OUTLINE_COLOR = (187,173,160)
OUTLINE_THICKNESS = 10

#Background
BACKGROUND_COLOR = (205,192,180)
FONT_COLOR =  (119,110,101)

# Button Colors
BUTTON_COLOR = (143, 122, 102)
BUTTON_HOVER_COLOR = (180, 150, 120)
BUTTON_TEXT_COLOR = (255, 255, 255)

#Move numbers
FONT = pygame.font.SysFont("comicsansms",60,bold=True)
MOVE_VEL = 20

#Set Gamescreen
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("2048") #Game name

#Class crate tile
class Tile:
    COLORS = [
        (237,229,218),
        (238,225,201),
        (243,178,122),
        (246,150,101),
        (247,124,95),
        (247,95,59),
        (237,208,115),
        (237,204,99),
        (236,202,80),
    ]

    def __init__(self,value ,row,col):
        self.value = value #Number on tile
        self.row = row #Rowl 0-3
        self.col = col #Colums 0-3
        self.x = col * RECT_WIDTH #X position (Horizontal)
        self.y = row * RECT_HEIGHT #Y Position (Vertical)

    def get_color(self):
        color_index = int(math.log2(self.value)) -1
        color = self.COLORS[color_index]
        return color

    def draw(self,window):
        color = self.get_color()
        pygame.draw.rect(window,color,(self.x,self.y,RECT_WIDTH,RECT_HEIGHT))

        text = FONT.render(str(self.value),1,FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH/2 - text.get_width()/2),
                self.y + (RECT_HEIGHT/2 - text.get_height()/2),
            ),
        )

    def set_pos(self,celi=False):
        if celi:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x/RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self,delta):
        self.x += delta[0]
        self.y += delta[1]
            
#Win and lost condition
def end_move(tiles):
    #Win condition
    for tile in tiles.values():
        if tile.value >= 2048:
            return "win"
        
    #Lost condition
    if not empty_spaces(tiles) and not can_merge(tiles):
        return "lost"
    
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

#Empty spaces check
def empty_spaces(tiles):
    return len(tiles) < ROWS * COLUMS

#Merge Check
def can_merge(tiles):
    #Check if tiles can merge
    for row in range(ROWS):
        for col in range(COLUMS):
            key = f"{row}{col}"
            tile = tiles.get(key)
            if not tile:
                continue

            #Right check
            right_tile = tiles.get(f"{row}{col + 1}")
            if right_tile and tile.value == right_tile.value:
                return True
            
            #Down check
            down_tile = tiles.get(f"{row + 1}{col}")
            if down_tile and tile.value == down_tile.value:
                return True
            
#Draw message and button
def draw_message(window,message,button_rect):
    #Back ground foe message
    overlay = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
    overlay.fill((0,0,0,150))
    window.blit(overlay,(0,0))
    
    #Show message
    GAME_FONT = pygame.font.SysFont("comicsansms", 80 , bold=True)
    text = GAME_FONT.render(message,1,BUTTON_TEXT_COLOR)

    #Center alignment
    text_x = WIDTH/2 - text.get_width()/2
    text_y = HEIGHT/2 - text.get_height()/ 2 -50

    window.blit(text,(text_x,text_y))

    #Show button
    mouse_pos = pygame.mouse.get_pos()
    #Hover
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    #Draw button
    pygame.draw.rect(window,color,button_rect,0,10)
    #Show text button
    BUTTON_FONT = pygame.font.SysFont("comicsansms",40,bold=True)
    button_text = BUTTON_FONT.render("Play Again",1,BUTTON_TEXT_COLOR)
    #Center alignment
    button_text_x = button_rect.x + (button_rect.width/2 - button_text.get_width()/2)
    button_text_y = button_rect.y + (button_rect.height/2 - button_text.get_height()/2)
    window.blit(button_text, (button_text_x , button_text_y))

    pygame.display.update()

#Draw grid
def draw_grid(window):
    #Draw Horizontal lines
    for row in range(1,ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window,OUTLINE_COLOR,(0,y),(WIDTH,y),OUTLINE_THICKNESS)

    #Draw Vertical lines
    for colums in range(1,COLUMS):
        x = colums * RECT_WIDTH
        pygame.draw.line(window,OUTLINE_COLOR,(x,0),(x,HEIGHT),OUTLINE_THICKNESS)

    #Outline
    pygame.draw.rect(window,OUTLINE_COLOR,(0,0,WIDTH,HEIGHT),OUTLINE_THICKNESS)

#Draw in game
def draw(window,tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)


    draw_grid(window)

    pygame.display.update()

#Random tiles
def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0,ROWS)
        col = random.randrange(0,COLUMS)

        if f"{row}{col}" not in tiles:
            break
    
    return row,col

#Moving tiles
def move_tiles(window,tiles,clock,direction):
    updated = True
    blocks = set()

    #Moving Left
    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL,0)
        boundary_check =  lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = (
            lambda tile , next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        )
        ceil = True

    #Moving Right
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL,0)
        boundary_check =  lambda tile: tile.col == COLUMS-1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile , next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False

    #Moving up
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0,-MOVE_VEL)
        boundary_check =  lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile , next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True

    #Moving Down
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0,MOVE_VEL)
        boundary_check =  lambda tile: tile.row == ROWS -1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile , next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        )
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        #blocks = set()
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    #tile.value = 0
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
                    updated = True
                        
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window,tiles,sorted_tiles)

    return end_move(tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "lost"
    
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2,4]),row,col)
    return "continue"


def update_tiles(window,tiles,sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        if tile.value > 0:
            tiles[f"{tile.row}{tile.col}"] = tile

    draw(window,tiles)

#Generate tiles
def generate_tiles():
    tiles = {}
    for i in range(2):
        row , col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2,row,col)

    return tiles

#Crate Game loop
def main(window):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()
    game_state = "running"

    #Button's size and position
    BUTTON_WIDTH , BUTTON_HEIGHT = 200,60
    BUTTON_X = WIDTH / 2 - BUTTON_WIDTH / 2
    BUTTON_Y = HEIGHT / 2 + 150
    restart_button_rect = pygame.Rect(BUTTON_X,BUTTON_Y,BUTTON_WIDTH,BUTTON_HEIGHT)  
    
    #Main loop
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #Restart Button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state != "running" and restart_button_rect.collidepoint(event.pos):
                    tiles = generate_tiles()
                    game_state = "running"
                    continue
                
            #Game state "runnig"
            if game_state == "running":
                if event.type == pygame.KEYDOWN: #Key press
                    direction = None

                    #Left arrow
                    if event.key == pygame.K_LEFT:
                        direction = "left"
                    #Righr arrow
                    elif event.key == pygame.K_RIGHT:
                        direction = "right"
                    #Up arrow
                    elif event.key == pygame.K_UP:
                        direction = "up"
                    #Down arrow
                    elif event.key == pygame.K_DOWN:
                        direction = "down"

                    if direction:
                        result = move_tiles(window,tiles,clock,direction)

                        if result in ["lost","win"]:
                            game_state = result
            
        draw(window,tiles)

        # "Game over / You win" Screen
        if game_state != "running":
            message = "Game Over" if game_state == "lost" else "You Win"
            draw_message(window,message,restart_button_rect)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)