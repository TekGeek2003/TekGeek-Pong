import pygame, sys, random


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= WIN_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # PLAYER SCORE
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        player_score += 1

    # OPPONENT SCORE
    if ball.right >= WIN_width:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        opponent_score += 1

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right  - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left  - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >=WIN_height:
        player.bottom = WIN_height

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom >ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >=WIN_height:
        opponent.bottom = WIN_height

def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (WIN_width/2, WIN_height/2)

    if current_time - score_time < 700:
        number_three = game_font.render("3",False, '#4169e1')
        WIN.blit(number_three,(WIN_width/2 - 10, WIN_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_number = game_font.render("2",False, '#274C3B')
        WIN.blit(number_number,(WIN_width/2 - 10, WIN_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1",False, '#4169e1')
        WIN.blit(number_one,(WIN_width/2 - 10, WIN_height/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_y = 7 * random.choice((1,-1))
        ball_speed_x = 7 * random.choice((1,-1))
        score_time = None






# GENERAL SETUP
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()

# GAME WINDOW
WIN_width = 900
WIN_height = 500
WIN = pygame.display.set_mode((WIN_width, WIN_height))
pygame.display.set_caption('TekGeek Pong')

# GAME RECTANGLES
ball =  pygame.Rect(WIN_width/2 - 15,WIN_height/2 - 15, 30, 30)
player = pygame.Rect(WIN_width - 20, WIN_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, WIN_height/2 - 70, 10, 140)

# COLORS
bg_color = pygame.Color('#ADD8E6')
accent_color = (27,35,43)
middle_strip = pygame.Rect(WIN_width/2 - 2,0,4,WIN_height)



# GAME VARIABELS
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7


# TEXT VARIABLES
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf",32)

# SOUND
pong_sound = pygame.mixer.Sound('/Users/techwiz2003/Desktop/TekGeek Pong/TekGeek Pygame/pong.ogg')
score_sound = pygame.mixer.Sound('/Users/techwiz2003/Desktop/TekGeek Pong/TekGeek Pygame/score.ogg')

# SCORE TIMER
score_time = True


# MAIN GAME LOOP
while True:
    # HANDLING INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

               

    # GAME LOGIC
    ball_animation()
    player_animation()
    opponent_ai()
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom >ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >=WIN_height:
        opponent.bottom = WIN_height



    

    



    # Visuals
    WIN.fill(bg_color)
    pygame.draw.rect(WIN, '#00008B', player)
    pygame.draw.rect(WIN, '#00008B', opponent)
    pygame.draw.ellipse(WIN, '#274C3B', ball)
    pygame.draw.aaline(WIN, '#32CD32', (WIN_width/2,0), (WIN_width/2,WIN_height))

    if score_time:
        ball_start()

    player_text = game_font.render(f"{player_score}",False,'#00008B')
    WIN.blit(player_text,(660,470))

    opponent_text = game_font.render(f"{opponent_score}",False,'#00008B')
    WIN.blit(opponent_text,(200,470))


    # UPDATING THE WINDOW
    pygame.display.flip()
    clock.tick(60)