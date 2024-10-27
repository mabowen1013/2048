import pygame
import random
import math




HEIGHT=800
WIDTH=800
GRID_NUM=4
GRID_WIDTH=WIDTH//GRID_NUM
GRID_HEIGHT=HEIGHT//GRID_NUM

BORDER_COLOR=(123,123,123)
MOVE_VEL = 40

pygame.init()

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("2048")


def lost_game_page(window):
    window.fill((169,169,169))
    
    font = pygame.font.Font(None,100)
    button_font = pygame.font.Font(None,50)
    
    text_surface = font.render("You LOSE",True,(255,0,0))
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH//2, HEIGHT//2)
    
    button_text_surface = font.render("PLAY AGAIN",True,(255,255,255))
    button_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2+200, 200,60)
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)    
    
    window.blit(text_surface,text_rect)
    pygame.draw.rect(window, (0,128,0), button_rect)
    window.blit(button_text_surface, button_text_rect)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    tiles = {}
                    main(window)
class Tile:
    COLOR = {
        2:(237,229,218),
        4:(238,225,201),
        8:(243,178,122),
        16:(246,150,101),
        32:(247,124,95),
        64:(247,95,59),
        128:(237,208,115),
        256:(237,204,99),
        512:(236,202,80),
        1024:(123,123,123),
        2048:(123,123,123) 
    }
    
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col*GRID_WIDTH
        self.y = row*GRID_HEIGHT
        
    def get_color(self):
        if self.value not in self.COLOR:
            return (111,111,111)
        return self.COLOR[self.value]
            
    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window,color,(self.x,self.y,GRID_WIDTH,GRID_HEIGHT))
        
        font = pygame.font.Font(None,100)
        text = font.render(str(self.value),1,(111,111,111))
        window.blit(
            text,
            (self.x+GRID_WIDTH/2-text.get_width()/2,
             self.y+GRID_HEIGHT/2-text.get_height()/2))
        
    def move(self, delta):
        self.x+=delta[0]
        self.y+=delta[1]
        
    def set_pos(self, ceil=False):
        if ceil:
            self.row= math.ceil(self.y/GRID_HEIGHT)
            self.col = math.ceil(self.x/GRID_WIDTH)
        else:
            self.row= math.floor(self.y/GRID_HEIGHT)
            self.col = math.floor(self.x/GRID_WIDTH)

def generate_random_tile(tiles):
    random_init_value = random.choice([2,4])
    
    avaliable_spot = {
        "00","01","02","03",
        "10","11","12","13",
        "20","21","22","23",
        "30","31","32","33",
    }
    for cord in tiles.keys():
        avaliable_spot.remove(cord)
    if not avaliable_spot:
        lost_game_page(window)
    random_cord = random.choice(list(avaliable_spot))
    
    new_tile = Tile(random_init_value,int(random_cord[0]),int(random_cord[1]))
    tiles[random_cord] = new_tile
    
