import pygame
from os.path import join
from random import randint, uniform



pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("space shooter")
running = True
clock = pygame.time.Clock()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))
    def update(self,dt):
        pass

class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("..","images","player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        #initialize direction to [0,0]
        self.direction = pygame.Vector2()
        self.speed = 300
        self.can_shoot = True
        self.laser_shoot_time = 0
        #miliseconds
        self.cooldown_duration = 400
        #getting a mask from image surface for better collision detections
        self.mask = pygame.mask.from_surface(self.image)


    def laser_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        #only normalize the vector when there is an input, else its [0,0] which means false
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_time()
        

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.rect.centery -= 400 *dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.og_img = surf
        self.image = self.og_img
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.life_time = 3000
        #random between floating points
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400,500)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation = 0

    def update(self, dt):
        #center is a tuple(x, y) , direction is vector(a,b) it adds x to a and y to b
        self.rect.center += self.direction * self.speed * dt
        #self.start
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()

        self.rotation += randint(0,100) * dt
        self.image = pygame.transform.rotozoom(self.og_img, self.rotation,1)
        #update rect based on rotated surface
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimationExplosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=(pos))

    def update(self,dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions():
    global running
    #print(pygame.sprite.spritecollide(player, meteor_sprites, True))
    #note using mask is hardware intensive
    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        running = False

    all_sprites.draw(display_surface)
    for l in laser_sprites:
        if pygame.sprite.spritecollide(l, meteor_sprites, True):
            l.kill()
            AnimationExplosion(explosion_frames,l.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks()//1000
    text_surf = font.render(str(current_time), True, "red")
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH//2, WINDOW_HEIGHT-50))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface,"red",text_rect.inflate(20,10).move(0,-8),5,10)
#imports
star_surf = pygame.image.load(join("..","images","star.png")).convert_alpha()
laser_surf = pygame.image.load(join("..","images","laser.png")).convert_alpha()
meteor_surf = pygame.image.load(join("..","images","meteor.png")).convert_alpha()
#paramters(font,fontsize) none = default, importing custom font
font = pygame.font.Font(join("..","images","Oxanium-Bold.ttf"),40)
explosion_frames = [pygame.image.load(join("..","images/explosion",f"{i}.png")).convert_alpha() for i in range(21)]
#set volume is 0 - 1, floatpoint value
laser_sound = pygame.mixer.Sound(join("..","audio","laser.wav"))
explosion_sound = pygame.mixer.Sound(join("..","audio","explosion.wav"))
game_music = pygame.mixer.Sound(join("..","audio","game_music.wav"))
laser_sound.set_volume(0.01)
explosion_sound.set_volume(0.01)
game_music.set_volume(0.01)
#-1 = indefinitely, 5  = 5 times
game_music.play(loops=-1)


#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf)

player = Player(all_sprites)

#custom event
meteor_event = pygame.event.custom_type()
#miliseconds, 500 = 0.5 seconds, need understand how this work
pygame.time.set_timer(meteor_event,500)

while running:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == meteor_event:
            x, y = randint(0,WINDOW_WIDTH),randint(-200,-100)
            Meteor(meteor_surf,(x,y), (all_sprites, meteor_sprites))
    #clock.tick(60)

    display_surface.fill("aquamarine")
    display_score()
    all_sprites.update(dt)
    collisions()


    pygame.display.update()

pygame.quit()