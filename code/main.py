import pygame
from os.path import join
from random import randint



pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("space shooter")
running = True
clock = pygame.time.Clock()

class Star(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.image.load(join("..","images","star.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(x,y))
    def update(self):
        pass

class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("..","images","player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        #initialize direction to [0,0]
        self.direction = pygame.Vector2()
        self.speed = 300

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        #only normalize the vector when there is an input, else its [0,0] which means false
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print("fire")




all_sprites = pygame.sprite.Group()
print(all_sprites)
print("==========")
player = Player(all_sprites)
print(all_sprites)

star_surf = pygame.image.load(join("..","images","star.png")).convert_alpha()
star_position = []

for i in range(20):
    star_position.append([randint(0,WINDOW_WIDTH), randint(0,WINDOW_HEIGHT)])


while running:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #clock.tick(60)

    display_surface.fill("aquamarine")

    all_sprites.update(dt)

    for x,y in star_position:
        display_surface.blit(star_surf,(x,y))
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()