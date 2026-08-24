import os
import sys
from tkinter import filedialog
import pygame
from pygame import mixer
import random


"""
"""


def get_image(sheet, frame, width, height, scale, color):

    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)

    return image


pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

pygame.mixer.music.load("sounds\music\song.mp3")
pygame.mixer.music.set_volume(0.05)

pygame.display.set_caption("Blob Master")
screen = pygame.display.set_mode((1280, 720), 0, 32)
clock = pygame.time.Clock()
level = 0
max_level = 1
white = (255, 255, 255)
grid_state = False
loaded = False
clicks = 3

bg = pygame.image.load("images/bg.png")
bg = pygame.transform.scale(bg,(1280,720))
block = 1
start_game = False
game_pause = False
player_state = True
level_complet = False
editor_state = False
color = (252,223,205)
dirt = pygame.image.load("images/dirt.png")
dirt_img = pygame.transform.scale(dirt, (32, 32))
grass = pygame.image.load("images/grass.png")
grass_img = pygame.transform.scale(grass, (32, 32))
plant1 = pygame.image.load("images/plant1.png")
plant1_img = get_image(plant1, 0, 16, 16, 2, color)
plant2 = pygame.image.load("images/plant2.png")
plant2_img = get_image(plant2, 0, 16, 16, 2, color)
plant3 = pygame.image.load("images/plant3.png")
plant3_img = get_image(plant3, 0, 16, 16, 2, color)
lava = pygame.image.load("images/lava.png")
lava_img = get_image(lava, 0, 32, 16, 1, (255,255,255))
door = pygame.image.load("images/door.png")
door_img = pygame.transform.scale(door, (30, 60))
door_min = pygame.transform.scale(door, (15, 30))
cobweb = pygame.image.load("images/cobweb.png")
cobweb.set_colorkey((128, 128, 128))
sprite = pygame.image.load("images/blob.png")
blob_img = [get_image(sprite, i, 16, 16, 2, (245, 155, 20)) for i in range(2)]
blob_i = blob_img[0]
enter_blob_speed = False
enter_blobl_range = False
lava_t = 120
cobweb_t = 30
place_t = 8
break_t = 8

# Player variables

on_ground = False
jumping = False
y_gravity = 1.2
j_height = 16
y_vel = j_height
power = 12
speed = 5
lifes = 3
won = False

font = pygame.font.Font("inne/Minecraft.ttf", 32)
text = font.render(f"x {lifes}", True, white)

start_x = None
start_y = None

end_x = None
end_y = None

life_img = pygame.image.load("images/miniature_head.png")
life_img = pygame.transform.scale(life_img, (48, 48))
life_img.set_colorkey((47, 232, 45))
life_img2 = pygame.transform.scale(life_img, (32, 32))
life_img2.set_colorkey((47, 232, 45))
player_img = pygame.image.load("images/standing.png")
player_img = pygame.transform.scale(player_img, (32, 62))
player_img.set_colorkey((47, 232, 45))
player_rect = player_img.get_rect()
player_x = 0
plyaer_y = 0
player_rect.width = 32
player_rect.height = 64
sprite = pygame.image.load("images/moving2.png")
sprite_left = pygame.image.load("images/moving_left.png")
sprite_jump = pygame.image.load("images/jumping3.png")
colorkey = (47, 232, 45)
won_img = pygame.image.load("images/youwin.png").convert_alpha()
won_img = pygame.transform.scale(won_img, (150, 300))
won_img.set_colorkey((201,205,243))
grid = pygame.image.load("images/buttons/grid_button.png")
grid.set_colorkey((47, 232, 45))


walk_right = [get_image(sprite, i, 16, 32, 2, colorkey) for i in range(8)]
walk_left = [get_image(sprite_left, i, 16, 32, 2, colorkey) for i in range(8)]
jump_frame = [get_image(sprite_jump, i, 16, 32, 2, colorkey) for i in range(8)]
walk_sound = pygame.mixer.Sound("sounds/walk.mp3")
jump_sound = pygame.mixer.Sound("sounds/jumping.mp3")
blob_deth_sound = pygame.mixer.Sound("sounds/blob_sfx.mp3")
player_deth_sound = pygame.mixer.Sound("sounds/death_sound.mp3")
victory_sound = pygame.mixer.Sound("sounds/victory_sound.mp3")
fail_sound = pygame.mixer.Sound("sounds/fail.mp3")
door_sound = pygame.mixer.Sound("sounds/door.mp3")
blob_walking_sound = pygame.mixer.Sound("sounds/blob_walking_sfx.mp3")
lava_bloop_sound = pygame.mixer.Sound("sounds/lava_sfx.mp3")
cobweb_sound = pygame.mixer.Sound("sounds/cobweb.mp3")
block_place_sound = pygame.mixer.Sound("sounds/block_place.wav")
poof_sound = pygame.mixer.Sound("sounds/poof_sound.mp3")


