import os
from os import path

from tkinter import *
from tkinter import messagebox

import pygame

FPS = 50
LVL_DICT = {'lvl_play_1.txt': 'lvl_map_1.txt', 'lvl_play_2.txt': 'lvl_map_2.txt', 'lvl_play_3.txt': 'lvl_map_3.txt',
            'lvl_play_4.txt': 'lvl_map_4.txt', 'lvl_play_5.txt': 'lvl_map_5.txt', 'lvl_play_6.txt': 'lvl_map_6.txt'}
SCORE_DICT = {1: 10, 2: 10, 3: 20, 4: 20, 5: 20, 6: 20}
OPTIMAL_MOVES = {1: 21, 2: 20, 3: 16, 4: 26, 5: 41, 6: 66}


img_dir = path.join(path.dirname(__file__), 'data', 'img')
snd_dir = path.join(path.dirname(__file__), 'data', 'snd')


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(width, height):
    clock = pygame.time.Clock()
    intro_text = ["Логическая игра, которая заставит ваc подумать",
                  "Помоги зайчику посадить морковку", "",
                  "Для продолжения нажмите любую клавишу"]
    fon = pygame.transform.scale(load_image(path.join(img_dir, 'fon.jpg')), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 350
    string_rendered = font.render('Зайка Велиар', 1, pygame.Color('white'))
    screen.blit(string_rendered, [150, 20])
    font = pygame.font.Font(None, 30)
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.mixer.music.load(path.join(snd_dir, 'fon_music.wav'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(width, height, score):
    clock = pygame.time.Clock()
    intro_text = ["", "Поздравляем!", "",
                  "Вы прошли игру",
                  "Ваш IQ 337",
                  "Ваш счет: " + str(score),
                  "",
                  "Нажмите пробел, чтобы играть заново"]
    fon = pygame.transform.scale(load_image(path.join(img_dir, 'fon.jpg')), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.mixer.music.load(path.join(snd_dir, 'fon_music.wav'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return start_screen(width, height)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name):
    fullname = path.join(img_dir, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    if not os.path.isfile(filename):
        print("Файл не найден")
        sys.exit()
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image(path.join(img_dir, 'barrier.png')),
    'empty': load_image(path.join(img_dir, 'grass.png')),
    'pit': load_image(path.join(img_dir, 'pit.png')),
    'button': load_image(path.join(img_dir, 'bt_restart.jpg'))
}
player_image = load_image(path.join(img_dir, 'rabbit.png'))
carrot_image = load_image(path.join(img_dir, 'carrot.png'))
tile_width = tile_height = 64


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def get_x(self):
        return self.pos_x + 1

    def get_y(self):
        return self.pos_y + 1


class Carrot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(object_group, all_sprites)
        self.image = carrot_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def get_x(self):
        return self.pos_x + 1

    def get_y(self):
        return self.pos_y + 1


player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '0':
                Tile('pit', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Tile('pit', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                new_carrot = Carrot(x, y)
            elif level[y][x] == '%':
                Tile('pit', x, y)
                new_carrot = Carrot(x, y)
    Tile('button', 0, y + 1)
    return new_player, new_carrot, x + 1, y + 2, level


def move_player(file_r, pos_x, pos_y, fname, height, wight, x=0, y=0):
    update = True
    line = ''
    if x == 1 and pos_x < wight:
        if pos_x == len(file_r[pos_y - 1]):
            update = False
        elif file_r[pos_y - 1][pos_x] != '#':
            if (file_r[pos_y - 1][pos_x] != '*' and file_r[pos_y - 1][pos_x] != '%') or \
                    ((file_r[pos_y - 1][pos_x] == '*' or file_r[pos_y - 1][pos_x] == '%') and
                     (file_r[pos_y - 1][pos_x + 1] == '0' or file_r[pos_y - 1][pos_x + 1] == '.')):
                if file_r[pos_y - 1][pos_x - 1] == '$':
                    line = file_r[pos_y - 1][:pos_x - 1] + '0' + file_r[pos_y - 1][pos_x:]
                else:
                    line = file_r[pos_y - 1][:pos_x - 1] + '.' + file_r[pos_y - 1][pos_x:]
                if file_r[pos_y - 1][pos_x] == '*' or file_r[pos_y - 1][pos_x] == '%':
                    if file_r[pos_y - 1][pos_x + 1] != '0':
                        line = line[:pos_x + 1] + '*' + line[pos_x + 2:]
                    else:
                        line = line[:pos_x + 1] + '%' + line[pos_x + 2:]
                if file_r[pos_y - 1][pos_x] != '0' and file_r[pos_y - 1][pos_x] != '%':
                    line = line[:pos_x] + '@' + line[pos_x + 1:]
                else:
                    line = line[:pos_x] + '$' + line[pos_x + 1:]
            else:
                update = False
        else:
            update = False
    elif x == -1 and pos_x > 1 and file_r[pos_y - 1][pos_x - 2] != '#':
        if (file_r[pos_y - 1][pos_x - 2] != '*' and file_r[pos_y - 1][pos_x - 2] != '%') or \
                ((file_r[pos_y - 1][pos_x - 2] == '*' or file_r[pos_y - 1][pos_x - 2] == '%') and
                 (file_r[pos_y - 1][pos_x - 3] == '0' or file_r[pos_y - 1][pos_x - 3] == '.')):
            if file_r[pos_y - 1][pos_x - 1] == '$':
                line = file_r[pos_y - 1][:pos_x - 1] + '0' + file_r[pos_y - 1][pos_x:]
            else:
                line = file_r[pos_y - 1][:pos_x - 1] + '.' + file_r[pos_y - 1][pos_x:]
            if file_r[pos_y - 1][pos_x - 2] == '*' or file_r[pos_y - 1][pos_x - 2] == '%':
                if file_r[pos_y - 1][pos_x - 3] != '0':
                    line = line[:pos_x - 3] + '*' + line[pos_x - 2:]
                else:
                    line = line[:pos_x - 3] + '%' + line[pos_x - 2:]
            if file_r[pos_y - 1][pos_x - 2] != '0' and file_r[pos_y - 1][pos_x - 2] != '%':
                line = line[:pos_x - 2] + '@' + line[pos_x - 1:]
            else:
                line = line[:pos_x - 2] + '$' + line[pos_x - 1:]
        else:
            update = False
    elif y == -1 and pos_y > 1 and file_r[pos_y-2][pos_x - 1] != '#':
        if (file_r[pos_y - 2][pos_x - 1] != '*' and file_r[pos_y - 2][pos_x - 1] != '%') or\
                ((file_r[pos_y - 2][pos_x - 1] == '*' or file_r[pos_y - 2][pos_x - 1] == '%') and
                 (file_r[pos_y - 3][pos_x - 1] == '0' or file_r[pos_y - 3][pos_x - 1] == '.')):
            if file_r[pos_y - 1][pos_x - 1] == '$':
                line_nearby = file_r[pos_y - 1][:pos_x - 1] + '0' + file_r[pos_y - 1][pos_x:]
            else:
                line_nearby = file_r[pos_y - 1][:pos_x - 1] + '.' + file_r[pos_y - 1][pos_x:]
            if file_r[pos_y-2][pos_x - 1] == '*' or file_r[pos_y-2][pos_x - 1] == '%':
                if file_r[pos_y - 3][pos_x - 1] != '0':
                    line_next = file_r[pos_y - 3][:pos_x - 1] + '*' + file_r[pos_y - 3][pos_x:]
                else:
                    line_next = file_r[pos_y - 3][:pos_x - 1] + '%' + file_r[pos_y - 3][pos_x:]
            else:
                line_next = file_r[pos_y - 3]
            if file_r[pos_y - 2][pos_x - 1] != '0' and file_r[pos_y - 2][pos_x - 1] != '%':
                line = file_r[pos_y - 2][:pos_x - 1] + '@' + file_r[pos_y - 2][pos_x:]
            else:
                line = file_r[pos_y - 2][:pos_x - 1] + '$' + file_r[pos_y - 2][pos_x:]
        else:
            update = False
    elif y == 1 and pos_y < height and file_r[pos_y][pos_x - 1] != '#':
        if (file_r[pos_y][pos_x - 1] != '*' and file_r[pos_y][pos_x - 1] != '%') or \
                ((file_r[pos_y][pos_x - 1] == '*' or file_r[pos_y][pos_x - 1] == '%') and
                 (file_r[pos_y + 1][pos_x - 1] == '0' or file_r[pos_y + 1][pos_x - 1] == '.')):
            if file_r[pos_y - 1][pos_x - 1] == '$':
                line_nearby = file_r[pos_y - 1][:pos_x - 1] + '0' + file_r[pos_y - 1][pos_x:]
            else:
                line_nearby = file_r[pos_y - 1][:pos_x - 1] + '.' + file_r[pos_y - 1][pos_x:]
            if file_r[pos_y][pos_x - 1] == '*' or file_r[pos_y][pos_x - 1] == '%':
                if file_r[pos_y + 1][pos_x - 1] != '0':
                    line_next = file_r[pos_y + 1][:pos_x - 1] + '*' + file_r[pos_y + 1][pos_x:]
                else:
                    line_next = file_r[pos_y + 1][:pos_x - 1] + '%' + file_r[pos_y + 1][pos_x:]
            else:
                line_next = file_r[pos_y + 1]
            if file_r[pos_y][pos_x - 1] != '0' and file_r[pos_y][pos_x - 1] != '%':
                line = file_r[pos_y][:pos_x - 1] + '@' + file_r[pos_y][pos_x:]
            else:
                line = file_r[pos_y][:pos_x - 1] + '$' + file_r[pos_y][pos_x:]
        else:
            update = False
    else:
        update = False
    if update:
        with open("data/" + fname, "w", encoding="utf8") as file_w:
            for i in range(len(file_r)):
                if y == - 1 and i == pos_y - 2 and line != '':
                    file_w.write(line)
                elif y == -1 and i == pos_y - 1 and line != '':
                    file_w.write(line_nearby)
                elif y == -1 and i == pos_y - 3 and line != '':
                    file_w.write(line_next)
                elif y == 1 and i == pos_y and line != '':
                    file_w.write(line)
                elif y == 1 and i == pos_y - 1 and line != '':
                    file_w.write(line_nearby)
                elif y == 1 and i == pos_y + 1 and line != '':
                    file_w.write(line_next)
                elif (x == 1 or x == -1) and i == pos_y - 1 and line != '':
                    file_w.write(line)
                else:
                    file_w.write(file_r[i])
                if i != len(file_r) - 1:
                    file_w.write('\n')

    return update


def count_scores(nm_lvl, quan_moves):
    if OPTIMAL_MOVES[nm_lvl] == quan_moves:
        return SCORE_DICT[nm_lvl]
    else:
        if quan_moves - OPTIMAL_MOVES[nm_lvl] <= 5:
            return SCORE_DICT[nm_lvl] - 5
        else:
            return SCORE_DICT[nm_lvl] - 10

def reset_lvl(nm_lvl):
    file = open("data/" + LVL_DICT[nm_lvl], 'r', encoding='utf-8')
    lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]
    file_w = open("data/" + nm_lvl, "w", encoding="utf8")
    for i in range(len(lines)):
        file_w.write(lines[i])
        if i != len(lines) - 1:
            file_w.write('\n')
    file.close()
    file_w.close()


def check_win(lvl_chem):
    for el in lvl_chem:
        if '0' in el or '$' in el:
            return False
    return True


def clean_sprites(background):
    for item in tiles_group:
        item.kill()
        tiles_group.clear(screen, background)
    for item in object_group:
        item.kill()
        object_group.clear(screen, background)
    for item in player_group:
        item.kill()
        player_group.clear(screen, background)
    for item in all_sprites:
        item.kill()
        all_sprites.clear(screen, background)


def on_music_play():
    pygame.mixer.music.load(path.join(snd_dir, 'play_music.wav'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)


if __name__ == '__main__':
    pygame.init()
    nm_lvl = 1
    move_counter = 0
    score = 0
    name_file = 'lvl_play_' + str(nm_lvl) + '.txt'
    reset_lvl(name_file)
    player, carrots, level_x, level_y, lvl = generate_level(load_level(name_file))
    size = level_x * tile_width, level_y * tile_height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Зайка Велиар')
    running = True
    clock = pygame.time.Clock()
    x, y = player.get_x(), player.get_y()
    start_screen(size[0], size[1])
    pygame.display.set_caption('Уровень 1')
    expl_sounds = []
    on_music_play()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] >= size[1] - 60 and event.pos[1] <= size[1]:
                    clean_sprites(screen)
                    reset_lvl(name_file)
                    move_counter = 0
                    player, carrots, level_x, level_y, lvl = generate_level(load_level(name_file))
                    x, y = player.get_x(), player.get_y()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if move_player(lvl, x, y, name_file, level_y, level_x, -1):
                        x -= 1
                        move_counter += 1
                        player, carrots, level_x, level_y, lvl = generate_level(load_level(name_file))
                if event.key == pygame.K_RIGHT:
                    if move_player(lvl, x, y, name_file, level_y, level_x, 1):
                        x += 1
                        move_counter += 1
                        player, carrots, level_x, level_y, lvl = generate_level(load_level(name_file))
                if event.key == pygame.K_UP:
                    if move_player(lvl, x, y, name_file, level_y, level_x, 0, -1):
                        y -= 1
                        move_counter += 1
                        player, carrots, level_x, level_y, lvl = generate_level(load_level(name_file))
                if event.key == pygame.K_DOWN:
                    if move_player(lvl, x, y, name_file, level_y, level_x, 0, 1):
                        y += 1
                        move_counter += 1
                        player, carrots, level_x, level_y, lvl = generate_level(load_level(name_file))
            if check_win(lvl):
                Tk().wm_withdraw()
                score += count_scores(nm_lvl, move_counter)
                messagebox.showinfo('Поздравляем!', 'Вы прошли уровень ' + str(nm_lvl) +
                                    '\nХодов: ' + str(move_counter) +
                                    '\nОчков: ' + str(count_scores(nm_lvl, move_counter)))
                move_counter = 0
                clean_sprites(screen)
                if nm_lvl < 6:
                    nm_lvl += 1
                else:
                    pygame.display.set_caption('Зайка Велиар')
                    end_screen(size[0], size[1], score)
                    nm_lvl = 1
                    score = 0
                    on_music_play()
                name_file = 'lvl_play_' + str(nm_lvl) + '.txt'
                reset_lvl(name_file)
                player, carrots, level_x, level_y, lvl = generate_level(load_level(name_file))
                size = level_x * tile_width, level_y * tile_height
                screen = pygame.display.set_mode(size)
                x, y = player.get_x(), player.get_y()
                pygame.display.set_caption('Уровень ' + str(nm_lvl))
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
