import random
import math
import pygame
class RRTMap:
    def __init__(self,start,goal,MapDimentions,obsdim,obsnum):
        self.start=start
        self.goal=goal
        self.MapDimentions=MapDimentions
        self.Maph,self.mapw=MapDimentions

        #windows settings
        self.map=pygame.display.set_mode((self.mapw,self.Maph))
        pygame.display.set_caption('RRT path planing')
        self.map.fill((255, 255, 255))
        self.nodeRad=2
        self.nodeThickness=0
        self.edgeThickness=1
        self.obstacles=[]
        self.obsnum=obsnum
        self.obsdim=obsdim

        #color
        self.grey=(70,70,70)
        self.blue=(0,0,255)
        self.green=(0,255,0)
        self.red=(255,0,0)
        self.white=(255,255,255)
        

    def drawMap(self,obstacles):
        pygame.draw.circle(self.map,self.green,self.start,self.nodeRad+5,0)
        pygame.draw.circle(self.map,self.green,self.goal,self.nodeRad+20,1)
        self.drawObs(obstacles)


    def  drawPath (self):
        pass
    def drawObs (self,obstacles):
        obstaclesList=obstacles.copy()
        while(len(obstaclesList)>0):
            obstacles=obstaclesList.pop(0)
            pygame.draw.rect(self.map,self.grey,obstacles)


class RRTGraph:
    def __init__(self,start,goal,MapDimentions,obsdim,obsnum):
        (x,y)=start
        self.start=start
        self.goal=goal
        self.goalFLage=False
        self.Maph,self.mapw=MapDimentions
        self.x=[]
        self.y=[]
        self.parent=[]

        #init the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        #the obs
        self.obstacles=[]
        self.obsnum=obsnum
        self.obsdim=obsdim

        #path
        self.goalstate=None
        self.path=[]


    def makeRandomRect(self):
        uppercornerx=int(random.randint(0,self.mapw-self.obsdim))
        uppercornery=int(random.randint(0,self.mapw-self.obsdim))
        return (uppercornerx,uppercornery)


    def MakeObs(self):
        obs=[]
        for i in range(0,self.obsnum):
            rectang=None
            startgoalcol = True
            while startgoalcol:
                upper=self.makeRandomRect()
                rectang=pygame.Rect(upper,(self.obsdim,self.obsdim))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol=True
                else:
                    startgoalcol=False
            obs.append(rectang)
        self.obstacles=obs.copy()
        return obs

    def add_node (self,n,x,y):
        self.x.insert(n,x)
        self.y.append(y)


    def remove_node (self,n):
        self.x.pop(n)
        self.y.pop(n)


    def add_edge(self,parent,child):
        self.parent.insert(child,parent)

    def remove_edge(self,parent,n):
        self.parent.popn()


    def number_of_nodes(self):
        return len(self.x)


    def distance (self,n1,n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        px=(float(x1)-float(x2))**2
        py=(float(y1)-float(y2))**2
        return (px+py)**0.5


    def sample_evir(self):
        x=int(random.randint(0,self.mapw))   
        y=int(random.randint(0,self.Maph)) 
        return x,y


    def nearst (self):
        pass
    def isFree (self):
        n=self.number_of_nodes()-1
        (x,y)=(self.x[n],self.y[n])
        obs=self.obstacles.copy()
        while len(obs)>0:
            rectang=obs.pop(0)
            if rectang.collidepoint(x,y):
                self.remove_node(n)
                return False
        return True


    def crossObstacle (self,x1,x2,y1,y2):
        obs=self.obstacles.copy()
        while len(obs)>0:
            rectang=obs.pop(0)
            for i in range(0,101):
                u=i/100
                x=x1*u+x2*(1-u)
                y=y1*u+y2*(1-u)
                if rectang.collidepoint(x,y):
                    return True
        return False
    def connect (self):
        (x1,y1)=(self.x1[n1],self.y1[n1])
        (x2,y2)=(self.x2[n2],self.y2[n2])
        if self.crossObstacle(x1,x2,y1,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1,n2)
            return True
            

    def step (self):
        pass
    def pass_to_goal(self):
        pass
    def getpathcoords(self):
        pass
    def bias (self):
        pass
    def expand (self):
        pass
    def cost (self):
        pass

        

