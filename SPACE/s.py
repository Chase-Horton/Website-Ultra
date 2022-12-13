import pandas as pd
import sys, pygame
from pygame.locals import *
import math
from skyfield.api import Star as SkyStar, load
from skyfield.data import hipparcos
from skyfield.trigonometry import position_angle_of

size = width, height = 3840, 2160
screen = pygame.display.set_mode(size, display=1)
black = 0, 0, 0
white = 255, 255, 255
pygame.init()
myfont = pygame.font.SysFont("monospace", 32)
ts = load.timescale()


class StarMapper:
    def __init__(self, PPI, df):
        self.df = df
        self.PPI = PPI
        self.starFilter = 3
        self.starColor = white
        self.selectedConstell = 0
        self.constell = ['None', 'UMa', 'UMi', 'Gem', "Tau", 'Ori', 'Cas', 'Dra', 'Cru']
        self.Selector = StarSelector(df)

    def calculateStarLoc(self, star):
        x = self.PPI*11 * math.cos(star.altAng) * math.cos(star.azAngle) + width/2
        y = self.PPI*11 * math.cos(star.altAng) * math.sin(star.azAngle) + height/2
        return (x, y)

    def updateText(self):
        label = myfont.render('Showing Stars brighter than Magnitude: {:.1f}'.format(self.starFilter), 1, (255,255,0))
        screen.blit(label, (2900, 100))
        if self.constell[self.selectedConstell] != 'None':
            constell = self.Selector.constellNameDict[self.constell[self.selectedConstell]]
        else:
            constell = 'None'
        label = myfont.render(f'Selected Constellation: {constell}', 1, (255,255,0))
        screen.blit(label, (2900, 140))
        label = myfont.render(f'Date: {self.Selector.dmy[1]}/{self.Selector.dmy[0]}/{self.Selector.dmy[2]} 20:00:00 CST', 1, (255,255,0))
        screen.blit(label, (2900, 180))
        

    def mapStars(self):
        self.starsToMap = self.Selector.selectStarsByMag(self.starFilter)
        for star in self.starsToMap:
            x, y = self.calculateStarLoc(star)
            mag = star.magnitude
            mag = mag/self.starFilter
            rad = 11 - 8*mag
            star.coords = (x, y)
            star.rad = rad
            if star.name != "nan":
                c = [255, 0, 0]
            else:
                c = self.starColor
            if star.symbol == self.constell[self.selectedConstell]:
                c = [0,0,255]
            pygame.draw.circle(screen, c, (x, y), rad)
        self.updateText()
    def justMapStars(self):
        for star in self.starsToMap:
            x, y = self.calculateStarLoc(star)
            mag = star.magnitude
            mag = mag/self.starFilter
            rad = 11 - 8*mag
            star.coords = (x, y)
            star.rad = rad
            if star.name != "nan":
                c = [255, 0, 0]
            else:
                c = self.starColor
            if star.symbol == self.constell[self.selectedConstell]:
                c = [0,0,255]
            pygame.draw.circle(screen, c, (x, y), rad)
        self.updateText()
    def redrawStar(self, star, color):
        x, y = self.calculateStarLoc(star)
        mag = star.magnitude
        mag = mag/self.starFilter
        rad = 11 - 8*mag
        star.coords = (x, y)
        star.rad = rad
        pygame.draw.circle(screen, color, (x, y), rad)
    def checkStar(self, loc):
        for star in self.starsToMap:
            try:
                dist = math.sqrt((loc[0] - star.coords[0])**2 + (loc[1] - star.coords[1])**2)
                if dist < star.rad:
                    return star
            except:
                #star has no coords
                pass
    def incrementDay(self):
        dmy = self.Selector.dmy
        dmy[0] += 1
        if dmy[0] >= 28:
            dmy[0] = 1
            dmy[1] += 1
        if dmy[1] > 12:
            dmy[1] = 1
            dmy[2] += 1
        self.Selector.dmy = dmy
    def decrementDay(self):
        dmy = self.Selector.dmy
        dmy[0] -= 1
        if dmy[0] <= 0:
            dmy[0] = 28
            dmy[1] -= 1
        if dmy[1] < 1:
            dmy[1] = 12
            dmy[2] -= 1
        self.Selector.dmy = dmy



with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

df = df[df['ra_degrees'].notnull()]

G = GridPlotter(97)
G.plotGraph()
G.plotGraphLines()
S = StarMapper(97, df)
S.mapStars()

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_TAB:
                G.updateGraphLines(True)
                S.mapStars()
            elif event.key == K_UP:
                S.starFilter += 0.1
                G.updateGraphLines()
                S.mapStars()
            elif event.key == K_DOWN:
                S.starFilter -= 0.1
                G.updateGraphLines()
                S.mapStars()
            elif event.key == K_d:
                S.incrementDay()
                G.updateGraphLines()
                S.mapStars()
            elif event.key == K_a:
                S.decrementDay()
                G.updateGraphLines()
                S.mapStars()
            elif event.key == K_RIGHT:
                G.updateGraphLines()
                S.selectedConstell += 1
                if S.selectedConstell >= len(S.constell): S.selectedConstell = 0
                S.justMapStars()
            elif event.key == K_LEFT:
                G.updateGraphLines()
                S.selectedConstell -= 1
                S.justMapStars()
        elif event.type == MOUSEBUTTONDOWN:
            G.updateGraphLines()
            S.justMapStars()
            try:
                selectedStar = S.checkStar(pygame.mouse.get_pos())
                selectedStar.info()
                S.redrawStar(selectedStar, (255,255,0))
            except:
                label = myfont.render('No Star Found', 1, (255,255,0))
                screen.blit(label, (100, 100))
                pass