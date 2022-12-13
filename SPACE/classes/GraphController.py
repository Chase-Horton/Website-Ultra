from skyfield.api import load, wgs84
from skyfield.data import hipparcos
from StarSelector import StarSelector
from GridPlotter import GridPlotter
from datetime import datetime
import pygame, sys
from pygame.locals import *
import math
pygame.init()
myfont = pygame.font.SysFont("monospace", 32)
class GraphController:
    def __init__(self):
        #STATEFUL
        self.graphStateIndex = 6
        self.constellationCatalog = ['none', 'Ori', 'UMa', 'UMi', 'Dra', 'Cas']
        self.constellationCatalogIndex = 0
        self.filter = 7
        #CONST
        size = 3840, 2160
        self.screen = pygame.display.set_mode(size, display=1)
        self.ts = load.timescale()
        #set time for angle calc
        self.time = self.ts.now()

        planets = load('de421.bsp')
        self.earth = planets['earth']
        #set location to wichita on earth for apparent location of stars
        self.location = self.earth + wgs84.latlon(37.697948, -97.314835, 400)

        #load hipparcos db of stars
        with load.open(hipparcos.URL) as f:
            self.df = hipparcos.load_dataframe(f)

        #remove missing pos
        self.df = self.df[self.df['ra_degrees'].notnull()]
        #create star selector object
        self.Selector = StarSelector(self.df)
        #create grid controller
        self.GridPlotter = GridPlotter(self.screen, 115)
    #select stars filtering by selected magnitude
    def selectStarsByMag(self):
        return self.Selector.selectStarsByMag(self.filter, self.time, self.location)
    #select stars by list of constellation symbols
    def selectStarsByConst(self, consts):
        return self.Selector.selectStarsByConstellations(self.time, self.location, consts)
    #add stars by list of constellation symbols to list of stars
    def addStarsByConst(self, consts, starList):
        return self.Selector.selectStarsByConstellations(self.time, self.location, consts, starList)
    #update selected constellation index
    def updateConstellationIndex(self, i):
        self.constellationCatalogIndex += i
        if self.constellationCatalogIndex < 0:
            self.constellationCatalogIndex = len(self.constellationCatalog) - 1
        elif self.constellationCatalogIndex >= len(self.constellationCatalog):
            self.constellationCatalogIndex = 0
        self.fastDrawStars()
    #update GraphStateIndex
    def updateGraphStateIndex(self, i):
        self.graphStateIndex += i
        if self.graphStateIndex < 0:
            self.graphStateIndex = 0
        elif self.graphStateIndex > 6:
            self.graphStateIndex = 6
        self.fastDrawStars()
    #redraw graph then stars based on state values
    def drawStars(self):
        #draw graph and lines and labels
        self.GridPlotter.update(self.graphStateIndex)
        #!selection magnitude add more options later
        if "mag" == "mag":
            self.currStars = self.selectStarsByMag()
            self.GridPlotter.plotStarList(self.currStars, self.constellationCatalog[self.constellationCatalogIndex])
        #selection constellation
        elif "byConst" == "TBA":
            pass
    #draw stars with threading
    def drawStarsWithThread(self):
        #draw graph and lines and labels
        self.GridPlotter.update(self.graphStateIndex)
        #!selection magnitude add more options later
        if "mag" == "mag":
            self.currStars = self.Selector.selectStarsByMagnitudeWithBatching(self.filter, self.time, self.location)
            self.GridPlotter.plotStarList(self.currStars, self.constellationCatalog[self.constellationCatalogIndex])
        #selection constellation
        elif "byConst" == "TBA":
            pass
    def fastDrawStars(self):
        self.GridPlotter.update(self.graphStateIndex)
        self.GridPlotter.plotStarList(self.currStars, self.constellationCatalog[self.constellationCatalogIndex])
    def findStar(self, loc):
        for star in self.currStars:
            dist = math.sqrt((loc[0] - star.loc[0]) ** 2 + (loc[1] - star.loc[1]) ** 2)
            if dist < star.normMagnitude*8 + 2:
                return star
        return None
    def selectStar(self, star):
        if star == None:
            label = myfont.render('No Star Found', 1, (255,255,0))
            self.screen.blit(label, (100, 100))
            return
        else:
            #recolor star
            self.GridPlotter.plotStar(star, [255, 255, 0])
            #print info
            dist = 'Distance: {:,.2f} AU '.format(star.distance.au) + '| {:,.2f} ly'.format(star.distance.m/9460730472580800)
            infoLst = [f'HYG ID: {star.ID}', f'Name: {star.name}', f'Magnitude: {star.magnitude}', dist, f'Member of Constellation: {star.constellation} | {star.symbol}',
            'Azimuth: {:.2f}'.format(star.az), 'Altitude: {:.2f}'.format(star.alt)]
            offset = 0
            for txt in infoLst:
                label = myfont.render(txt, 1, (255,255,0))
                self.screen.blit(label, (100, 100 + offset))
                offset += 40
    # update location with new lat long
    def updateLocation(self, lat, long ,elev=0):
        self.location = self.earth + wgs84.latlon(lat, long, elev)
        self.drawStarsWithThread()
    #update filter value and redraw stars
    def updateFilter(self, i):
        self.filter += i
        self.drawStarsWithThread()
    #update time and redraw stars
    def updateTime(self, i):
        self.time += i
        self.drawStarsWithThread()
    #update info text
    def updateInfoText(self):
        label = myfont.render('Showing Stars brighter than Magnitude: {:.1f}'.format(self.filter), 1, (255,255,0))
        self.screen.blit(label, (2700, 100))
        if self.constellationCatalog[self.constellationCatalogIndex] != 'none':
            constell = self.Selector.constellNameDict[self.constellationCatalog[self.constellationCatalogIndex]]
        else:
            constell = 'None'
        label = myfont.render(f'Selected Constellation: {constell}', 1, (255,255,0))
        self.screen.blit(label, (2800, 140))
        label = myfont.render(f'Selected Time: {self.time.utc_strftime()}', 1, (255,255,0))
        self.screen.blit(label, (2900, 180))
G = GraphController()
start = datetime.now()
G.drawStars()
end = datetime.now()
print('Time to draw stars: ', end - start)
while True:
    pygame.display.update()
    G.updateInfoText()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_w:
                G.updateFilter(.1)
            elif event.key == K_s:
                G.updateFilter(-.1)
            elif event.key == K_d:
                G.updateConstellationIndex(1)
            elif event.key == K_a:
                G.updateConstellationIndex(-1)
            elif event.key == K_z:
                G.updateGraphStateIndex(-1)
            elif event.key == K_x:
                G.updateGraphStateIndex(1)
            elif event.key == K_e:
                G.updateTime(10)
            elif event.key == K_q:
                G.updateTime(-1)
        elif event.type == MOUSEBUTTONDOWN:
            G.fastDrawStars()
            star = G.findStar(pygame.mouse.get_pos())
            G.selectStar(star)

            