def move_grid(window,tiles, clock, direction):
    updated = True
    moved = False
    blocks = set() #记录那些已经merge过的tile，避免出现多次merge的情况
    
    if direction == "left":
        sort_func = lambda x:x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile:tile.col==0
        get_next_tile = lambda tile:tiles.get(f"{tile.row}{tile.col-1}") #寻找当前tile左边的tile，如果没有，就返回none
            
        merge_check = lambda tile,next_tile:tile.x > next_tile.x+MOVE_VEL #如果两个可以merge，当tile移动到啥时候才可以merge
        move_check = lambda tile,next_tile: tile.x > next_tile.x+GRID_WIDTH+MOVE_VEL #如果两个tile不可以merge，那么tile移动到啥时候停止
        
        ceil = True
    elif direction =="right":
        sort_func = lambda x:x.col
        reverse = True
        delta = (MOVE_VEL,0)
        boundary_check = lambda tile:tile.col==3
        get_next_tile = lambda tile:tiles.get(f"{tile.row}{tile.col+1}")
        
        merge_check = lambda tile,next_tile:tile.x < next_tile.x-MOVE_VEL #如果两个可以merge，当tile移动到啥时候才可以merge
        move_check = lambda tile,next_tile: tile.x+GRID_WIDTH+MOVE_VEL < next_tile.x #如果两个tile不可以merge，那么tile移动到啥时候停止

        ceil = False
    
    elif direction =="up":
        sort_func = lambda x:x.row
        reverse = False
        delta = (0,-MOVE_VEL)
        boundary_check = lambda tile:tile.row==0
        get_next_tile = lambda tile:tiles.get(f"{tile.row-1}{tile.col}")
        
        merge_check = lambda tile,next_tile:tile.y > next_tile.y+MOVE_VEL #如果两个可以merge，当tile移动到啥时候才可以merge
        move_check = lambda tile,next_tile: tile.y > next_tile.y+MOVE_VEL+GRID_HEIGHT #如果两个tile不可以merge，那么tile移动到啥时候停止

        ceil = True
        
    elif direction =="down":
        sort_func = lambda x:x.col
        reverse = False
        delta = (0,MOVE_VEL)
        boundary_check = lambda tile:tile.row==3
        get_next_tile = lambda tile:tiles.get(f"{tile.row+1}{tile.col}")
        
        merge_check = lambda tile,next_tile:tile.y < next_tile.y-MOVE_VEL#如果两个可以merge，当tile移动到啥时候才可以merge
        move_check = lambda tile,next_tile: tile.y < next_tile.y-MOVE_VEL-GRID_HEIGHT #如果两个tile不可以merge，那么tile移动到啥时候停止

        ceil = False
    while updated:
        clock.tick(60)
        
        updated = False
        sorted_tiles = sorted(tiles.values(),key=sort_func,reverse=reverse)
        
        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):#如果tile在边角了，不能移动了
                continue#直接跳过
            next_tile = get_next_tile(tile)
            if not next_tile: #如果找不到next tile,并且不在边角，simply移动就好
                tile.move(delta)
                moved = True
            #如果两个tile value相同，并且没有被merge过，说明可以merge
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile,next_tile):#两个tile还没移动到一起
                    tile.move(delta)
                    moved =True
                else:#可以merge了
                    next_tile.value *=2
                    sorted_tiles.pop(i)#删除当前tile
                    blocks.add(next_tile)
                    moved=True
            elif move_check(tile,next_tile):#两个tile数字不相同的move
                tile.move(delta)
                moved=True
            else:
                continue
            tile.set_pos(ceil)
            updated = True
        update_tiles(window,tiles,sorted_tiles)
            
    return end_move(tiles,moved)
    
def end_move(tiles,moved):
    if len(tiles)==16:
        return lost_game_page(window)
    if moved:
        generate_random_tile(tiles)
    return "continue"
    
def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile
        
    
    draw(window,tiles)

def draw_grid(window):
    pygame.draw.rect(window,BORDER_COLOR,(0,0,WIDTH,HEIGHT),10) #border
    
    for row in range(1, GRID_NUM):
        pygame.draw.line(window,BORDER_COLOR,(0,row*GRID_WIDTH),(WIDTH,row*GRID_WIDTH),10)
    
    for col in range(1, GRID_NUM):
        pygame.draw.line(window,BORDER_COLOR,(col*GRID_HEIGHT,0),(col*GRID_HEIGHT,HEIGHT),10)
    
    
def draw(window, tiles):
    window.fill((205,192,180)) #background color
    
    for tile in tiles.values():
        tile.draw(window)
    draw_grid(window)

    pygame.display.update()
    
    
    
def main(window):

    clock = pygame.time.Clock()
    run = True
    
    tiles = {}
    generate_random_tile(tiles)
    generate_random_tile(tiles)
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_grid(window,tiles,clock,"up")
                elif event.key == pygame.K_LEFT:
                    move_grid(window,tiles,clock,"left")
                elif event.key == pygame.K_RIGHT:
                    move_grid(window,tiles,clock,"right")
                elif event.key == pygame.K_DOWN:
                    move_grid(window,tiles,clock,"down")

        draw(window,tiles)
    
if __name__ == "__main__":
    main(window)
    
    
    


    # elif direction == "right":
    #     sort_func = lambda x:x.col
    #     reverse = True
    #     delta = (MOVE_VEL,0)
    #     boundary_check = lambda tile:tile.col==3
    #     get_next_tile = lambda tile:tiles.get(f"{tile.row}{tile.col+1}")
        
    #     merge_check = lambda tile,next_tile: tile.x < next_tile.x+MOVE_VEL
    #     move_check = lambda tile,next_tile:tile.x < next_tile.x+MOVE_VEL+GRID_WIDTH
        
    #     ceil = True
    # elif direction == "up":
    #     sort_func = lambda x:x.row
    #     reverse = False
    #     delta = (0,-MOVE_VEL)
    #     boundary_check = lambda tile:tile.row == 0
    #     get_next_tile = lambda tile:tiles.get(f"{tile.row-1}{tile.col}")
        
    #     merge_check = lambda tile,next_tile:tile.y>next_tile.y+MOVE_VEL
    #     move_check = lambda tile,next_tile:tile.y>next_tile.y+MOVE_VEL+GRID_HEIGHT
        
    #     ceil = False