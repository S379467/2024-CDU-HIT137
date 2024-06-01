"""PART 2: Side scrolling shooter game with Tanks"""
#TESSA SURENDONK [S379467]

import pygame
from pygame import mixer
import os
import random
import csv

mixer.init()
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HIT137 Side Scroller Shooter")

#set framerate
start = pygame.time.get_ticks()
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
SCALE = 2
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TITLE_TYPES = 21
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
good_bombs_pickup = False
good_bombs_counter = 0
score = 0


#define player action variables
moving_left = False
moving_right = False
shoot = False

#load music
pygame.mixer.music.load("music/level_music.mp3")
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1, 0.0, 5000)
shot_fx = pygame.mixer.Sound("music/laser.mp3")
shot_fx.set_volume(0.6)
explosion_fx = pygame.mixer.Sound("music/explosion.mp3")
explosion_fx.set_volume(0.3)

#button images
start_img = pygame.image.load("img/start_btn.png").convert_alpha()
exit_img = pygame.image.load("img/exit_btn.png").convert_alpha()
restart_img = pygame.image.load("img/restart_btn.png").convert_alpha()
#load background
pine1_img = pygame.image.load("img/background/pine1.png").convert_alpha()
pine2_img = pygame.image.load("img/background/pine2.png").convert_alpha()
mountain_img = pygame.image.load("img/background/mountain.png").convert_alpha()
sky_img = pygame.image.load("img/background/sky_cloud.png").convert_alpha()
#store tiles in a list
img_list = []
for x in range(TITLE_TYPES):
    img = pygame.image.load(f"img/Tile/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
#load images
bullet_img = pygame.image.load("img/bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (int(bullet_img.get_width() * SCALE), int(bullet_img.get_height() * SCALE)))
good_bombs_img = pygame.image.load("img/items/good_bombs.png").convert_alpha()
good_bombs_img = pygame.transform.scale(good_bombs_img, (int(good_bombs_img.get_width() * SCALE), int(good_bombs_img.get_height() * SCALE)))
health_box_img = pygame.image.load("img/items/health_box.png").convert_alpha()
health_box_img = pygame.transform.scale(health_box_img, (int(health_box_img.get_width() * SCALE), int(health_box_img.get_height() * SCALE)))
shoot_speed_img = pygame.image.load("img/items/shoot_speed.png").convert_alpha()
shoot_speed_img = pygame.transform.scale(shoot_speed_img, (int(shoot_speed_img.get_width() * SCALE), int(shoot_speed_img.get_height() * SCALE)))

item_boxes = {
    "Health"        : health_box_img,
    "Good_Bombs"    : good_bombs_img, 
    "Shot_Speed"    : shoot_speed_img }


#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)


#define font
font = pygame.font.SysFont("Futura", 30)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))



def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    bomb_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

