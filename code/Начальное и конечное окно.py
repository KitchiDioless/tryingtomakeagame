import pygame
import sys
import math

width, height = 960, 640
size_frame_x, size_frame_y = 70, 60
size_bullet = 100
all_sprite = pygame.sprite.Group()
sprites_bullet = pygame.sprite.Group()
sprites_platform = pygame.sprite.Group()
sprite_barrier = pygame.sprite.Group()
sprite_enemy = pygame.sprite.Group()
sprite_reload = pygame.sprite.Group()
ghost_sprite = pygame.sprite.Sprite()
filename_bullet = r'project\bullet.png' 
filename_hero = r'project\pass.png'
filename_hero_2 = r'project\walk1.png'
filename_hero_3 = r'project\walk2.png'
filename_game_over = r'project\gameover.png'
filename_reload = r'project\reload.png'
filename_exit = r'project\exit.png'

class Draw(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, size):
        super().__init__(all_sprite)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.set_colorkey((255, 255, 255))


class Hero(pygame.sprite.Sprite):
    def __init__(self, file_name, hp):
        super().__init__(all_sprite)
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (size_frame_x, size_frame_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rotate_k = 'r'
        self.rect.x = 0
        self.rect.y = 0
        self.HP = hp
        self.strip_hp = pygame.sprite.Sprite()
        all_sprite.add(self.strip_hp)
        self.strip_hp.image = pygame.Surface([self.rect.size[0], 5])
        self.strip_hp.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.size[0], 5)
        self.strip_hp.image.fill(pygame.Color("green"))

    def update(self, sp_x, sp_y, rotate):
        if rotate:
            if self.rotate_k == 'r':
                self.rotate_k = 'l'
            else:
                self.rotate_k = 'r'
            self.image = pygame.transform.flip(self.image, 1, 0)
        if pygame.sprite.spritecollideany(self, sprites_platform):
            if pygame.sprite.spritecollideany(ghost_sprite, sprites_platform):
                if sp_y < 0:
                    sp_y = 0
            else:
                if sp_y > 0:
                    sp_y = 0
        else:
            if sp_y == 0:
                sp_y = 5
        self.rect = self.rect.move(sp_x, sp_y)
        self.strip_hp.rect.x = self.rect.x
        self.strip_hp.rect.y = self.rect.y

    def new_image(self, file_name, coord):
        self.image = self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (size_frame_x, size_frame_y))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_colorkey((0, 0, 0))
        self.rect.x, self.rect.y = coord
        if self.rotate_k == 'l':
            self.image = pygame.transform.flip(self.image, 1, 0)
    
    def damage(self, zn):
        if pygame.sprite.spritecollideany(self, sprite_enemy):
            self.HP -= int(zn)
            if self.HP <= 0:
                self.kill()
            self.strip_hp.image = pygame.transform.scale(self.strip_hp.image, (self.HP, 5))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, file_name, pos, target_pos):
        super().__init__()
        sprites_bullet.add(self)
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (15, 4))
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
        elif 30 <= self.angle <= 40 or -40 <= self.angle <= -30:
            self.delta_x = 2
            self.delta_y = 3
        elif 20 <= self.angle <= 30 or -30 <= self.angle <= -20:
            self.delta_y = 3
        elif 10 <= self.angle <= 20 or -20 <= self.angle <= -10:
            self.delta_y = 3
        else:
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
        elif 20 <= self.angle <= 30 or -30 <= self.angle <= -20:
            self.delta_x = 0
            if self.n % 2 == 0:
                self.delta_x = 3
        elif 10 <= self.angle <= 20 or -20 <= self.angle <= -10:
            self.delta_x = 0
            if self.n % 3 == 0:
                self.delta_x = 2

        self.rect = self.rect.move(self.k_x * self.delta_x, self.k_y * self.delta_y)
        if self.rect.x <= 0 or self.rect.x >= width or self.rect.y >= height or self.rect.y <= 0 or pygame.sprite.spritecollideany(self, sprite_barrier):
            self.kill()
        if pygame.sprite.spritecollideany(self, sprite_enemy):
            sprite_enemy.update(4)
            self.kill()


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprite)
        sprites_platform.add(self)
        self.image = pygame.Surface([size[0], size[1]])
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.image.fill(pygame.Color("red"))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.HP = size[0]
        sprite_enemy.add(self)
        self.image = pygame.Surface([size[0], size[1]])
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.image.fill(pygame.Color("blue"))
        self.strip_hp = pygame.sprite.Sprite()
        all_sprite.add(self.strip_hp)
        self.strip_hp.image = pygame.Surface([size[0], 5])
        self.strip_hp.rect = pygame.Rect(pos[0], pos[1], size[0], 5)
        self.strip_hp.image.fill(pygame.Color("green"))
        
    
    def update(self, zn):
        if zn == 0:
            self.rect = self.rect.move(-5, 0)
            if self.rect.x < 0:
                self.rect.x = 960
            self.strip_hp.rect.x = self.rect.x
            self.strip_hp.rect.y = self.rect.y
        else:
            if pygame.sprite.spritecollideany(self, sprites_bullet):
                self.HP -= int(zn)
                if self.HP <= 0:
                    self.kill()
                self.strip_hp.image = pygame.transform.scale(self.strip_hp.image, (self.HP, 5))

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        sprite_reload.add(self)
        self.image = pygame.image.load(sheet)
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.cut_sheet(self.image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.x = x
        self.rect.y = y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, self.rect.size[0] // columns, 
                                self.rect.size[1] // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, *arr):
        if len(arr) == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

def main():
    pygame.init()
    size = width, height
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 70)
    part_window = 0
    jump_event = 30000
    shot_event = 30001
    shot_event2 = 30002
    move_event = 30003
    enemy_event = 30004
    reload_event = 30005
    pygame.time.set_timer(jump_event, 30)
    pygame.time.set_timer(shot_event, 4)
    pygame.time.set_timer(shot_event2, 100)
    pygame.time.set_timer(move_event, 120)
    pygame.time.set_timer(enemy_event, 120)
    pygame.time.set_timer(reload_event, 105)
    running, draw = True, False
    while running:
        if part_window == 0:
            screen.fill((100, 100, 200))
            pos = [(100, 100), (120, 45)]
            pygame.draw.rect(screen, pygame.Color('green'), pos, 0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    coord = event.pos
                    if 100 <= coord[0] <= 200 and 100 <= coord[1] <= 200:
                        part_window = 1
            screen.blit(font.render('Start', True, pygame.Color('red')), (100, 100))
        elif part_window == 1:
            if not draw:
                coord = X, Y = 0, 0
                sp_x, sp_y, jump_speed, gravity = 0, 0, -10, 1
                count_reload, reload = 0, False
                reload_screen = AnimatedSprite(filename_reload, 2, 4, 10, 0)
                text_count_reload = pygame.font.Font(None, 50)
                running, press, jump, rotate = True, False, False, False
                rotate_hero = 'r'
                old_x = 0
                now_herofile = filename_hero
                #-----------------------------
                hero1 = Hero(filename_hero, 100)
                Platform((100, 300), (300, 2))
                sprite_barrier.add(Platform((100, 200), (100, 3)))
                sprite_barrier.add(Platform((250, 100), (100, 3)))
                Platform((-100, 600), (1100, 2))
                sprite_barrier.add(Platform((300, 450), (200, 3)))
                Enemy((800, 450), (100, 200))
                Enemy((400, 200), (100, 200))
                Draw(filename_exit, 940, 0, (20, 20))
                #--------------------------------
                ghost_sprite.image = pygame.Surface([hero1.rect.size[0], 10])
                ghost_sprite.rect = pygame.Rect(0, 0, hero1.rect.size[0], 10)
                draw = True
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
                    if 940 <= event.pos[0] <= 960 and 0 <= event.pos[1] <= 20:
                        part_window = 2
                        continue
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
                    elif event.key == pygame.K_r:
                        count_reload = 0
                        reload = True
                if event.type == shot_event:
                    sprites_bullet.update()
                if event.type == enemy_event:
                    sprite_enemy.update(0)
                if event.type == shot_event2:
                    if not reload and press:
                        count_reload += 1
                        Bullet(filename_bullet, (X+20, Y+10), mouse_pos)
                    if reload:
                        count_reload += 1
                    if not reload and count_reload == 20:
                        reload = True
                        count_reload = 0
                    elif reload and count_reload == 10:
                        reload = False
                        count_reload = 0
                if jump and event.type == jump_event:
                    jump_speed += gravity
                    if pygame.sprite.spritecollideany(ghost_sprite, sprites_platform):
                        jump_speed = 1
                    if jump_speed > 10 and pygame.sprite.spritecollideany(hero1, sprites_platform):
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
                if event.type == reload_event:
                    reload_screen.update()
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
            if pygame.sprite.spritecollideany(hero1, sprite_enemy):
                hero1.damage(1)
            sprites_bullet.draw(screen)
            sprite_enemy.draw(screen)
            all_sprite.draw(screen)
            all_sprite.update(sp_x, sp_y, rotate)
            if not reload:
                screen.blit(text_count_reload.render(str(20-count_reload), True, pygame.Color('red')), (20, 0))
            else:
                sprite_reload.draw(screen)
            if hero1 not in all_sprite:
                part_window = 2
        elif part_window == 2:
            image_game_over = pygame.image.load(filename_game_over).convert_alpha()
            image_game_over.set_colorkey((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    part_window = 0
                    all_sprite.empty()
                    sprites_bullet.empty()
                    sprites_platform.empty()
                    sprite_barrier.empty()
                    sprite_enemy.empty()
                    sprite_reload.empty()
                    draw = False
            screen.blit(image_game_over, (120, 120))
            screen.blit(font.render('Нажмите на любое место', True, pygame.Color('red')), (100, 595))
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()
            

if __name__ == '__main__':
    sys.exit(main())
