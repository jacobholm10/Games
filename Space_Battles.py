import pygame
import time
import os
import random

#Font
pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 50)
GAME_FONT = pygame.font.SysFont("comicsans", 100)

#Dimensions
WIDTH, HEIGHT = 1000, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battles")
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 100

#Images
SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets2", "spaceship_yellow.png"))
SPACESHIP = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
ENEMY_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets2", "spaceship_red.png"))
ENEMY_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(ENEMY_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets2", "space_battles_background.png")), (WIDTH, HEIGHT))

BLUE_LASER = pygame.image.load(os.path.join("assets2", "blue_laser.png"))
RED_LASER = pygame.image.load(os.path.join("assets2", "red_laser.png"))

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
BLACK = (0, 0, 0)

#Movement variables
player_vel = 5




class Character:
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_count = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        
    def cool_down(self):
        if self.cooldown_count >= self.COOLDOWN:
            self.cooldown_count = 0
        elif self.cooldown_count > 0:
            self.cooldown_count += 1
    
    def move_lasers(self, vel, obj):
        self.cool_down()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
        
    
    def shoot(self):
        if self.cooldown_count == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_count = 1



    def get_height(self):
        return self.ship_img.get_height()
    
    def get_width(self):
        return self.ship_img.get_width()

class Player(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = SPACESHIP
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    
    def draw(self, window):
        super().draw(window)
        self.health_bar(window)
    
    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x - 20, self.y, 10, self.ship_img.get_height()))
        pygame.draw.rect(window, (0, 255, 0), (self.x - 20, self.y, 10, self.ship_img.get_height() * (self.health/self.max_health)))


class Enemy(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = ENEMY_SPACESHIP
        self.laser_img = RED_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    
    def draw(self, window):
        super().draw(window)
        self.health_bar(window)
    
    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x + self.ship_img.get_width() + 10, self.y, 10, self.ship_img.get_height()))
        pygame.draw.rect(window, (0, 255, 0), (self.x + self.ship_img.get_width() + 10, self.y, 10, self.ship_img.get_height() * (self.health/self.max_health)))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def move(self, vel):
        self.x += vel
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def off_screen(self, width):
        return self.x <= 0 and self.x >= width

    def collision(self, obj):
        return collide(self, obj)



def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def player_movement(keys, player):
    if keys[pygame.K_w] and player.y - player_vel > 0:
        player.y -= player_vel
    if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:
        player.y += player_vel
    if keys[pygame.K_a] and player.x - player_vel > 0:
        player.x -= player_vel
    if keys[pygame.K_d] and player.x + player_vel + player.get_width() < BORDER.x:
        player.x += player_vel
    if keys[pygame.K_SPACE]:
        player.shoot()

    
    



def draw_window(player, enemy, lost, won):
    WINDOW.blit(BG, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    player.draw(WINDOW)
    enemy.draw(WINDOW)


    if lost:
        lost_text = GAME_FONT.render("You Lost!!", 1, (255, 255, 255))
        WINDOW.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, 350))
    
    if won:
        won_text = GAME_FONT.render("You Won!!", 1, (255, 255, 255))
        WINDOW.blit(won_text, (WIDTH/2 - won_text.get_width()/2, 350))

    pygame.display.update()


def main():
    FPS = 60
    lost = False
    won = False
    won_count = 0
    lost_count = 0
    clock = pygame.time.Clock()
    running = True
    enemy_vel_x = 4
    enemy_vel_y = 5
    player_laser_vel = 12
    enemy_laser_vel = 15
    


    #Player
    player = Player(200, 400)
    #Enemy
    enemy = Enemy(800, 400)

    while running:
        clock.tick(FPS)
        draw_window(player, enemy, lost, won)

        #Player Health
        if player.health <= 0:
            lost = True
            lost_count += 1

        #Lost
        if lost:
            if lost_count > FPS * 3:
                running = False
            else:
                continue

        
        #Enemy Health
        if enemy.health <= 0:
            won = True
            won_count += 1
        
        #Won
        if won:
            if won_count > FPS * 3:
                running = False
            else:
                continue
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()

        #Player Movement
        player_movement(keys, player)

        #Enemy Random Movement
        if enemy.x < BORDER.x + BORDER.width + 20 or enemy.x > WIDTH - 150 or random.random() < 0.05:
            enemy_vel_x = random.randint(2,8) * (-1 if enemy_vel_x > 0 else 1)
            enemy_vel_y = random.randint(-8, 8)

            if enemy_vel_x == 0 and enemy_vel_y == 0:
                enemy_vel_x = random.randint(2,8) * (-1 if enemy_vel_x > 0 else 1)
                enemy_vel_y = random.randint(-8, 8)
        
        if enemy.y < 50 or enemy.y > HEIGHT - 150 or random.random() < 0.05:
            enemy_vel_y *= -1

            if enemy_vel_x == 0 and enemy_vel_y == 0:
                enemy_vel_x = random.randint(2,8) * (-1 if enemy_vel_x > 0 else 1)
                enemy_vel_y = random.randint(-8, 8)


        
        enemy.x += enemy_vel_x
        enemy.y += enemy_vel_y




        if enemy:
            enemy.move_lasers(-enemy_laser_vel, player)
            if random.randrange(0, 120) == 1:
                enemy.shoot()
        
        player.move_lasers(player_laser_vel, enemy)


def main_menu():
     home_font = pygame.font.SysFont("comicsans", 60)
     running = True
     while running:
          WINDOW.blit(BG, (0, 0))
          title_label = home_font.render("Press the mouse to begin...", 1, (255, 255, 255))
          WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
          pygame.display.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
               if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
     
     pygame.quit()

main_menu()
    