jump_sound.set_volume(0.3)
walk_sound.set_volume(0.1)
blob_deth_sound.set_volume(0.2)
player_deth_sound.set_volume(0.2)
fail_sound.set_volume(0.1)
victory_sound.set_volume(0.2)
door_sound.set_volume(0.1)
blob_walking_sound.set_volume(0.01)
lava_bloop_sound.set_volume(0.3)
cobweb_sound.set_volume(0.1)
block_place_sound.set_volume(0.05)
poof_sound.set_volume(0.05)

cur_right = 0
cur_left = 0
cur_jump = 0
walk_r = 0
walk_l = 0
jump_timer = 0
grass_t = 0
lava_count = 0


def generate_new_level():
    level = []
    row = []
    for i in range (int(720/32)):
        for j in range (int(1280/32)):
            row.append(0)
        level.append(row)
        row = []
    return level
            

def get_file_path():
    data = filedialog.askopenfilename()
    return data


def load_level(leve_path):
    global new_level, loaded
    loaded = False
    test_level(level_path) 
    with open (level_path)as f:
        new_level = [list(line.rstrip().strip("[]").split(",")) for line in f]
    return new_level
     

def play_music():
    global game_pause

    if not game_pause:
        if not pygame.mixer.music.get_busy():
            pygame.mixer_music.play(0,0,200)


def get_max_level():
    global max_level
    for i in range(99):
        if os.path.exists(f"level{i}.txt"):
            max_level = i
        else:
            break
    return max_level


def test_level(level_data):
    global max_level
    with open("level_test.txt", "w") as f:
        for line in level_data:
            text = "[" + ",".join(map(str, line)) + "]"
            f.write(text + "\n")


def save_new_level(filename,level_data):
    global max_level, loaded
    with open(filename, "w") as f:
        for line in level_data:
            text = "[" + ",".join(map(str, line)) + "]"
            f.write(text + "\n")
    if loaded:
        max_level += 1
    get_max_level()


def drawGrid():
    blockSize = 32
    for x in range(0, 1280, blockSize):
        for y in range(32, 720, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, white, rect, 1)


def won_screen():
    global screen, won_img, player_state, level, world, start_game, won
    screen.blit(won_img, (560, 40))
    level = 0
    pygame.mixer_music.pause()
    if reset.draw():
        reset_check()
    elif exit.draw():
        start_game = False
        won = False
        reset_level(level)


def gravity(movement, power):
    global jumping, on_ground
    if jumping == False:
        on_ground = False
        movement[1] += power


def reset_level(level):
    global world_data
    world_data = []
    if os.path.exists(f"level{level}.txt"):
        with open(f"level{level}.txt") as f:
            world_data = [list(line.rstrip().strip("[]").split(",")) for line in f]
    world = World(world_data)

    player_rect.y = plyaer_y
    player_rect.x = player_x
    return world


def restart():

    global player_state, level, world, lifes, won, start_game, game_pause
    if not player_state:
        if lifes == 0:
            fail_sound.play()
            lifes = 3
            level = 0
        
        if reset.draw():
            if lifes == 0:
                level = 0
                lifes = 3
            world = reset_level(level)
            player_rect.y = plyaer_y
            player_rect.x = player_x
            player_state = True
            won = False
        if exit.draw():
            start_game = False
            game_pause = False
            level = 0 
            lifes = 3
            won = False


def reset_check():
    global lifes, level, player_state, game_pause, world, won

    level = 0
    world = reset_level(level)
    player_rect.y = plyaer_y
    player_rect.x = player_x
    player_state = True
    game_pause = False
    won = False
    lifes = 3
    return world


def pause():

    global game_pause, lifes , player_state, level, world, start_game, won

    if game_pause:
        if start.draw():
            game_pause = False
        elif reset.draw():
            reset_check()
        elif exit.draw():
            start_game = False
            game_pause = False
            won = False
            reset_check()


