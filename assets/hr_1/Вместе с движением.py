print(1)
import pygame
import sys
import math

width, height = 1200, 800
size_frame_x, size_frame_y = 70, 60
size_bullet = 100
all_sprite = pygame.sprite.Group()
sprite_bullet = pygame.sprite.Group()
sprite_platform = pygame.sprite.Group()
sprite_barrier = pygame.sprite.Group()
ghost_sprite = pygame.sprite.Sprite()
filename_bullet = r'bullet.png' 
filename_hero = r'pass.png'
filename_hero_2 = r'walk1.png'
filename_hero_3 = r'walk2.png'


class Hero(pygame.sprite.Sprite):
    def __init__(self, file_name):
        super().__init__(all_sprite)
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (size_frame_x, size_frame_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rotate_k = 'r'
        self.rect.x = 0
        self.rect.y = 0

    def update(self, sp_x, sp_y, rotate):
        if rotate:
            if self.rotate_k == 'r':
                self.rotate_k = 'l'
            else:
                self.rotate_k = 'r'
            self.image = pygame.transform.flip(self.image, 1, 0)
        if pygame.sprite.spritecollideany(self, sprite_platform):
            if pygame.sprite.spritecollideany(ghost_sprite, sprite_platform):
                if sp_y < 0:
                    sp_y = 0
            else:
                if sp_y > 0:
                    sp_y = 0
        else:
            if sp_y == 0:
                sp_y = 5
        self.rect = self.rect.move(sp_x, sp_y)

            
    
    def new_image(self, file_name, coord):
        self.image = self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (size_frame_x, size_frame_y))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_colorkey((0, 0, 0))
        self.rect.x, self.rect.y = coord
        if self.rotate_k == 'l':
            self.image = pygame.transform.flip(self.image, 1, 0)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, file_name, pos, target_pos):
        super().__init__()
        sprite_bullet.add(self)
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (18, 5))#18, 5
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.target_pos = target_pos
        catet1, catet2 = self.target_pos[0]-self.rect.x, self.target_pos[1]-self.rect.y
        try:
            self.angle = int(math.degrees(math.atan(catet1/catet2)))
        except ZeroDivisionError:
            self.angle = 90
        if target_pos[1] > pos[1]:
            self.image = pygame.transform.rotate(self.image, self.angle+270)
        else:
            self.image = pygame.transform.rotate(self.image, self.angle+90)
        self.image.set_colorkey((255, 255, 255))
        self.n = 0
        self.delta_x, self.delta_y = 0, 0
        self.k_x, self.k_y = 0, 0
        if  80 <= self.angle <= 85 or -85 <= self.angle <= -80:
            self.delta_x = 3
        elif self.angle >= 85 or self.angle <= -85:
            self.delta_x = 3
        elif 70 <= self.angle <= 80 or -80 <= self.angle <= -70:
            self.delta_x = 3
        elif 60 <= self.angle <= 70 or -70 <= self.angle <= -60:
            self.delta_x = 3
        elif 50 <= self.angle <= 60 or -60 <= self.angle <= -50:
            self.delta_x = 3
            self.delta_y = 2
        elif 40 <= self.angle <= 50 or -50 <= self.angle <= -40:
            self.delta_x = 2
            self.delta_y = 2
        elif 20 <= self.angle <= 40 or -40 <= self.angle <= -20:
            self.delta_x = 2
            self.delta_y = 3
        elif 0 <= self.angle <= 20 or -20 <= self.angle <= 0:
            self.delta_y = 3

        if self.rect.x > self.target_pos[0] and self.angle >= 0:
            self.k_x = -1
            self.k_y = -1
        elif self.rect.x < self.target_pos[0] and self.angle >= 0:
            self.k_x = 1
            self.k_y = 1
        elif self.rect.y < self.target_pos[1] and self.angle <= 0:
            self.k_x = -1
            self.k_y = 1
        else:
            self.k_x = 1
            self.k_y = -1

    def update(self, *arr):
        self.n += 1
        if 85 >= self.angle >= 80 or -85 <= self.angle <= -80:
            self.delta_y = 0
            if self.n % 3 == 0:
                self.delta_y = 1
        elif 70 <= self.angle <= 80 or -80 <= self.angle <= -70:
            self.delta_y = 0
            if self.n % 4 == 0:
                self.delta_y = 3
        elif 60 <= self.angle <= 70 or -70 <= self.angle <= -60:
            self.delta_y = 0
            if self.n % 3 == 0:
                self.delta_y = 4
        
        self.rect = self.rect.move(self.k_x * self.delta_x, self.k_y * self.delta_y)
        if self.rect.x <= 0 or self.rect.x >= width or self.rect.y >= height or self.rect.y <= 0 or pygame.sprite.spritecollideany(self, sprite_barrier):
            self.kill()


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprite)
        sprite_platform.add(self)
        self.image = pygame.Surface([size[0], size[1]])
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.image.fill(pygame.Color("red"))


