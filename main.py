import pygame as pg
import sys
import time
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH+100, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.drag=False
        self.load_data()
        self.speed=0
        self.startx=100
        self.starty=100
        self.complete=False
        self.finding=False
        self.rightclickCount=0

    def load_data(self):
        pass

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.borders = pg.sprite.Group()
        self.destinations = pg.sprite.Group()
        for x in range(0,GRIDHEIGHT-1):
            Dest(self,0,x)
        for x in range(1,GRIDWIDTH-1):
            Dest(self,x,0)
        for x in range(0,GRIDWIDTH):
            Dest(self,x,GRIDHEIGHT-1)
        for x in range(0,GRIDHEIGHT):
            Dest(self,GRIDWIDTH-1,x)
        self.quitBtn=Button(self,GRIDWIDTH,GRIDHEIGHT-2,'Quit')
        self.infostring='Start by right   clicking a tile  to set it as the start node. Then right click      another tile to  set it as the    target node. You can then left    click and drag to create walls.   Once all walls   and nodes are    set up, press    enter to start.'
        self.infolist=[self.infostring[i:i+17] for i in range(0, len(self.infostring), 17)]
        self.linecount=0
        for i in self.infolist:
            Info(self,GRIDWIDTH,self.linecount,i,DARKGREY,13)
            self.linecount+=0.5
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) /1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        time.sleep(self.speed)


    def found(self):
        self.finding=False
        self.complete=True
        path=self.player.getWall(self.destination.x,self.destination.y).shortestpath
        for x in path[1:]:
            j=x.split(",")
            Dest(self,int(j[0]),int(j[1]),PINK)
            self.update()
            self.draw()
        Destination(self,self.destination.x,self.destination.y)
        self.update()
        self.draw()
    def events(self):
            for event in pg.event.get():
                if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
                    mouse_x,mouse_y=(pg.mouse.get_pos())
                    if mouse_y//TILESIZE>=self.quitBtn.y and mouse_x//TILESIZE>=self.quitBtn.x:
                        self.quit()
                if not(self.finding) and not(self.complete):
                    if event.type == pg.MOUSEMOTION:
                        if self.drag:
                            mouse_x,mouse_y=(pg.mouse.get_pos())
                            try:
                                if mouse_x//TILESIZE!=self.destination.x or mouse_y//TILESIZE!=self.destination.y:
                                    if mouse_x//TILESIZE!=self.startx or mouse_y//TILESIZE!=self.starty:  
                                        if (mouse_y//TILESIZE<23 and mouse_x//TILESIZE<31) and (mouse_y//TILESIZE>0 and mouse_x//TILESIZE>0): 
                                            Dest(self,mouse_x//TILESIZE,mouse_y//TILESIZE)
                            except AttributeError:
                                pass
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                            self.start()
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.drag=True
                        mouse_x,mouse_y=(pg.mouse.get_pos())
                        try:
                            if mouse_x//TILESIZE!=self.destination.x or mouse_y//TILESIZE!=self.destination.y:
                                if mouse_x//TILESIZE!=self.startx or mouse_y//TILESIZE!=self.starty:  
                                    if (mouse_y//TILESIZE<23 and mouse_x//TILESIZE<31) and (mouse_y//TILESIZE>0 and mouse_x//TILESIZE>0): 
                                        Dest(self,mouse_x//TILESIZE,mouse_y//TILESIZE)
                        except AttributeError:
                            pass

                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                        if self.rightclickCount==0:
                            mouse_x,mouse_y=(pg.mouse.get_pos())
                            if (mouse_y//TILESIZE<23 and mouse_x//TILESIZE<31) and (mouse_y//TILESIZE>0 and mouse_x//TILESIZE>0):  
                                self.player = Player(self, mouse_x//TILESIZE, mouse_y//TILESIZE) 
                                self.player.x=mouse_x//TILESIZE 
                                self.player.y=mouse_y//TILESIZE 
                                self.startx=self.player.x
                                self.starty=self.player.y
                                Wall(self,self.player.x,self.player.y,[],BLUE)
                                self.rightclickCount+=1
                        else:
                            if self.rightclickCount==1:
                                mouse_x,mouse_y=(pg.mouse.get_pos())
                                if (mouse_y//TILESIZE<23 and mouse_x//TILESIZE<31) and (mouse_y//TILESIZE>0 and mouse_x//TILESIZE>0) and (mouse_x//TILESIZE!=self.player.x or mouse_y//TILESIZE!=self.player.y) :   
                                    self.destination=Destination(self,mouse_x//TILESIZE,mouse_y//TILESIZE)
                                    self.rightclickCount+=1

                    if event.type == pg.MOUSEBUTTONUP and event.button==1:
                        self.drag=False
    def start(self):
        self.finding=True
        while self.finding:
            self.speed=0.03
            for wall in self.walls:
                if wall.edgepiece:
                    self.player.x=wall.x
                    self.player.y=wall.y 
                    if self.player.checkCollide(dx=1):
                        Wall(self,self.player.x+1,self.player.y,self.player.getWall(self.player.x,self.player.y).shortestpath+[(str(self.player.x)+','+str(self.player.y))])
                        self.update()
                        self.draw()
                        if wall.x+1==self.destination.x and wall.y==self.destination.y:
                            self.playing=False
                            self.found()
                            break
                    if self.player.checkCollide(dy=-1):
                        Wall(self,self.player.x,self.player.y-1,self.player.getWall(self.player.x,self.player.y).shortestpath+[(str(self.player.x)+','+str(self.player.y))])
                        self.update()
                        self.draw()
                        if wall.x==self.destination.x and wall.y-1==self.destination.y:
                            self.playing=False
                            self.found()
                            break
                    if self.player.checkCollide(dy=1):
                        Wall(self,self.player.x,self.player.y+1,self.player.getWall(self.player.x,self.player.y).shortestpath+[(str(self.player.x)+','+str(self.player.y))])
                        self.update()
                        self.draw()
                        if wall.x==self.destination.x and wall.y+1==self.destination.y:
                            self.playing=False
                            self.found()
                            break
                    if(self.player.checkCollide(dx=-1)):
                        Wall(self,self.player.x-1,self.player.y,self.player.getWall(self.player.x,self.player.y).shortestpath+[(str(self.player.x)+','+str(self.player.y))])
                        self.update()
                        self.draw()
                        if wall.x-1==self.destination.x and wall.y==self.destination.y:
                            self.playing=False
                            self.found()
                            break
                    wall.edgepiece=False



g = Game()
g.new()
while True:
    g.events()
    g.update()
    g.draw()