def jump(movement):

    global jumping, y_vel, on_ground, j_height, power, on_cobweb
    if jumping:
        on_ground = False
        update_jump()
        movement[1] -= y_vel
        y_vel -= y_gravity

        if y_vel < -j_height:
            y_vel = j_height
            jumping = False

    else:
        gravity(movement, power)


def test_collision(rect, tiles):

    collision = []
    for tile in tiles:
        if rect.colliderect(tile[1]) and tile[2] != 3:
            collision.append(tile[1])
    return collision


def check_lava_col():

    global player_state, lifes, player_rect, player_img, lava_t, lava_count

    feet_rect = pygame.Rect(player_rect.x, player_rect.bottom, player_rect.width, 2)
    for lava_tile in world.lava_tiles:
        if feet_rect.colliderect(lava_tile):
            lava_count = 1
            if lifes - 1 > 0:
                player_deth_sound.play()
            player_state = False
    lifes -= lava_count
    lava_count = 0

    if lava_t == 0:
        lava_bloop_sound.play()
        lava_t = random.randint(100,500)
    else:
        lava_t -= 1
        

def move(rect, movement, tiles):

    global jumping, on_ground, y_vel, j_height, player_state
    rect.x += movement[0]
    collision = test_collision(rect, tiles)
    for tile in collision:
        if movement[0] > 0:
            rect.right = rect.right
            rect.right = tile.left
        if movement[0] < 0:
            rect.left = rect.left
            rect.left = tile.right

    rect.y += movement[1]
    collision = test_collision(rect, tiles)
    for tile in collision:
        if movement[1] > 0:
            rect.bottom = tile.top
            jumping = False
            on_ground = True
            y_vel = j_height
        if movement[1] < 0:
            rect.top = tile.bottom
            y_vel = 0
            on_ground = False

    return rect


def update_right():
    global cur_right, walk_r

    walk_r += 1
    if walk_r % 4 == 0:
        cur_right += 1
    if cur_right == 8:
        cur_right = 0


def update_left():
    global cur_left, walk_l

    walk_l += 1
    if walk_l % 4 == 0:
        cur_left += 1
    if cur_left == 8:
        cur_left = 0


def update_jump():

    global cur_jump, jump_timer

    jump_timer += 1
    if jump_timer % 8 == 0:
        cur_jump += 1
    if cur_jump == 8:
        cur_jump = 0


def walking_sound():
    global movement, walk_sound, on_ground, grass_t
    if movement[0] != 0 and on_ground == True:
        if grass_t == 0:
            walk_sound.play()
            grass_t = 20


def render():
    global w_r, w_l, j, cur_jump, cur_left, cur_right
    if right:
        w_r = walk_right[cur_right]
        update_right()
        screen.blit(w_r, (player_rect.x, player_rect.y))
    elif left:
        w_l = walk_left[cur_left]
        update_left()
        screen.blit(w_l, (player_rect.x, player_rect.y))
    elif jumping:
        j = jump_frame[cur_jump]
        update_jump()
        screen.blit(j, (player_rect.x, player_rect.y))
    else:
        screen.blit(player_img, (player_rect.x, player_rect.y))


def player_blob_collision(blob, player):
    global player_state, on_ground, jumping, lifes
    current_time = pygame.time.get_ticks()
    blob_rect = blob.rect
    feet_rect = pygame.Rect(player.x, player.bottom, player.width, 12)

    if current_time < blob.col_cd:
        return

    if (feet_rect.colliderect(blob_rect) and player.bottom <= blob_rect.top and not on_ground):
        blob.death()
        blob_deth_sound.play()
        jumping = True
        return

    elif player.colliderect(blob_rect):
        if lifes - 1 > 0:
            player_deth_sound.play()
        lifes -= 1
        player_state = False


def cobweb_coll():
    global player_rect, power, on_ground, jumping, y_gravity, speed, cobweb_t
    on_cobweb = False
    for tile in world.cobweb:
        if player_rect.colliderect(tile):
            on_cobweb = True
            on_ground = True
            jumping = False

    if on_cobweb:
        if cobweb_t == 0:
            cobweb_sound.play()
            cobweb_t = 60
        else:
            cobweb_t -= 1
        
        power = 1
        y_gravity = 1
        speed = 1
    else:
        power = 12
        y_gravity = 1.2
        speed = 5


def door_coll():

    global level, level_complet
    p_rect = pygame.Rect(player_rect.x, player_rect.y, 32, 64)

    for tile in world.doors:
        if p_rect.colliderect(tile):
            if level != max_level:
                door_sound.play()
            level_complet = True
            return level_complet