class Tank(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed, scale=SCALE, enemy_type=0, health=100):
        pygame.sprite.Sprite.__init__(self)     #calls upon parent class built into pygame import
        self.alive = True
        self.char_type = char_type
        if enemy_type == 1:
            self.speed = speed + 3
        else:
            self.speed = speed
        self.shoot_cooldown = 0
        self.health = health
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.shoot_timing = 25
        #enemy specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,150,20)
        self.idling = False
        self.idling_counter = 0
        self.enemy_type = enemy_type



        #load all images for player
        animation_types = ["IdleORJump", "Run", "Death"]
        for animation in animation_types:
            #reset temp list of images
            temp_list = []
            num_of_frames = len(os.listdir(f"img/{self.char_type}_{enemy_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"img/{self.char_type}_{enemy_type}/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  
        self.width = self.image.get_width()      
        self.height = self.image.get_height() 

    def update(self):
        self.update_animation()
        self.check_alive()
        #update bullet cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        #reset movement variables
        screen_scroll = 0
        dx = 0 
        dy = 0
    
        #assign movent variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump and apply gravity
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #collision check
        for tile in world.obstacle_list:
            if tile [1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #if ai has hit a wall turn around
                if self.char_type == "enemy":
                    self.direction *= -1
                    self.move_counter = 0
            if tile [1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                #check if hit head or falling
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        #falling in water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        #touching exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        #falling off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0



        #check for edge of the screen
        if self.char_type == "player":
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                 dx = 0            

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update screen scroll based on player postion
        if self.char_type == "player":
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete


    def shoot(self):

        if self.shoot_cooldown == 0:
            if self.shoot_timing > 25:
                self.shoot_timing -= 1
                self.shoot_cooldown = 2
                bullet = Bullet(self.rect.centerx + (0.7 * self.rect.size[0] * self.direction), (self.rect.centery - 15), self.direction)
                bullet_group.add(bullet)
                shot_fx.play()
            else:
                self.shoot_cooldown = 25
                bullet = Bullet(self.rect.centerx + (0.7 * self.rect.size[0] * self.direction), (self.rect.centery - 15), self.direction)
                bullet_group.add(bullet)
                shot_fx.play()



    def ai(self):
        if self.alive and player.alive:
            if self.rect.colliderect(player.rect):
                player.health -= 1
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
        #check if the ai in near the player
            if self.vision.colliderect(player.rect):
        #stop running and face the player
                if self.enemy_type != 1:
                    self.update_action(0)#0: idle
                    self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    #ai vision
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                if self.move_counter > TILE_SIZE:
                    self.direction *= -1
                    self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

		#scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 500
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        global score
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)
            if self.health == 0 and self.char_type == "enemy":
                if self.enemy_type == 0:
                    score += 50
                elif self.enemy_type == 1:
                    score += 25
                elif self.enemy_type == 2:
                    score += 10000
            elif self.health == 0 and self.char_type == "player":
                score = 0


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
       



class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8 or tile == 12:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)                    
                    elif tile >= 11 and tile <= 14 and tile != 12:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)

                    elif tile == 15: #player location
                        player = Tank("player", x * TILE_SIZE, y * TILE_SIZE, 6, health=150)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16: #enemy creation and location
                        if level != 3:
                            enemy = Tank("enemy_soldier", x * TILE_SIZE, y * TILE_SIZE, 2, enemy_type=random.randint(0,1))
                            enemy_group.add(enemy)
                        else: #NOTE: NEED TO CHANGE
                            enemy = Tank("enemy_soldier", x * TILE_SIZE, y * TILE_SIZE, 2, scale=6, enemy_type=2, health=1000)
                            enemy_group.add(enemy)

                    elif tile == 17: #create Shot speed
                        item_box = ItemBox("Shot_Speed", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18: #create Good Bombs
                        item_box = ItemBox("Good_Bombs", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19: #create HEalth Box
                        item_box = ItemBox("Health", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    
                    elif tile == 20:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
        return player, health_bar
    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])



class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

        self.vel_y = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.rect.x += screen_scroll
        global good_bombs_pickup
        global good_bombs_counter
        #check for collision
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == "Health":
                player.health += 100
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Shot_Speed":
                player.shoot_timing = 175
            elif self.item_type == "Good_Bombs":
                good_bombs_counter = 400
                good_bombs_pickup = True
            self.kill()
        if level == 3:
            self.vel_y += GRAVITY/2
            dy = self.vel_y

            #collision detection
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.speed = 0
                    if self.vel_y >= 0:
                        self.vel_y = 0
                        dy = tile[1].top - self.rect.bottom
            self.rect.y += dy




class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #update with current health
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x -2, self.y -2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #move bullet and check if offscreen
        self.rect.x += (self.direction * self.speed) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            global score
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()
                    if enemy.health == 0:
                        if enemy.enemy_type == 0:
                            score += 50
                        elif enemy.enemy_type == 1:
                            score += 25
                        elif enemy.enemy_type == 2:
                            score += 10000


class Bomb(pygame.sprite.Sprite):
    def __init__(self, bomb_type, x, y=-10):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = 0
        self.type = bomb_type
        bomb_img = pygame.image.load(f"img/bomb{bomb_type}.png").convert_alpha()
        self.image = pygame.transform.scale(bomb_img, (int(bomb_img.get_width() * SCALE), int(bomb_img.get_height() * SCALE)))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.vel_y += GRAVITY/2
        dy = self.vel_y

        #collision detection
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
        self.rect.x += screen_scroll
        self.rect.y += dy


        #countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.type, self.rect.x, self.rect.y, 2)
            explosion_group.add(explosion)
            #do damage to player
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 25
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50



class Explosion(pygame.sprite.Sprite):
    def __init__(self,type, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 8):
            img = pygame.image.load(f"img/explosion/bomb{type}/{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll

        EXPLOSION_SPEED = 5
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else: self.image = self.images[self.frame_index]



#create buttons
start_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group() #steals properties of pygames inbuilt Group class
bomb_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()







#Load in level data
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
with open(f"level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)


player_win = False
run = True
while run:


    clock.tick(FPS)
    now = pygame.time.get_ticks()

    if start_game == False:
        #main menu 
        screen.fill(BG)
        if exit_button.draw(screen):
            run = False
        if player_win:
            draw_text("YOU'RE A WINNER!", pygame.font.SysFont("Futura", 125), (255,255,255), 10, 35)
        else:
            if start_button.draw(screen):
                start_game = True
                player_win = False

    else:
        #update background
        draw_bg()
        #draw world map
        world.draw()

        #show health
        health_bar.draw(player.health)
        draw_text(f'SCORE: {score}', font, (255,255,255), 10, 35)


        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        #update and draw groups
        bullet_group.update()
        bomb_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()

        bullet_group.draw(screen)
        bomb_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        #random bomb generation
        if good_bombs_pickup == True:
            if good_bombs_counter > 0:
                good_bombs_counter -= 1
                if now - start > random.randint(200, 1000):
                    start = now
                    bomb = Bomb(random.randint(0,1),random.randint(0, SCREEN_WIDTH))
                    bomb_group.add(bomb)
        else:
            if now - start > random.randint(2000, 10000):
                start = now
                bomb = Bomb(random.randint(0,1),random.randint(0, SCREEN_WIDTH))
                bomb_group.add(bomb)

        if level == 3:
            if now - start > random.randint(200, 1000):
                holding_number = random.randint(1, 100)
                start = now
                if holding_number >= 80 and holding_number <= 100:
                    bomb = Bomb(random.randint(0,1),random.randint(0, SCREEN_WIDTH))
                    bomb_group.add(bomb)       
                elif holding_number >= 40 and holding_number <= 60:
                    enemy = Tank("enemy_soldier", random.randint(0, SCREEN_WIDTH), 0, 2, enemy_type=random.randint(0,1))
                    enemy_group.add(enemy)
                elif holding_number == 17:
                    item_box = ItemBox("Shot_Speed", random.randint(0, SCREEN_WIDTH), 0)
                    item_box_group.add(item_box)
                    print("box 17")
                elif holding_number == 18:
                    item_box = ItemBox("Good_Bombs", random.randint(0, SCREEN_WIDTH), 0)
                    item_box_group.add(item_box)
                    print("box 18")
                elif holding_number == 19:
                    item_box = ItemBox("Health", random.randint(0, SCREEN_WIDTH), 0)
                    item_box_group.add(item_box)
   


        #update player acitons
        if player.alive:
            #shoot bullets
            if shoot:
                player.shoot()
            if player.in_air:
                player.update_action(0) #shares same animation as idle
            elif moving_left or moving_right:
                player.update_action(1) #run in 1 index position
            else:
                player.update_action(0) #idle in 0 index position
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            #check if level completed
            if level_complete:
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    with open(f"level{level}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)                    
        else:
            screen_scroll = 0
            if restart_button.draw(screen):
                bg_scroll = 0
                world_data = reset_level()
                with open(f"level{level}_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    if score >= 10000: 
        start_game = False
        player_win = True


    pygame.display.update()


pygame.quit()

"""
BIBLIOGRAPHY
Coding With Russ. (2021, March 7). PyGame Scrolling Shooter Game Beginner Tutorial in Python - Playlist Part 1 to 13.
    YouTube. https://www.youtube.com/watch?v=DHgj5jhMJKg&list=PLjcN1EyupaQm20hlUE11y9y8EY2aXLpnv
"""