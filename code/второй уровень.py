print()
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
filename_bullet = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\bullet.png' 
filename_hero = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\pass2.png'
filename_hero_2 = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\walk3.png'
filename_hero_3 = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\walk4.png'
filename_reload = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\reload.png'
filename_exit = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\exit.png'
filename_background = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\background_level_1.png'
filename_game_over = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\gameover.png'
filename_game_win = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\win2.png'
filename_platform = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\platform.png'
filename_record = r'C:\Users\frozj\OneDrive\Документы\Python\Нужные фото\project\records.txt'
f = open(filename_record, 'r+')
records = {}
records_zn = []
for el in f.read().split('\n'):
    el = el.split()
    records_zn.append(int(el[0]))
    records[el[0]] = el[1]
records_zn.sort()
NAME = input('Введите ник: ')

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
        self.rect = self.image.get_rect()
        self.rotate_k = 'r'
        self.rect.x = 0
        self.rect.y = 500
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
        if self.rect.y > 700:
            self.rect.y = 0

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
            sprite_enemy.update(4, (0, 0))
            self.kill()


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprite)
        sprites_platform.add(self)
        self.image = pygame.image.load(filename_platform).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        if size[0]>100:
            for i in range(size[0]//100):
                Platform((pos[0]+100, pos[1]), (size[0]-100, size[1]))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, speed):
        super().__init__()
        self.HP = size[0]
        sprite_enemy.add(self)
        self.image = pygame.Surface([size[0], size[1]])
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.image.fill(pygame.Color("blue"))
        self.strip_hp = pygame.sprite.Sprite()
        sprite_enemy.add(self.strip_hp)
        self.strip_hp.image = pygame.Surface([size[0], 5])
        self.strip_hp.rect = pygame.Rect(pos[0], pos[1], size[0], 5)
        self.strip_hp.image.fill(pygame.Color("green"))
        self.speed = speed
    
    def update(self, zn, coord):
        if zn == 0:
            if coord[0] < self.rect.x:
                move_x = -self.speed
            elif coord[0] > self.rect.x:
                move_x = self.speed
            else:
                move_x = 0
            if coord[1] < self.rect.y:
                move_y = -self.speed
            elif coord[1] > self.rect.y:
                move_y = self.speed
            else:
                move_y = 0
            self.rect = self.rect.move(move_x, move_y)
            if self.rect.x < 0:
                self.rect.x = 960
            self.strip_hp.rect.x = self.rect.x
            self.strip_hp.rect.y = self.rect.y
        else:
            if pygame.sprite.spritecollideany(self, sprites_bullet):
                self.HP -= int(zn)
                if self.HP <= 0:
                    self.kill()
                    self.strip_hp.kill()
                else:
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
    global records_zn, records
    pygame.init()
    size = width, height
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 70)
    font_2 = pygame.font.Font(None, 20)
    part_window = 0
    jump_event = 30000
    shot_event = 30001
    shot_event2 = 30002
    move_event = 30003
    enemy_event = 30004
    reload_event = 30005
    timer_event = 30006
    pygame.time.set_timer(jump_event, 40)
    pygame.time.set_timer(shot_event, 4)
    pygame.time.set_timer(shot_event2, 100)
    pygame.time.set_timer(move_event, 130)
    pygame.time.set_timer(enemy_event, 120)
    pygame.time.set_timer(reload_event, 105)
    pygame.time.set_timer(timer_event, 1000)
    running, draw = True, False
    result = None
    part_draw = 0
    wait_f = False
    while running:
        if part_window == 0:
            screen.fill((100, 100, 200))
            y = 0
            for el in records_zn:
                screen.blit(font_2.render(f'{records[str(el)]} {str(el)}', True, pygame.Color('red')), (700, y))
                y += 10
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
                #background = pygame.image.load(filename_background)
                hero1 = Hero(filename_hero, 100)
                if part_draw == 0:
                    count_finish = 0
                    timer = 0
                    Platform((0, 600), (100, 10))
                    Platform((860, 600), (100, 10))
                    Platform((150, 500), (100, 10))
                    Platform((300, 600), (200, 10))
                    Platform((220, 250), (100, 10))
                    Platform((450, 400), (200, 10))
                    Platform((600, 150), (200, 10))
                    Enemy((400, 20), (25, 25), 10)
                    Enemy((400, 570), (50, 50), 7)
                    Enemy((890, 570), (50, 50), 7)
                    Draw(filename_exit, 940, 0, (20, 20))
                elif part_draw == 1:
                    Platform((100, 300), (300, 10))
                    Platform((100, 200), (100, 10))
                    Platform((250, 100), (100, 10))
                    Platform((0, 600), (500, 10))
                    Platform((500, 600), (500, 10))
                    Platform((700, 450), (100, 10))
                    Platform((600, 300), (100, 10))
                    Platform((300, 450), (200, 10))
                    Enemy((400, 450), (25, 25), 4)
                    Enemy((400, 200), (25, 25), 6)
                    Draw(filename_exit, 940, 0, (20, 20))
                #--------------------------------
                ghost_sprite.image = pygame.Surface([hero1.rect.size[0], 10])
                ghost_sprite.rect = pygame.Rect(0, 0, hero1.rect.size[0], 10)
                draw = True
                
            if len(sprite_enemy) == 0:
                if count_finish == 0:
                    count_finish += 1
                    Enemy((20, 20), (25, 25), 10)
                    Enemy((20, 570), (50, 50), 7)
                    Enemy((890, 570), (50, 50), 7)
                elif count_finish == 1:
                    wait_f = True
                elif count_finish == 2:
                    count_finish += 1
                    Enemy((20, 20), (25, 25), 10)
                    Enemy((890, 20), (20, 20), 20)
                    Enemy((20, 570), (50, 50), 7)
                    Enemy((890, 570), (50, 50), 7)
                elif count_finish == 3:
                    part_window = 2
                    result = 'win'
                    continue    
            coord = X, Y = hero1.rect.x, hero1.rect.y
            ghost_sprite.rect = ghost_sprite.rect.move(X-ghost_sprite.rect.x, Y-ghost_sprite.rect.y)
            ghost_sprite.rect.x = X
            ghost_sprite.rect.y = Y
            #screen.blit(background, (0, 0))
            screen.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if wait_f:
                    screen.blit(font.render('Нажмите на клавишу F', True, pygame.Color('red')), (170, 560))
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:
                            all_sprite.empty()
                            sprites_bullet.empty()
                            sprites_platform.empty()
                            sprite_barrier.empty()
                            sprite_enemy.empty()
                            sprite_reload.empty()
                            draw = False
                            count_finish += 1
                            part_draw = 1
                            wait_f = False
                        else:
                            continue
                    else:
                        continue
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    press = True
                    if 940 <= event.pos[0] <= 960 and 0 <= event.pos[1] <= 20:
                        sprite_enemy.empty()
                        part_window = 2
                        result = 'loss'
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
                    elif event.key == pygame.K_r:
                        count_reload = 0
                        reload = True
                if event.type == shot_event:
                    sprites_bullet.update()
                if event.type == enemy_event:
                    sprite_enemy.update(0, coord)
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
                    if jump_speed > 5 and pygame.sprite.spritecollideany(hero1, sprites_platform):
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
                if event.type == timer_event:
                    timer += 1
            #---------------------------------
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if sp_x != -4 and rotate_hero == 'r':
                    rotate = True
                    rotate_hero = 'l'
                else:
                    rotate = False
                sp_x = -4
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if sp_x != 4 and rotate_hero == 'l':
                    rotate = True
                    rotate_hero = 'r'
                else:
                    rotate = False
                sp_x = 4
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
            all_sprite.draw(screen)
            all_sprite.update(sp_x, sp_y, rotate)
            sprites_bullet.draw(screen)
            sprite_enemy.draw(screen)
            if not reload:
                screen.blit(text_count_reload.render(str(20-count_reload), True, pygame.Color('red')), (20, 0))
            else:
                sprite_reload.draw(screen)
            if hero1 not in all_sprite and draw:
                part_window = 2
                result = 'loss'
            screen.blit(text_count_reload.render(str(timer), True, pygame.Color('red')), (900, 0))
        elif part_window == 2:
            if result == 'win':
                image_game_win = pygame.image.load(filename_game_win).convert_alpha()
                image_game_win = pygame.transform.scale(image_game_win, (width, height))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and draw:
                        records[str(timer)] = NAME
                        records_zn.append(int(timer))
                        records_zn.sort()
                        f.write(f'\n{timer} {NAME}')
                        part_window = 0
                        all_sprite.empty()
                        sprites_bullet.empty()
                        sprites_platform.empty()
                        sprite_barrier.empty()
                        sprite_enemy.empty()
                        sprite_reload.empty()
                        draw = False
                screen.blit(image_game_win, (0, 0))
                screen.blit(font.render('Нажмите на любое место', True, pygame.Color('red')), (100, 595))
            elif result == 'loss':
                image_game_over = pygame.image.load(filename_game_over).convert_alpha()
                image_game_over = pygame.transform.scale(image_game_over, (width, height))
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
                screen.blit(image_game_over, (0, 0))
                screen.blit(font.render('Нажмите на любое место', True, pygame.Color('red')), (190, 595))
            count_finish = 0
            timer = 0
        pygame.display.flip()
        clock.tick(100)
    f.close()
    pygame.quit()
            

if __name__ == '__main__':
    sys.exit(main())