def blob_update(player):
    for blob in world.blob_list:
        player_blob_collision(blob, player)
        blob.update_l()
        blob.update_r()
        blob.move()
        blob.draw()


def blob_render(level_data):
    for blob in level_data.blob_list:
        blob.update_l()
        blob.update_r()
        blob.move()
        blob.draw()


class World:
    def __init__(self, data):
        global player_x, plyaer_y, editor_state

        self.tiles = []
        self.lava_tiles = []
        self.doors = []
        self.cobweb = []
        self.blob_list = []

        white = (255, 255, 255)
        dirt = pygame.image.load("images/dirt.png")
        dirt_img = pygame.transform.scale(dirt, (32, 32))
        grass = pygame.image.load("images/grass.png")
        grass_img = pygame.transform.scale(grass, (32, 32))
        plant1 = pygame.image.load("images/plant1.png")
        plant1_img = get_image(plant1, 0, 16, 16, 2, color)
        plant2 = pygame.image.load("images/plant2.png")
        plant2_img = get_image(plant2, 0, 16, 16, 2, color)
        plant3 = pygame.image.load("images/plant3.png")
        plant3_img = get_image(plant3, 0, 16, 16, 2, color)
        lava = pygame.image.load("images/lava.png")
        lava_img = get_image(lava, 0, 32, 16, 1, (255,255,255))
        door = pygame.image.load("images/door.png")
        door_img = pygame.transform.scale(door, (30, 60))
        cobweb = pygame.image.load("images/cobweb.png")
        cobweb.set_colorkey((128, 128, 128))
        sprite = pygame.image.load("images/blob.png")
        blob_img = [get_image(sprite, i, 16, 16, 2, (245, 155, 20)) for i in range(2)]
        blob_i = blob_img[0]
        player_img = pygame.image.load("images/standing.png")
        player_img = pygame.transform.scale(player_img, (32, 62))
        player_img.set_colorkey((47, 232, 45))

        row = 0
        for r in data:
            col = 0
            for tile in r:
                if tile == "2":
                    img = grass_img.get_rect()
                    img.x = col * 32
                    img.y = row * 32
                    til = (grass_img, img, 2)
                    self.tiles.append(til)
                if tile == "1":
                    img = dirt_img.get_rect()
                    img.x = col * 32
                    img.y = row * 32
                    til = (dirt_img, img, 1)
                    self.tiles.append(til)
                if tile == "3":
                    img = plant1_img.get_rect()
                    img.x = col * 32
                    img.y = row * 32
                    til = (plant1_img, img, 3)    
                    self.tiles.append(til)
                if tile == "4":
                    img = lava_img.get_rect()
                    img.x = col * 32
                    img.y = row * 32 + 16
                    til = (lava_img, img, 4)
                    self.tiles.append(til)
                    self.lava_tiles.append(img)
                if tile == "5":
                    img = door_img.get_rect()
                    img.x = col * 32
                    img.y = row * 32 + 4
                    til = (door_img, pygame.Rect(img.x, img.y, 0, 0), 5)
                    self.tiles.append(til)
                    self.doors.append(img)
                if tile == "6":
                    img = cobweb.get_rect()
                    img.x = col * 32
                    img.y = row * 32
                    til = (cobweb, pygame.Rect(img.x, img.y, 0, 0), 6)
                    self.tiles.append(til)
                    self.cobweb.append(pygame.Rect(img.x, img.y, 33, 33))
                if tile == '7':
                    plyaer_y = row * 32
                    player_x = col * 32
                    if editor_state:
                        img = plant_img1.get_rect()
                        img.x = col * 32
                        img.y = row * 32
                        til = (player_img1, pygame.Rect(img.x, img.y, 0, 0), 7)
                        self.tiles.append(til)
                if tile != "0":
                    if int(tile) > 10:
                        tilw = tile
                        img = blob_i.get_rect()
                        img.x = col * 32
                        img.y = row * 32 + 8
                        speed = tilw[1]
                        tils = tilw[2]
                        blob = Blob(img.x, img.y, int(tils), int(speed))
                        self.blob_list.append(blob)
                col += 1
            row += 1

    def draw(self):
        for tile in self.tiles:
            screen.blit(tile[0], tile[1])