def main():
    pygame.init()
    size = width, height
    screen = pygame.display.set_mode(size)
    background = pygame.Surface(size)
    clock = pygame.time.Clock()

    jump_event = 30000
    shot_event = 30001
    shot_event2 = 30002
    move_event = 30003
    coord = X, Y = 0, 0
    sp_x, sp_y, jump_speed, gravity = 0, 0, -10, 1
    pygame.time.set_timer(jump_event, 30)
    pygame.time.set_timer(shot_event, 5)
    pygame.time.set_timer(shot_event2, 60)
    pygame.time.set_timer(move_event, 120)
    running, press, jump, rotate = True, False, False, False
    rotate_hero = 'r'
    old_x = 0
    now_herofile = filename_hero
    hero1 = Hero(filename_hero)
    Platform((100, 300), (800, 2))
    sprite_barrier.add(Platform((100, 200), (100, 3)))
    sprite_barrier.add(Platform((250, 100), (100, 3)))
    Platform((-100, 600), (1100, 2))
    sprite_barrier.add(Platform((300, 450), (200, 3)))
    ghost_sprite.image = pygame.Surface([hero1.rect.size[0], 10])
    ghost_sprite.rect = pygame.Rect(0, 0, hero1.rect.size[0], 10)
    while running:
        coord = X, Y = hero1.rect.x, hero1.rect.y
        ghost_sprite.rect = ghost_sprite.rect.move(X-ghost_sprite.rect.x, Y-ghost_sprite.rect.y)
        ghost_sprite.rect.x = X
        ghost_sprite.rect.y = Y
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                press = True
                mouse_pos = event.pos
                Bullet(filename_bullet, (X+20, Y+10), event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                press = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not jump:
                    jump = True
                elif event.key == pygame.K_ESCAPE:
                    hero1.new_image(filename_hero_2, coord)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    all_sprite.update(0, 5, False)
            if event.type == shot_event:
                sprite_bullet.update()
            if press and event.type == shot_event2:
                Bullet(filename_bullet, (X+20, Y+10), mouse_pos)
            if jump and event.type == jump_event:
                jump_speed += gravity
                if jump_speed > 0 and pygame.sprite.spritecollideany(hero1, sprite_platform):
                    jump_speed = -10
                    jump = False
            if event.type == move_event:
                if old_x != coord[0]:
                    if now_herofile == filename_hero:
                        now_herofile = filename_hero_2
                    elif now_herofile == filename_hero_2:
                        now_herofile = filename_hero_3
                    elif now_herofile == filename_hero_3:
                        now_herofile = filename_hero
                    hero1.new_image(now_herofile, coord)
                elif now_herofile != filename_hero:
                    now_herofile = filename_hero
                    hero1.new_image(now_herofile, coord)
                old_x = coord[0]

        #---------------------------------
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if sp_x != -2 and rotate_hero == 'r':
                rotate = True
                rotate_hero = 'l'
            else:
                rotate = False
            sp_x = -2
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if sp_x != 2 and rotate_hero == 'l':
                rotate = True
                rotate_hero = 'r'
            else:
                rotate = False
            sp_x = 2
        else:
            sp_x = 0
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            sp_x = 0
        #---------------------------------
        if jump:
            sp_y = jump_speed
        else:
            sp_y = 0
        sprite_bullet.draw(screen)
        all_sprite.draw(screen)
        all_sprite.update(sp_x, sp_y, rotate)
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())