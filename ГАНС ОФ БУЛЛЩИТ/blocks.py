

from pygame import *
import os
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#009900"
ICON_DIR = os.path.dirname(__file__)

ANIMATION_BLOCKTELEPORT = [
            ('%s/blocks/portalb1.png' % ICON_DIR),
            ('%s/blocks/portalb2.png' % ICON_DIR),
            ('%s/blocks/portalb3.png' % ICON_DIR),
            ('%s/blocks/portalb4.png' % ICON_DIR)]

ANIMATION_PRINCESS = [
            ('%s/blocks/princess_l.png' % ICON_DIR),
            ('%s/blocks/princess_r.png' % ICON_DIR)]

ANIMATION_COIN = [
            ('%s/blocks/coin9.png' % ICON_DIR),
            ('%s/blocks/coin9.png' % ICON_DIR)]
            
 
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/bedrock.jpg" % ICON_DIR)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        
class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/lava 0.jpg" % ICON_DIR)

class BlockTeleport(Platform):
    def __init__(self, x, y, goX,goY):
        Platform.__init__(self, x, y)
        self.goX = goX
        self.goY = goY
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        
class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x,y)
        boltAnim = []
        for anim in ANIMATION_PRINCESS:
            boltAnim.append((anim, 0.8))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        

class Coin(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_COIN:
            boltAnim.append((anim, 0.1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))