class Blob:
    def __init__(self, x, y, tiles, speed):
        sprite = pygame.image.load("images/blob.png")
        sprite_left = pygame.image.load("images/blob_left.png")
        self.right = [get_image(sprite, i, 16, 16, 2, (245, 155, 20)) for i in range(2)]
        self.left = [
            get_image(sprite_left, i, 16, 16, 2, (245, 155, 20)) for i in range(2)
        ]
        self.rect = sprite.get_rect()
        self.tiles = tiles
        self.speed = speed
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.cur_r = 0
        self.walk_r = 0
        self.cur_l = 0
        self.walk_l = 0
        self.s_r = self.x
        self.r = True
        self.l = False
        self.col_cd = 0
        self.blob_t = 0
        self.state = True

    def update_r(self):

        self.walk_r += 1

        if self.walk_r % 64 == 0:
            self.cur_r += 1
            self.rect.y = self.y - 2

        if self.cur_r == 2:
            self.cur_r = 0
            self.rect.y = self.y
            self.walk_r = 0

    def update_l(self):

        self.walk_l += 1

        if self.walk_l % 64 == 0:
            self.cur_l += 1
            self.rect.y = self.y

        if self.cur_l == 2:
            self.cur_l = 0
            self.rect.y = self.y - 2
            self.walk_l = 0

    def move(self):

        if self.rect.x >= self.s_r + (self.tiles * 32):
            self.r = False
            self.l = True

        if self.rect.x < self.s_r:
            self.l = False
            self.r = True

        if self.r:
            self.rect.x += self.speed
            if self.state:
                if self.blob_t == 0:
                    blob_walking_sound.play()
                    self.blob_t = 50/self.speed

        elif self.l:
            self.rect.x -= self.speed
            if self.state:
                if self.blob_t == 0:
                    blob_walking_sound.play()
                    self.blob_t = 50/self.speed
        if self.blob_t > 0:
            self.blob_t -= 1

    def death(self):
        self.state = False
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.x = 1000
        self.y = 1000

    def draw(self):

        if self.r:
            wr = self.right[self.cur_r]
            self.update_r()
            screen.blit(wr, (self.rect.x, self.rect.y))
        if self.l:
            wl = self.left[self.cur_l]
            self.update_l()
            screen.blit(wl, (self.rect.x, self.rect.y))


             
