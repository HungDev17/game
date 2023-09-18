import pygame , sys , random

def draw_floor():
    screen.blit(floor , (floor_x_pos, 650))
    screen.blit(floor , (floor_x_pos + 432, 650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500 , random_pipe_pos))    
    top_pipe = pipe_surface.get_rect(midtop = (500 , random_pipe_pos - 700 ))    
    return bottom_pipe , top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface , pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface , False ,True)
            screen.blit(flip_pipe , pipe)
def check_vacham(pipes):
    for pipe in pipes:
        if bird_react.colliderect(pipe):     
            # hit_sound.play()
            return False
        if bird_react.top <= -75 or bird_react.bottom >= 650:
            return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*2 , 1)
    return new_bird
def  bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100 , bird_react.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main game' :
        score_surface = game_font.render(str(int(score)) , True, (255 , 255 ,255))
        score_rect = score_surface.get_rect(center = (216 , 100))
        screen.blit(score_surface , score_rect)
    if game_state == 'game_over':
                score_surface = game_font.render(f'Diem {int(score)}' , True, (255 , 255 ,255))
                score_rect = score_surface.get_rect(center = (216 , 100))
                screen.blit(score_surface , score_rect)

                higt_score_surface = game_font.render(f'Diem cao {int(score)}', True, (255 , 255 ,255))
                higt_score_rect = score_surface.get_rect(center = (200 , 630))
                screen.blit(higt_score_surface , higt_score_rect)
def update_score(score , high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100 , size=-16 , channels=2 , buffer=512)
pygame.init()
screen = pygame.display.set_mode((432 , 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf' , 40)

# bien
game_active = True
trongluc = 0.25
bird_movement = 0
score = 0
high_score = 0
# background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
# san
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# chim
bird_down = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_mid = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird  = bird_list[bird_index]
# bird = pygame.transform.scale2x(bird)
bird_react = bird.get_rect(center = (100 , 384))

# timer bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap , 200)
# ong
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# tao timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1500)
pipe_height = [200 , 300 , 400]
# ket thuc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216 , 384))
# am thanh
# flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
# hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
# die_sound = pygame.mixer.Sound('sound/sfx_die.wav')
# score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# score_sound_countdown = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement =- 11
                # flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_movement = 0  
                score = 0
                bird_react.center = (100 , 384)
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2 :
                bird_index += 1
            else:
                bird_index = 0
            bird , bird_react = bird_animation()
    screen.blit(bg , (0 , 0))
    if game_active:
            # chim
            bird_movement += trongluc
            rotated_bird = rotate_bird(bird)
            bird_react.centery += bird_movement
            screen.blit(rotated_bird , bird_react) 
            game_active =  check_vacham(pipe_list)
            # ong
            pipe_list = move_pipe(pipe_list)
            draw_pipe(pipe_list  )
            score += 0.01
            score_display('main game')
            # score_sound_countdown -=1
            # if score_sound_countdown <= 0:
            #     # score_sound.play()
            #     score_sound_countdown= 100
    else:
        screen.blit(game_over_surface , game_over_rect)
        high_score = update_score(score , high_score)
        score_display('game_over')
        

    # san
    floor_x_pos -= 1
    if floor_x_pos <= -432:
        floor_x_pos = 0
    draw_floor()
    pygame.display.update()
    clock.tick(120)