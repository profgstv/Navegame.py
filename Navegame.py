import pygame
import math
import save_score
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
save_score.reading_data()

start_menu = True
start_menu_color = (255, 255, 255)
game_over = False

vel_const = 15
vel = vel_const
score = 0
highscore = save_score.highscore


def quit_game():
    save_score.writing_data()
    pygame.quit()
    exit()

class screen:
    width = pygame.display.Info().current_w
    height = pygame.display.Info().current_h
    canva = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    pygame.display.set_caption('Navegame.py')

    font_start_menu0 = pygame.font.Font(None, int(width*0.1))
    start_game_message = font_start_menu0.render("Navegame.py", True, (255, 255, 255))
    font_start_menu1 =  pygame.font.Font(None, int(width*0.03))
    start_game_button_press = font_start_menu1.render("Aperte 'Enter' para Começar ou 'Esc' para Sair", True, (255, 255, 255))

    font_score = pygame.font.Font(None, int(width*0.02))
    font_highscore = pygame.font.Font(None, int(width*0.02))
    count = font_score.render(f"Pontuação: {score}", True, (255, 255, 255))
    high_count = font_highscore.render(f"Recorde: {highscore}", True, (255, 255, 255))

    font_game_over0 = pygame.font.Font(None, int(width*0.1))
    game_over_message0 = font_game_over0.render("Você Perdeu!", True, (255, 255, 255))
    font_game_over1 = pygame.font.Font(None, int(width*0.03))
    game_over_message1 = font_game_over1.render("Aperte 'Enter' para Recomeçar ou 'Esc' para Sair", True, (255, 255, 255))

