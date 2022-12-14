from skyfield.api import load, wgs84
from skyfield.data import hipparcos
from StarSelector import StarSelector
from PlanetSelector import PlanetSelector
from MessierSelector import MessierSelector
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
        self.selectedSearchObject = None
        self.currPlanets = []
        self.currStars = []
        self.currMessier = []
        self.planetPlotterEnabled = False
        self.messierPlotterEnabled = False
        self.graphStateIndex = 6
        self.constellationCatalog = ['none', 'Ori', 'UMa', 'UMi', 'Dra', 'Cas']
        self.constellationCatalogIndex = 0
        self.filter = 2.5
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
        #create star, planet, and messier selector object
        self.Selector = StarSelector(self.df)
        self.PlanetSelector = PlanetSelector()
        self.MessierSelector = MessierSelector()
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
        self.fastRefresh()
    #update GraphStateIndex
    def updateGraphStateIndex(self, i):
        self.graphStateIndex += i
        if self.graphStateIndex < 0:
            self.graphStateIndex = 0
        elif self.graphStateIndex > 6:
            self.graphStateIndex = 6
        self.fastRefresh()
    #redraw graph then stars based on state values
    def drawStars(self):
        #!selection magnitude add more options later
        if "mag" == "mag":
            self.currStars = self.selectStarsByMag()
            self.GridPlotter.plotStarList(self.currStars, self.constellationCatalog[self.constellationCatalogIndex])
        #selection constellation
        elif "byConst" == "TBA":
            pass
    #draw planets 
    def drawPlanets(self):
        self.currPlanets = self.PlanetSelector.getVisiblePlanets(self.time, self.location)
        self.GridPlotter.plotPlanetList(self.currPlanets)
    #draw messier objects
    def drawMessier(self):
        self.currMessier = self.MessierSelector.getVisibleMessierObjects(self.time, self.location)
        self.GridPlotter.plotMessierList(self.currMessier)  
    #draw stars with threading
    def drawStarsWithThread(self):
        #!selection magnitude add more options later
        if "mag" == "mag":
            self.currStars = self.Selector.selectStarsByMagnitudeWithBatching(self.filter, self.time, self.location)
            self.GridPlotter.plotStarList(self.currStars, self.constellationCatalog[self.constellationCatalogIndex])
        #selection constellation
        elif "byConst" == "TBA":
            pass
    def fastDrawStars(self):
        self.GridPlotter.plotStarList(self.currStars, self.constellationCatalog[self.constellationCatalogIndex])
    def findStarOrPlanet(self, loc):
        for star in self.currStars:
            dist = math.sqrt((loc[0] - star.loc[0]) ** 2 + (loc[1] - star.loc[1]) ** 2)
            if dist < star.normMagnitude*8 + 2:
                return star
        for planet in self.currPlanets:
            dist = math.sqrt((loc[0] - planet.loc[0]) ** 2 + (loc[1] - planet.loc[1]) ** 2)
            if dist < planet.normMagnitude*12 + 2:
                return planet
        for messierObject in self.currMessier:
            dist = math.sqrt((loc[0] - messierObject.loc[0]) ** 2 + (loc[1] - messierObject.loc[1]) ** 2)
            if dist < messierObject.normMagnitude*12 + 2:
                return messierObject
        return None
    #!TODO:save infolst and offsets for between refreshes
    def selectStarOrPlanet(self, starOrPlanet, color=[255, 255, 0], position = [100, 100]):
        if starOrPlanet == None:
            label = myfont.render('No Star Found', 1, color)
            self.screen.blit(label, position)
            return
        elif starOrPlanet.objType == 'star':
            star = starOrPlanet
            #recolor star
            self.GridPlotter.plotStar(star, color)
            #print info
            dist = 'Distance: {:,.2f} AU '.format(star.distance.au) + '| {:,.2f} ly'.format(star.distance.m/9460730472580800)
            infoLst = [f'HYG ID: {star.ID}', f'Name: {star.name}', f'Magnitude: {star.magnitude}', dist, f'Member of Constellation: {star.constellation} | {star.symbol}',
            'Azimuth: {:.2f}°'.format(star.az), 'Altitude: {:.2f}°'.format(star.alt)]
            offset = 0
            for txt in infoLst:
                label = myfont.render(txt, 1, color)
                self.screen.blit(label, (position[0], position[1] + offset))
                offset += 40
            return
        elif starOrPlanet.objType == 'planet':
            planet = starOrPlanet
            #recolor planet
            if planet.alt > 0:
                self.GridPlotter.plotPlanet(planet, color)
            #print info
            dist = 'Distance: {:,.2f} km '.format(planet.distance.km) + '| {:,.2f} ly'.format(planet.distance.m/9460730472580800)
            infoLst = [f'Name: {planet.name}', f'Magnitude: {planet.magnitude}', dist,'Azimuth: {:.2f}°'.format(planet.az),
                'Altitude: {:.2f}°'.format(planet.alt), 'Mass: {:,.2f} kg'.format(planet.mass1024*1024), 'Diameter: {:,.2f} km'.format(planet.diameter),
                 'Density: {:,.2f} kg/m^3'.format(planet.density), 'Gravity: {:,.2f} m/s^2'.format(planet.gravity),
                  'Average Temperature: {:,.2f} C'.format(planet.avgTemp), 'Number of Moons {}'.format(planet.numMoons)]
            offset = 0
            for txt in infoLst:
                label = myfont.render(txt, 1, color)
                self.screen.blit(label, (position[0], position[1] + offset))
                offset += 40
            return
        else:
            if messier.alt > 0:
                messier = starOrPlanet
            #recolor messier
            self.GridPlotter.plotPlanet(messier, color)
            #print info
            designation = f'Messier #: {messier.MCode}'
            NGC = f'NGC #: {messier.NGC}'
            if messier.NGCNames == None:
                name = 'Other Names: N/A'
            else:
                name = f'Other Names: {messier.NGCNames}'
            constellation = f'Constellation: {messier.constellation}'
            mType = f'Type: {messier.type}'
            yearDiscovered = 'Year Discovered: {:,.0f}'.format(messier.yearDiscovered)

            magnitude = 'Magnitude: {:.2f}'.format(messier.magnitude)
            alt = 'Altitude: {:.2f}°'.format(messier.alt)
            az = 'Azimuth: {:.2f}°'.format(messier.az)
            distance = 'Distance: {:,.2f} ly'.format(messier.distance)
            infoLst = [designation, NGC, name, constellation, mType, yearDiscovered, magnitude, alt, az, distance]
            offset = 0
            for txt in infoLst:
                label = myfont.render(txt, 1, color)
                self.screen.blit(label, (position[0], position[1] + offset))
                offset += 40
            return
            
            
    # update location with new lat long
    def updateLocation(self, lat, long ,elev=0):
        self.location = self.earth + wgs84.latlon(lat, long, elev)
        self.refresh()
    #update filter value and redraw stars
    def updateFilter(self, i):
        self.filter += i
        self.refresh()
    #update time and redraw stars
    def updateTime(self, i):
        self.time += i
        self.refresh()
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
    #toggle planet plotter
    def togglePlanetPlotter(self):
        self.planetPlotterEnabled = not self.planetPlotterEnabled
        self.refresh()
    def toggleMessierPlotter(self):
        self.messierPlotterEnabled = not self.messierPlotterEnabled
        self.refresh()
    #!TODO: ADD METHOD THAT UPDATES SAVED SEARCH OBJECTS POSITION INSTEAD OF RERUNNING THIS FUNCTION
    def searchObject(self, name):
        # first check if it is a planet we are displaying
        for planet in self.currPlanets:
            if planet.name == name:
                print('Found on screen')
                return planet
        # then check if it is a planet we are not displaying
        if name in self.PlanetSelector.planetList:
            return self.PlanetSelector.getPlanetObj(name, self.time, self.location)
        # then check if it is a messier object we are displaying
        for messier in self.currMessier:
            if messier.NGCNames != None:
                if name in messier.NGCNames:
                    print('Found on screen')
                    return messier
            if name == messier.MCode:
                print('Found on screen')
                return messier
            if name == messier.NGC:
                print('Found on screen')
                return messier
        # then check if it is a messier object we are not displaying
        messierObjects = self.MessierSelector.getAllMessierObjects(self.time, self.location)
        for messier in messierObjects:
            if messier.NGCNames != None:
                if name in messier.NGCNames:
                    return messier
            if name == messier.MCode:
                return messier
            if name == messier.NGC:
                return messier
        # now check if the object is a star we are displaying
        foundStar = None
        for star in self.currStars:
            if star.name == name:
                foundStar = star
            if star.ID == name:
                foundStar = star
                return star
        if foundStar != None:
            if foundStar.alt > 0:
                print('Found on screen')
                return foundStar
            else:
                print('Star is below horizon')
                return foundStar
        else:
            #resolution too low
            return self.Selector.selectStarByNameOrId(name, self.location, self.time)
    def refreshSearchObjectAndData(self):
        if self.selectedSearchObject != None:
            #update info on search object in bottom right
            newObj = self.searchObject(self.selectedSearchObject.name)
            self.selectedSearchObject = newObj
            self.selectStarOrPlanet(newObj, [255, 0, 0], [2950, 1500])
    def refresh(self):
        #draw graph and lines and labels
        self.GridPlotter.update(self.graphStateIndex)
        if self.messierPlotterEnabled:
            self.drawMessier()
        #draw stars over messier
        self.drawStars()
        #draw planets over stars
        if self.planetPlotterEnabled:
            self.drawPlanets()
        #draw search object over planets
        self.refreshSearchObjectAndData()
    def fastRefresh(self):
        #draw graph and lines and labels
        self.GridPlotter.update(self.graphStateIndex)
        if self.messierPlotterEnabled:
            self.drawMessier()
        self.fastDrawStars()
        if self.planetPlotterEnabled:
            self.drawPlanets()
        self.refreshSearchObjectAndData()
    def handleKeys(self, events):
        for event in events:
            if(event.type == KEYDOWN):
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_w:
                    self.updateFilter(.1)
                elif event.key == K_s:
                    self.updateFilter(-.1)
                elif event.key == K_d:
                    self.updateConstellationIndex(1)
                elif event.key == K_a:
                    self.updateConstellationIndex(-1)
                elif event.key == K_z:
                    self.updateGraphStateIndex(-1)
                elif event.key == K_x:
                    self.updateGraphStateIndex(1)
                elif event.key == K_e:
                    self.updateTime(1)
                elif event.key == K_q:
                    self.updateTime(-1)
                elif event.key == K_p:
                    self.togglePlanetPlotter()
                elif event.key == K_m:
                    self.toggleMessierPlotter()
                elif event.key == K_i:
                    self.selectedSearchObject = self.searchObject('Sabik')
                    self.fastRefresh()
            elif event.type == MOUSEBUTTONDOWN:
                self.fastDrawStars()
                starOrPlanet = self.findStarOrPlanet(pygame.mouse.get_pos())
                self.fastRefresh()
                self.selectStarOrPlanet(starOrPlanet)

            