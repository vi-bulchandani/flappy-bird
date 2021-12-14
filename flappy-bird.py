import pygame
from pygame.locals import *

pygame.init()

screen_width=864
screen_height=936

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('FlappyBird')

#images

bg = pygame.image.load('img/bg.png')

run = True
while run:
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()