import pygame
import random
pygame.init()

#Font
FONT = pygame.font.SysFont("comicsans", 30)
GAME_FONT = pygame.font.SysFont("comicsans", 50)


#Window
WIDTH, HEIGHT = 1000, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 1, HEIGHT)


#Players
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER = pygame.Rect(10, HEIGHT/2 - 10, 10, 75)
OPPONENT_PLAYER = pygame.Rect(WIDTH - 20, HEIGHT/2 - 10, 10, 75)
BALL = pygame.Rect(WIDTH//2 - 5, HEIGHT//2, 10, 10)

#Player speeds
player_vel = 5
opponent_vel = 5
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = 4 * random.choice((1, -1))
player_score = 0
opponent_score = 0


        

def player_movement(keys, PLAYER):
    if keys[pygame.K_w] and PLAYER.y - player_vel > 0:
        PLAYER.y -= player_vel
    if keys[pygame.K_s] and PLAYER.y + player_vel + 75 < HEIGHT:
        PLAYER.y += player_vel



def opponent_movement():
    if OPPONENT_PLAYER.top < BALL.y and OPPONENT_PLAYER.y + opponent_vel + 75 < HEIGHT:
        OPPONENT_PLAYER.top += opponent_vel
    if OPPONENT_PLAYER.bottom > BALL.y and OPPONENT_PLAYER.y - opponent_vel > 0:
        OPPONENT_PLAYER.bottom -= opponent_vel




def ball_movement():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    if BALL.top <= 0 or BALL.bottom >= HEIGHT:
        ball_speed_y *= -1
    if BALL.left <= 0:
        opponent_score += 1
        reset_ball()
    if BALL.right >= WIDTH:
        player_score += 1
        reset_ball()
    if BALL.colliderect(PLAYER) or BALL.colliderect(OPPONENT_PLAYER):
        ball_speed_x *= -1

    BALL.x += ball_speed_x
    BALL.y += ball_speed_y



def reset_ball():
    global ball_speed_x, ball_speed_y
    BALL.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))


    




def draw_window(window, won, lost):
    window.fill(BLACK)
    pygame.draw.rect(WINDOW, WHITE, PLAYER)
    pygame.draw.rect(WINDOW, WHITE, OPPONENT_PLAYER)
    pygame.draw.rect(WINDOW, WHITE, BORDER)
    pygame.draw.ellipse(WINDOW, WHITE, BALL)

    player_score_text = FONT.render(f"{player_score}", 1, WHITE)
    opponent_score_text = FONT.render(F"{opponent_score}", 1, WHITE)
    window.blit(player_score_text, (WIDTH*0.25 - player_score_text.get_width()/2, 10))
    window.blit(opponent_score_text, (WIDTH*0.75 - opponent_score_text.get_width()/2, 10))

    if won:
        won_text = GAME_FONT.render("You won!!", 1, WHITE)
        window.blit(won_text, (WIDTH/2 - won_text.get_width()/2, 300))

    if lost:
        lost_text = GAME_FONT.render("You lost!!", 1, WHITE)
        window.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, 300))


    
    pygame.display.update()




def main():
    run = True
    won = False
    lost = False
    lost_count = 0
    won_count = 0
    clock = pygame.time.Clock()
    FPS = 60


    while run:
        clock.tick(FPS)

        if player_score == 10:
            won = True
            won_count += 1

        if won:
            if won_count > FPS * 3:
                run = False
            else:
                continue

        if opponent_score == 10:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()

        #Movement methods
        player_movement(keys, PLAYER)
        opponent_movement()
        ball_movement()

        #Display
        draw_window(WINDOW, won, lost)



def main_menu():
    begin_font = pygame.font.SysFont("comicsans", 50)
    win_font = pygame.font.SysFont("comicsans", 30)
    run = True
    while run:
        WINDOW.fill(BLACK)
        begin_text = begin_font.render("Press the mouse to begin...", 1, WHITE)
        win_text = win_font.render("Score 10 points to win", 1, WHITE)
        WINDOW.blit(begin_text, (WIDTH/2 - begin_text.get_width()/2, 250))
        WINDOW.blit(win_text, (WIDTH/2 - win_text.get_width()/2, 310))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
        
    pygame.quit()


main_menu()