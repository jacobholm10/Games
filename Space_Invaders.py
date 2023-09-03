import pygame
import os
import time
import random
pygame.font.init()

FONT = pygame.font.SysFont("comicsans", 30)
lost_font = pygame.font.SysFont("comicsans", 50)

#Game Window
WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter")

#Aliens
SPACE_ALIENS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "1163.png")), (40, 40))

#Spaceship
SPACESHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#Lasers
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_background.jpg")), (WIDTH, HEIGHT))

FPS = 60
VEL = 4
          
     


class Character:
     COOLDOWN = 30

     def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_countdown = 0

    
     def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
             laser.draw(window)
     
     def move_lasers(self, vel, obj):
          self.cool_down()
          for lasers in self.lasers:
               lasers.move(vel)
               if lasers.off_screen(HEIGHT):
                    self.lasers.remove(lasers)
               elif lasers.collision(obj):
                    obj.health -= 10
                    self.lasers.remove(lasers)

     
     def cool_down(self):
          if self.cool_countdown >= self.COOLDOWN:
               self.cool_countdown = 0
          elif self.cool_countdown > 0:
               self.cool_countdown += 1

     def shoot(self):
          if self.cool_countdown == 0:
              laser = Laser(self.x, self.y, self.laser_img)
              self.lasers.append(laser)
              self.cool_countdown = 1

     def get_width(self):
         return self.ship_img.get_width()
    
     def get_height(self):
         return self.ship_img.get_height()


class Player(Character):
     def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = SPACESHIP
        self.laser_img = RED_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)  
        self.max_health = health

     def move_lasers(self, vel, objs):
          self.cool_down()
          for laser in self.lasers:
               laser.move(vel)
               if laser.off_screen(HEIGHT):
                    self.lasers.remove(laser)
               else:
                    for obj in objs:
                         if laser.collision(obj):
                              objs.remove(obj)
                              if laser in self.lasers:
                                   self.lasers.remove(laser)
     
     def health_bar(self, window):
          pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
          pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


     def draw(self, window):
          super().draw(window)
          self.health_bar(window)


class Enemy(Character):
     def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = SPACE_ALIENS
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
    
     def move(self, vel):
         self.y += vel

     def shoot(self):
          if self.cool_countdown == 0:
              laser = Laser(self.x-30, self.y, self.laser_img)
              self.lasers.append(laser)
              self.cool_countdown = 1


class Laser:
     def __init__(self, x, y, img):
          self.x = x
          self.y = y
          self.img = img
          self.mask = pygame.mask.from_surface(self.img)
    
     def draw(self, window):
          window.blit(self.img, (self.x, self.y))

     def move(self, vel):
          self.y += vel

     def off_screen(self, height):
          return not(self.y <= height and self.y >= 0)
     
     def collision(self, obj):
          return collide(self, obj)


def collide(obj1, obj2):
     offset_x = obj2.x - obj1.x
     offset_y = obj2.y - obj1.y
     return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def handle_movement(keys, player):
     if keys[pygame.K_a] and player.x - VEL > 0:
            player.x -= VEL
     if keys[pygame.K_d] and player.x + VEL + player.get_width() < WIDTH:
            player.x += VEL
     if keys[pygame.K_w] and player.y - VEL > 0:
            player.y -= VEL
     if keys[pygame.K_s] and player.y + VEL + player.get_height() + 10 < HEIGHT:
            player.y += VEL
     if keys[pygame.K_SPACE]:
          player.shoot()


def draw_window(lives, level, player, enemies, lost):
    WINDOW.blit(BG, (0, 0))
    lives_text = FONT.render(f"Lives: {lives}", 1, (255, 255, 255))
    level_text = FONT.render(f"Level: {level}", 1, (255, 255, 255))

    WINDOW.blit(lives_text, (10, 10))
    WINDOW.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

    for enemy in enemies:
         enemy.draw(WINDOW)

    player.draw(WINDOW)

    if lost:
         lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
         WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 400))

    pygame.display.update()




#Game loop
def main():
     run = True
     lost = False
     clock = pygame.time.Clock()
     lives = 3
     level = 0
     enemies = []
     wave_length = 5
     enemy_vel = 1
     lost_count = 0
     laser_vel = 5

     player = Player(350, 680)

     while run:
          clock.tick(FPS)

          if lives <= 0 or player.health <= 0:
             lost = True
             lost_count += 1
        
          if lost:
              if lost_count > FPS * 3:
                  run = False
              else:
                   continue
             
             

          if len(enemies) == 0:
               level += 1
               wave_length += 5
               for i in range(wave_length):
                   enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1600, -100))
                   enemies.append(enemy)

          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  run = False
        
          keys = pygame.key.get_pressed()
        

          handle_movement(keys, player)

          for enemy in enemies[:]:
              enemy.move(enemy_vel)
              enemy.move_lasers(laser_vel, player)

              if random.randrange(0, 120) == 1:
                   enemy.shoot()

              if collide(enemy, player):
                   player.health -= 10
                   enemies.remove(enemy)

              elif enemy.y + enemy.get_height() > HEIGHT:
                  lives -= 1
                  enemies.remove(enemy)
 
          
          player.move_lasers(-laser_vel, enemies)
       

          draw_window(lives, level, player, enemies, lost)


def main_menu():
     home_font = pygame.font.SysFont("comicsans", 60)
     run = True
     while run:
          WINDOW.blit(BG, (0, 0))
          title_label = home_font.render("Press the mouse to begin...", 1, (255, 255, 255))
          WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
          pygame.display.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    run = False
               if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
     
     pygame.quit()

main_menu()















