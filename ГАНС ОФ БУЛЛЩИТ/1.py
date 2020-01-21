import pygame
import random
import os, sys

# инициализация Pygame:
pygame.init()
# размеры окна:
SCREENSIZE = width, height = 800, 600
# частота кадров
FPS = 60
clock = pygame.time.Clock()

# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(SCREENSIZE)


# формирование кадра:
# команды рисования на холсте

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (width - intro_rect.right) // 2  # 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]


    max_width = max(map(len, level_map))


    return list(map(lambda x: x.ljust(max_width, '.'), level_map))



tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y

    def move(self, tw, th):
        x = self.rect.x
        y = self.rect.y
        self.rect.x += tw
        self.rect.y += th
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0



        collisons = pygame.sprite.groupcollide(player_group, walls_group, False, False)
        if collisons:
            self.rect.x = x
            self.rect.y = y



player = None


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
dragon_group = pygame.sprite.Group()

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, dragon_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.tick_frame = 0
        self.moves = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if not self.moves:
            return
        if self.tick_frame == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.tick_frame = 0
            self.moves = False
        self.tick_frame += 1

    def move(self, tw, th):
        x = self.rect.x
        y = self.rect.y
        self.rect.x += tw
        self.rect.y += th
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        collisons = pygame.sprite.groupcollide(dragon_group, walls_group, False, False)
        if collisons:
            self.rect.x = x
            self.rect.y = y

sprite1 = pygame.transform.scale(load_image("spritesheet.png", -1), (100,100))
dragon = AnimatedSprite(sprite1, 2, 2, 100, 150)

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':

                walls_group.add(Tile('wall', x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)

    return new_player, x, y


class Camera:

    def __init__(self):
        self.dx = 0
        self.dy = 0


    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy



    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


start_screen()
levels = {1: 'level1_mario.txt'}
player, level_x, level_y = generate_level(load_level(levels[1]))

print(level_x, level_y)
camera = Camera()
running = True

x = 100
v = 300

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            dragon.moves = True
            if event.key == pygame.K_UP:
                player.move(0, -tile_height)
            elif event.key == pygame.K_DOWN:
                player.move(0, tile_height)
            elif event.key == pygame.K_RIGHT:
                player.move(tile_width, 0)
            elif event.key == pygame.K_LEFT:
                player.move(-tile_width, 0)
            if event.key == pygame.K_w:
                dragon.move(0, -tile_height)
            elif event.key == pygame.K_s:
                dragon.move(0, tile_height)
            elif event.key == pygame.K_d:
                dragon.move(tile_width, 0)
            elif event.key == pygame.K_a:
                dragon.move(-tile_width, 0)


        if event.type == pygame.MOUSEMOTION:
            pygame.draw.circle(screen, (0, 0, 255), event.pos, 5)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass
            if event.button == 4:
                x += v * clock.tick() / 100
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 5:
                x += -v * clock.tick() / 100



    camera.update(dragon)
    for sprite in all_sprites:
        camera.apply(sprite)

    tiles_group.draw(screen)
    player_group.draw(screen)
    dragon_group.draw(screen)
    all_sprites.update()
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
