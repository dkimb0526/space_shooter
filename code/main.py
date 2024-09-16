import pygame
from os.path import join
from random import randint


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("space shooter")
running = True

x = 100
player_surf = pygame.image.load(join("..","images","player.png")).convert_alpha()
star_surf = pygame.image.load(join("..","images","star.png")).convert_alpha()
star_position = []

for i in range(20):
    star_position.append([randint(0,WINDOW_WIDTH), randint(0,WINDOW_HEIGHT)])


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("aquamarine")
    display_surface.blit(player_surf, (x, 150))
    for x,y in star_position:
        display_surface.blit(star_surf,(x,y))
    pygame.display.update()

pygame.quit()