class background:
    def color(rgb):
        pygame.draw.rect(screen.canva, rgb, (0, 0, screen.width, screen.height))
        return
    
    class image(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.sprites = []
            for i in range(14):
                if i <= 9:
                    self.sprites.append(pygame.image.load(f'./assets/sprites/space0{i}.gif'))
                else:
                    self.sprites.append(pygame.image.load(f'./assets/sprites/space{i}.gif'))
            self.current = 0

            self.image = self.sprites[self.current]
            self.rect = self.image.get_rect()
        
        def update(self):
            global vel
            self.current += vel*0.02
            if self.current >= len(self.sprites):
                self.current = 0
            self.image = self.sprites[int(self.current)]
            self.image = pygame.transform.scale(self.image, (screen.width, screen.height))
            self.rect.topleft = 0, 0

    class sounds:
        music = pygame.mixer.music.load('./assets/sounds/space_expedition.mp3')
        scored = pygame.mixer.Sound('./assets/sounds/scoring.mp3')
        crash = pygame.mixer.Sound('./assets/sounds/explosion.mp3')   

class player:
    r = screen.width*0.025
    x = screen.width*0.05
    y = screen.height*0.5

    def ball():
        pygame.draw.circle(screen.canva, (255, 255, 255), (player.x, player.y), player.r)
        return

    def control(key):
        global score
        global highscore
        global start_menu
        global game_over

        if key[pygame.K_RETURN] and start_menu:
            pygame.mixer.music.play(-1)
            start_menu = False
        elif key[pygame.K_RETURN] and game_over:
            pygame.mixer.music.play(-1)
            game_over = False
            score = 0
            highscore = save_score.highscore
            screen.count = screen.font_score.render(f"Pontuação: {score}", True, (255, 255, 255))
            screen.high_count = screen.font_highscore.render(f"Recorde: {highscore}", True, (255, 255, 255))
        elif key[pygame.K_UP] and player.y >= player.r*3 and not game_over:
            player.y -= vel
        elif key[pygame.K_DOWN] and player.y <= screen.height - player.r*1.25 and not game_over:
            player.y += vel
        elif key[pygame.K_ESCAPE]:
            quit_game()
        return

class player_sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(8):
            self.sprites.append(pygame.image.load(f'./assets/sprites/player{i}.gif'))
        self.current = 0

        self.image = self.sprites[self.current]
        self.rect = self.image.get_rect()
    
    def update(self):
        global vel
        self.current += vel*0.01
        if self.current >= len(self.sprites):
            self.current = 0
        self.image = self.sprites[int(self.current)]
        self.image = pygame.transform.scale(self.image, (player.r*2, player.r*2))
        self.rect.topleft = player.x - player.r, player.y - player.r

class enemies:
    r = [0, 0, 0, 0, 0]
    x = [0, 0, 0, 0, 0]
    y = [0, 0, 0, 0, 0]
    v = [0, 0, 0, 0, 0]
    angle = [0, 0, 0, 0, 0]

    def ball(self):
        pygame.draw.circle(screen.canva, (255, 255, 255), (self.x[0], self.y[0]), self.r[0])
        return

    def movement(self, i):
        global score
        if not game_over:
            self.x[i] -= self.v[i]

            if self.x[i] <= 0:
                if not start_menu:
                    background.sounds.scored.play()
                    score += 1
                    screen.count = screen.font_score.render(f"Pontuação: {score}", True, (255, 255, 255))

                self.r[i] = int(screen.width*randint(10, 15)/1000)
                self.x[i] = screen.width
                self.y[i] = randint(int(screen.height*0.1), screen.height - int(self.r[i]*1.05))
                self.v[i] = int(vel*randint(110, 150)/100)
                self.angle[i] = randint(0, 360)
            
        return
    
    def colision(self, i): # Usar math.dist(p, q), onde p e q são as coordenadas de cada ponto
        global score
        global game_over
        if math.dist((self.x[i], self.y[i]), (player.x, player.y)) <= self.r[i] + player.r:
            background.sounds.crash.play()
            pygame.mixer.music.pause()
            game_over = True
            
            self.r[i] = int(screen.width*randint(10, 15)/1000)
            self.x[i] = screen.width
            self.y[i] = randint(int(screen.width*0.1), screen.height - int(self.r[i]*1.05))
            self.v[i] = int(vel*randint(110, 150)/100)

class enemies_sprites(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load(f'./assets/sprites/enemy0.png')
        self.image = self.sprite
        self.rect = self.image.get_rect()
    
    def update(self, enemy_index):
        self.image = self.sprite
        self.image = pygame.transform.scale(self.image, (enemies.r[enemy_index]*2, enemies.r[enemy_index]*2))
        self.image = pygame.transform.rotate(self.image, enemies.angle[enemy_index])
        self.rect.topleft = enemies.x[enemy_index] - enemies.r[enemy_index], enemies.y[enemy_index] - enemies.r[enemy_index]


sprites_group = pygame.sprite.Group()
sprites_group.add(background.image())
sprites_group.add(player_sprite())

enemies_list = []
enemies_sprites_group = pygame.sprite.Group()

for i in range(5):
    enemies_list.append(enemies_sprites())
    enemies_sprites_group.add(enemies_list[i])


while True:
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()

    player.control(key)

    if int(score/5 + 1) <= 5:
        difficulty = int(score/5 + 1)
    vel = vel_const * (1 + difficulty/5)

    if start_menu:
        background.color((0, 0, 0))
        player.ball()
        enemies.movement(enemies, 0)
        enemies.ball(enemies)
        screen.canva.blit(screen.high_count, (screen.width*0.5 - screen.high_count.get_width()/2, screen.width*0.005))

        screen.canva.blit(screen.start_game_message, (screen.width*0.5 - screen.start_game_message.get_width()/2, screen.height*0.5 - screen.start_game_message.get_height()/2))
        screen.canva.blit(screen.start_game_button_press, (screen.width*0.5 - screen.start_game_button_press.get_width()/2, screen.height*0.5 + screen.start_game_message.get_height() - screen.start_game_button_press.get_height()/2))

    elif game_over:
        background.color((0, 0, 0))

        save_score.new_score(score)

        screen.canva.blit(screen.count, (screen.width*0.4 - screen.count.get_width(), screen.width*0.005))
        screen.canva.blit(screen.high_count, (screen.width*0.6, screen.width*0.005))

        screen.canva.blit(screen.game_over_message0, (screen.width*0.5 - screen.game_over_message0.get_width()/2, screen.height*0.5 - screen.game_over_message0.get_height()/2))
        screen.canva.blit(screen.game_over_message1, (screen.width*0.5 - screen.game_over_message1.get_width()/2, screen.height*0.5 + screen.game_over_message0.get_height() - screen.game_over_message1.get_height()/2))

    else:
        sprites_group.draw(screen.canva)
        sprites_group.update()

        for i in range(difficulty):
            enemies_sprites_group.draw(screen.canva)
            enemies_sprites_group.update(i)
            enemies.movement(enemies, i)
            enemies.colision(enemies, i)

        screen.canva.blit(screen.count, (screen.width*0.4 - screen.count.get_width(), screen.width*0.005))
        screen.canva.blit(screen.high_count, (screen.width*0.6, screen.width*0.005))

        if score >= highscore:
            highscore = score
            screen.high_count = screen.font_highscore.render(f"Recorde: {highscore}", True, (255, 255, 255))

    pygame.display.update()