import pygame
from pygame.locals import *
import random
pygame.init()


clock = pygame.time.Clock()
fps = 60

screen_width=864
screen_height=936

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Flappy Bird')


ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap=150
pipe_frequency=1500
last_pipe=pygame.time.get_ticks()
#images

bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

run = True

class Bird (pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1,4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)

        self.image=self.images[self.index]
        self.rect= self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.pressed=False

    def update(self):
        if flying:
            self.vel+=0.5
            if self.vel>8:
                self.vel=8
            if self.rect.bottom<768:
                self.rect.y+=int(self.vel)

        if not game_over:
            if pygame.key.get_pressed()[K_SPACE] and (not self.pressed):
                self.pressed=True
                self.vel=-10
            elif not pygame.key.get_pressed()[K_SPACE]:
                self.pressed=False
            

            self.counter+=1
            flap_cooldown=10


            if self.counter>flap_cooldown:
                self.counter=0
                self.index+=1
                self.index%=len(self.images)
            self.image=self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], -2*self.vel)

        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect=self.image.get_rect()
        if position==1:
            self.rect.bottomleft = [x,y-pipe_gap//2]
            self.image=pygame.transform.flip(self.image, False, True)
        else:
            self.rect.topleft = [x,y+pipe_gap//2]

    def update(self):
        if not game_over and flying:
            self.rect.x-= scroll_speed
            if self.rect.right<0:
                self.kill()
        

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


flappy = Bird(100, screen_height//2)

bird_group.add(flappy)



########################################
# Game loop
#######################################
while run:
    clock.tick(fps)
    screen.blit(bg,(0,0))
    
    bird_group.draw(screen)
    pipe_group.draw(screen)
    bird_group.update()
    pipe_group.update()

    if flappy.rect.bottom>=768:
        game_over = True
        flying = False
    ground_scroll-=scroll_speed

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top<0:
        game_over=True



    if game_over==False:
        screen.blit(ground_img,(ground_scroll,768))
    if game_over==False and flying==True:
        

        time_now=pygame.time.get_ticks()
        if time_now-last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(screen_width, (screen_height-pipe_gap)//2+pipe_height,-1)
            top_pipe = Pipe(screen_width, (screen_height-pipe_gap)//2+pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now

    if (ground_scroll < -35):
        ground_scroll=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and game_over==False:
            flying = True



    pygame.display.update()


# exit
pygame.quit()