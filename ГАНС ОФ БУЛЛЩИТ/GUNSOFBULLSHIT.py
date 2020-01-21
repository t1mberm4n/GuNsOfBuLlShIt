import pygame

from player import *
from blocks import *
from monsters import *

pygame.init()
WIN_WIDTH = 900
WIN_HEIGHT = 800
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#200000"

FILE_DIR = os.path.dirname(__file__)
print(FILE_DIR)

LEVELS = [1, 2, 1]


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
        print(self.state, type(self.state))

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)
    l = max(-(camera.width-WIN_WIDTH), l)
    t = max(-(camera.height-WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h) 


def loadLevel(lev):
    global playerX, playerY
    if level:
        level.clear()
        entities.empty()
        animatedEntities.empty()
        monsters.empty()
        platforms.clear()

    levelFile = open('levels/'+str(lev)+'.txt')
    line = " "
    commands = []
    while line[0] != "/":
        line = levelFile.readline()
        if line[0] == "[":
            while line[0] != "]":
                line = levelFile.readline()
                if line[0] != "]":
                    endLine = line.find("|")
                    level.append(line[0: endLine])
                    
        if line[0] != "":
            commands = line.split()
            if len(commands) > 1:
                if commands[0] == "player":
                    playerX= int(commands[1])
                    playerY = int(commands[2])
                if commands[0] == "portal":
                    tp = BlockTeleport(int(commands[1]),int(commands[2]),int(commands[3]),int(commands[4]))
                    entities.add(tp)
                    platforms.append(tp)
                    animatedEntities.add(tp)
                if commands[0] == "monster":
                    mn = Monster(int(commands[1]),int(commands[2]),int(commands[3]),int(commands[4]),int(commands[5]),int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)

def main():
    
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("ГАНС ОФ БУЛЛЩИТ")
    
    font=pygame.font.Font(None,40)
    
    hero = Player()
    
    for lev in LEVELS:
        if hero.lifes < 0:
            sys.exit()
            
        loadLevel(lev)
        
        bg = Surface((WIN_WIDTH,WIN_HEIGHT))

        bg.fill(Color(BACKGROUND_COLOR))
        
        left = right = False
        up = False
        running = False

        
        hero.startX = playerX
        hero.startY = playerY
        hero.newlevel()
        
        entities.add(hero)
           
        timer = pygame.time.Clock()
        x=y=0
        for row in level:
            for col in row:
                if col == "-":
                    pf = Platform(x,y)
                    entities.add(pf)
                    platforms.append(pf)
                if col == "*":
                    bd = BlockDie(x,y)
                    entities.add(bd)
                    platforms.append(bd)
                if col == "C":
                    co = Coin(x,y)
                    entities.add(co)
                    platforms.append(co)
                    animatedEntities.add(co)
                if col == "P":
                    pr = Princess(x,y)
                    entities.add(pr)
                    platforms.append(pr)
                    animatedEntities.add(pr)
   
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0
    
        total_level_width  = len(level[0])*PLATFORM_WIDTH
        total_level_height = len(level)*PLATFORM_HEIGHT
    
        camera = Camera(camera_configure, total_level_width, total_level_height) 
    
        while not hero.winner:
            timer.tick(60)
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()

                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                if e.type == KEYDOWN and e.key == K_LSHIFT:
                    running = True

                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYUP and e.key == K_LSHIFT:
                    running = False

            screen.blit(bg, (0,0))

            animatedEntities.update()
            monsters.update(platforms)
            camera.update(hero)
            hero.update(left, right, up, running, platforms, entities)
            for e in entities:
                screen.blit(e.image, camera.apply(e))
            text2 = font.render(("Очки прокрастинации: " + str(hero.coins)+"  Жизни: " + str(hero.lifes)), 1,(255,255,255))
            screen.blit(text2, (10,10))
            pygame.display.update()
     

        text=font.render(("Спасибо Работяга! Принцесса на следущем уровне! ( нет)"), 1,(255,255,255))
        text1 = font.render(("Вы собрали " + str(hero.coins) + " очков прокрастинации.'"), 1,(255,255,255))
        screen.blit(text, (40,100))
        screen.blit(text1, (40,200))
        pygame.display.update()
        time.wait(3228)
     
    if hero.coins:
        print('Поздравляем! Вы собрали ', hero.coins,' очков прокрастинации.',)

level = []
entities = pygame.sprite.Group()
animatedEntities = pygame.sprite.Group()
monsters = pygame.sprite.Group()
platforms = []

if __name__ == "__main__":
    main()