# Button variables
start_button = pygame.image.load("images/buttons/start.png")
exit_button = pygame.image.load("images/buttons/exit.png")
restart_button = pygame.image.load("images/buttons/restart.png")
editor_button = pygame.image.load("images/buttons/editor.png")
save_button = pygame.image.load("images/buttons/save.png")
upload_button = pygame.image.load("images/buttons/upload.png")
clear_button = pygame.image.load("images/buttons/clear.png")

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, ((width * scale), (height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.image.set_colorkey((47, 232, 45))

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


if os.path.exists(f"level{level}.txt"):
    with open(f"level{level}.txt") as f:
        world_data = [list(line.rstrip().strip("[]").split(",")) for line in f]
world = World(world_data)
player_rect.y = plyaer_y
player_rect.x = player_x

left = False
right = False


start = Button(450, 180, start_button, 2)
exit = Button(450, 480, exit_button, 2)
reset = Button(450, 330, restart_button, 2)
editor = Button(450, 330, editor_button, 2)
grid_button = Button(1248, 0, grid, 1)
save = Button(450, 330, save_button, 2)
upload = Button(1216, 0, upload_button, 1)
clear = Button(1184,0,clear_button,1)


get_max_level()
level_path = f"level{max_level+1}.txt" 
new_level = generate_new_level()
while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if not game_pause:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    right = True
                if event.key == pygame.K_a:
                    left = True
                if event.key == pygame.K_SPACE:
                    if on_ground:
                        jump_sound.play()
                        jumping = True
                if event.key == pygame.K_p:
                    pygame.mixer.music.fadeout(500)
                if event.key == pygame.K_o:
                    pygame.mixer.music.play(-1,0,500)
                if event.key == pygame.K_ESCAPE:
                    game_pause = True
                    pygame.mixer_music.pause()
                    
                    if won:
                        sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = False
                if event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_w:
                    up = False
                if event.key == pygame.K_s:
                    down = False

        if editor_state:
            won = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    block = 1
                if event.key == pygame.K_2:
                    block = 2
                if event.key == pygame.K_3:
                    block = 4
                if event.key == pygame.K_4:
                    block = 6
                if event.key == pygame.K_5:
                    block = 5
                if event.key == pygame.K_6:
                    block = 3
                if event.key == pygame.K_7:
                    block = 9
                if event.key == pygame.K_8:
                    block = 7
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if block == 9:
                        clicks -= 1
                    
                    
    if not start_game and not editor_state:
        screen.fill((153,217,234))
        #screen.blit(bg,(0,0))
        if start.draw():
            game_pause = False
            start_game = True
            won = False
            player_state = True
        if exit.draw():
            sys.exit()
            pygame.quit()
        if editor.draw():
            editor_state = True

    elif editor_state:
        test_level(new_level)
        reset_level("_test")
        screen.fill((153,217,234))

        with open("level_test.txt") as f:
            world_data = [list(line.rstrip().strip("[]").split(",")) for line in f]

        x, y = pygame.mouse.get_pos()
        left, middle, right = pygame.mouse.get_pressed()
        if not game_pause:
            if left:
                if place_t == 0:
                    block_place_sound.play()
                    place_t = 6
                else:
                    place_t -= 1

                if block == 9:
                    if clicks == 2:
                        start_x = x
                        start_y = y
                    if clicks == 1:
                        end_x = x
                        end_y = y
                    if clicks == 0:
                        block = 710 + abs(int((start_x - end_x)/32)) 
                        new_level[int(start_y / 32)][int(start_x / 32)] = block
                        block = 9
                        clicks = 3
                
                if new_level[int(y / 32)][int(x / 32)] == 0:
                    new_level[int(y / 32)][int(x / 32)] = block
            if right:
                new_level[int(y / 32)][int(x / 32)] = 0
                if break_t == 0:
                    poof_sound.play()
                    break_t = 6
                else:
                    break_t -= 1


        word = World(world_data)

        if upload.draw():
            level_path = get_file_path()
            new_level = load_level(level_path)
            
        if grid_button.draw():
            if grid_state:
                grid_state = False
            else:
                grid_state = True

        if clear.draw():
            new_level = generate_new_level()
            loaded = False

        screen.blit(dirt_img, (0, 0))
        screen.blit(grass_img, (80, 0))
        screen.blit(lava_img, (160, 16))
        screen.blit(cobweb, (240, 0))
        screen.blit(door_min, (320, 0)) 
        screen.blit(plant1_img, (400, 0)) 
        screen.blit(blob_i,(480,0))
        screen.blit(life_img2,(560, 0))

        text1 = font.render("1", True, white)
        text2 = font.render("2", True, white)
        text3 = font.render("3", True, white)
        text4 = font.render("4", True, white)
        text5 = font.render("5", True, white)
        text6 = font.render("6", True, white)
        text7 = font.render("7", True, white)
        text8 = font.render("8", True, white)

        screen.blit(text1, (40, 5))
        screen.blit(text2, (120, 5))
        screen.blit(text3, (200, 5))
        screen.blit(text4, (280, 5))
        screen.blit(text5, (360, 5))
        screen.blit(text6, (440, 5))
        screen.blit(text7, (520, 5))
        screen.blit(text8, (600, 5))

        word.draw()
        blob_render(word)
        if grid_state:
            drawGrid()
        if game_pause:
            if start.draw():
                game_pause = False
            if save.draw():
                save_new_level(level_path,new_level)
                game_pause = False

            if exit.draw():
                editor_state = False
                start_game = False
                game_pause = False
                grid_state = False
                new_level = generate_new_level()
                level_path = f"level{max_level+1}.txt"
                loaded = False
                level = 0
                lifes = 3
                block = 1
                reset_check()
    else:

        if game_pause or not player_state and not editor_state:
            pause()
            restart()

        elif won:
            won_screen()
        elif not game_pause:
            if player_rect.y > 720:
                player_state = False
                lifes -= 1
            text = font.render(f"x {lifes}", True, white)
            if grass_t > 0:
                grass_t -= 1

            screen.fill((153,217,234))
            #screen.blit(bg,(0,0))
            movement = [0, 0]
            
            world.draw()
            screen.blit(life_img, (0, 0))
            screen.blit(text, (64, 15))

            if right:
                if player_rect.x >= 1250:
                    movement[0] += 0
                else:
                    movement[0] += speed

            if left:
                if player_rect.x == -20:
                    movement[0] += 0
                else:
                    movement[0] -= speed

            play_music()
            cobweb_coll()
            jump(movement)
            check_lava_col()
            player = move(player_rect, movement, world.tiles)
            render()
            walking_sound()
            restart()
            door_coll()

            if level_complet:
                if level == max_level:
                    won = True
                    victory_sound.play()
                else:
                    level += 1
                world = reset_level(level)
                level_complet = False

            blob_update(player)
    pygame.display.update()
    clock.tick(60)
