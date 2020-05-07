import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self):
        if not(self.collideWithWall(dx=1)):
            self.x += 1
        else:
            if not(self.collideWithWall(dy=-1)):
                self.y += -1
            else:
                if not(self.collideWithWall(dy=1)):
                    self.y += 1
                else:
                    if not(self.collideWithWall(dx=-1)):
                        self.x += -1

    def checkCollide(self, dx=0, dy=0):
        if not(self.collideWithWall(dx,dy)):
            return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def collideWithWall(self,dx=0,dy=0):
        for wall in self.game.walls:
            if wall.x==self.x+dx and wall.y==self.y+dy:
                return True
        for dest in self.game.borders:
            if dest.x==self.x+dx and dest.y==self.y+dy:
                return True
    def getWall(self,dx,dy):
        for wall in self.game.walls:
            if wall.x==dx and wall.y==dy:
                return wall
        return False

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y,path=[],color=GREEN):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.shortestpath=path
        self.edgepiece=True



class Dest(pg.sprite.Sprite):
    def __init__(self, game, x, y,color=RED):
        self.groups = game.all_sprites, game.borders
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


            

class Destination(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.destinations
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Button(pg.sprite.Sprite):
    def __init__(self, game, x, y,word='test',color=LIGHTGREY,fontsize=24):
        self.groups = game.all_sprites, game.destinations
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE*3, TILESIZE*2))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        font = pg.font.SysFont('Arial', fontsize)
        text = font.render(word, 1, (255,255,255))
        self.image.blit(text, [TILESIZE-10,TILESIZE/2])
class Info(pg.sprite.Sprite):
    def __init__(self, game, x, y,word='test',color=LIGHTGREY,fontsize=24):
        self.groups = game.all_sprites, game.destinations
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE*3, TILESIZE*2))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        font = pg.font.SysFont('Arial', fontsize)
        text = font.render(word, 1, (255,255,255))
        self.image.blit(text, [0,0])




