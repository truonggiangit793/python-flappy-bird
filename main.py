import sys
import pygame
import random
pygame.init()
# Audio mixer pre init
pygame.mixer.pre_init(
    frequency=44100,
    size=-16,
    channels=2, 
    buffer=512
)

# Initial variables
WIDTH           = 216
HEIGHT          = 384
MAX_HEIGHT      = 65
FLOOR_X         = 0
FLOOR_Y         = 55
BACKGROUND_X    = 0
FLOOR_SPEED     = 0.8
BG_SPEED        = 0.3
PIPE_SPEED      = 1
GRAVITY         = 0.15
BIRD_MOVEMENT   = 0
BIRD_FLY        = 3
PLAYED          = False
SCORE_STEP      = 1
SCORE_FLAG      = 25
PIPE_TIME       = 1450
SCREEN          = pygame.display.set_mode((WIDTH,HEIGHT))

# Initial resources
score           = 0
high_score      = 0
bot_pipe_list   = []
top_pipe_list   = []
background      = pygame.image.load("assets/background.png").convert()
floor           = pygame.image.load("assets/floor.png").convert()
pipe_up         = pygame.image.load("assets/pipe_up.png").convert()
pipe_down       = pygame.image.load("assets/pipe_down.png").convert()
bird_up         = pygame.image.load("assets/bird_up.png").convert()
bird_mid        = pygame.image.load("assets/bird_mid.png").convert_alpha()
bird_down       = pygame.image.load("assets/bird_down.png").convert()
message         = pygame.image.load("assets/message.png").convert_alpha()
sfx_die         = pygame.mixer.Sound("sound/sfx_die.wav")
sfx_hit         = pygame.mixer.Sound("sound/sfx_hit.wav")
sfx_point       = pygame.mixer.Sound("sound/sfx_point.wav")
sfx_swooshing   = pygame.mixer.Sound("sound/sfx_swooshing.wav")
sfx_wing        = pygame.mixer.Sound("sound/sfx_wing.wav")
bird_rect       = bird_mid.get_rect(center=((WIDTH/5),(HEIGHT/2)))
game_font       = pygame.font.Font("assets/04B_19.TTF",25)
clock           = pygame.time.Clock()
spawn_pipe      = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe,PIPE_TIME)
pygame.display.set_caption('Flappy')
pygame.display.set_icon(bird_mid)


# Function to animate a background
def background_animation():
    SCREEN.blit(background,(BACKGROUND_X,0))
    SCREEN.blit(background,((BACKGROUND_X+WIDTH),0))

# Function to draw a floor
def draw_floor():
    SCREEN.blit(floor,(FLOOR_X,(HEIGHT-FLOOR_Y)))
    SCREEN.blit(floor,((FLOOR_X+WIDTH),(HEIGHT-FLOOR_Y)))

# Function to draw pipes
def draw_pipes(pipe_type,pipes_list):
    for pipe in pipes_list:
        SCREEN.blit(pipe_type,pipe) 

# Function to generate bottom pipes 
def bottom_pipes(rand_num):
    return pipe_up.get_rect(midtop=((WIDTH+10),(HEIGHT-rand_num)))

# Function to generate top pipes 
def top_pipes(rand_num,min_space):
    return pipe_down.get_rect(midbottom=((WIDTH+10),(HEIGHT-rand_num)-min_space))

# Function to animate pipes
def pipes_animation(pipes):
    for pipe in pipes:
        pipe.right -= (PIPE_SPEED)
    return pipes

# Function to check collision
def collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    return True

# Function to rotate bird
def bird_rotate(bird):
    return pygame.transform.rotozoom(bird,-BIRD_MOVEMENT*3,1)

# Function to render score
def score_render():
    score_text = game_font.render(f"{str(score)}",True,(255,255,255))
    score_rect = score_text.get_rect(center=(20,20))
    high_score_text = game_font.render(f"{str(high_score)}",True,(255,255,255))
    high_score_rect = score_text.get_rect(center=(WIDTH-25,20))
    SCREEN.blit(score_text,score_rect)
    SCREEN.blit(high_score_text,high_score_rect)

# Function to render message
def home_screen():
    home = message.get_rect(center=(WIDTH/2,HEIGHT/2))
    SCREEN.blit(message,home)

# Game while loop
while True:
    # Game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PLAYED = True
                BIRD_MOVEMENT = 0
                BIRD_MOVEMENT -= BIRD_FLY
                sfx_wing.play()
        if event.type == spawn_pipe:
            if PLAYED:
                if score >= SCORE_FLAG:
                    if score == SCORE_FLAG:
                        sfx_point.play()
                        SCORE_STEP += 2
                        SCORE_FLAG += 25
                    score += SCORE_STEP
                    PIPE_TIME = random.choice(range(750,1450,5))
                    pygame.time.set_timer(spawn_pipe,PIPE_TIME)
                    rand_num = random.choice(range(100,180,1))
                    min_space = random.choice(range(100,200,5))
                    bot_pipe_list.append(bottom_pipes(rand_num))
                    top_pipe_list.append(top_pipes(rand_num,min_space))
                else:
                    score += SCORE_STEP
                    PIPE_TIME = random.choice(range(1450,1600,5))
                    pygame.time.set_timer(spawn_pipe,PIPE_TIME)
                    rand_num = random.choice(range(100,180,1))
                    min_space = random.choice(range(200,300,5))
                    bot_pipe_list.append(bottom_pipes(rand_num))
                    top_pipe_list.append(top_pipes(rand_num,min_space))

    # Backround
    BACKGROUND_X -= BG_SPEED
    background_animation()
    if BACKGROUND_X <= -WIDTH:
        BACKGROUND_X = 0

    if PLAYED:
        # Pipes
        bot_pipe_list = pipes_animation(bot_pipe_list)
        draw_pipes(pipe_up,bot_pipe_list)
        top_pipe_list = pipes_animation(top_pipe_list)
        draw_pipes(pipe_down,top_pipe_list)

        # Bird
        SCREEN.blit(bird_rotate(bird_mid),bird_rect)
        BIRD_MOVEMENT += GRAVITY
        bird_rect.centery += BIRD_MOVEMENT
        if bird_rect.centery >= (HEIGHT-MAX_HEIGHT):
            bird_rect.centery = (HEIGHT-MAX_HEIGHT)
        if bird_rect.centery <= 10:
            bird_rect.centery = 10
        if collision(top_pipe_list) == False or collision(bot_pipe_list) == False:
            sfx_hit.play()
            PLAYED = False
            if score >= high_score:
                high_score = score
            score = 0
    else:
        home_screen()
        bot_pipe_list.clear()
        top_pipe_list.clear()
        PIPE_SPEED = 1
        SCORE_STEP = 1
        SCORE_FLAG = 25

    # Floor
    FLOOR_X -= FLOOR_SPEED
    draw_floor()
    if FLOOR_X <= -WIDTH:
        FLOOR_X = 0
        
    # Score render
    score_render()

   




    












    pygame.display.update()
    clock.tick(120)
