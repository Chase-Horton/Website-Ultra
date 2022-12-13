from skyfield.api import load, wgs84
from Planet import Planet
class PlanetSelector:
    def __init__(self):
        self.planets = load('de421.bsp')
        self.planetList = {'Mercury':1, 'Venus':2, 'Mars':4, 'Jupiter':5, 'Saturn':6, 'Uranus':7, 'Neptune':8}
        self.planetMagnitudes = {'Mercury':-0.36, 'Venus':-4.40, 'Mars':-1.52, 'Jupiter':-9.40, 'Saturn':-8.88, 'Uranus':-7.19, 'Neptune':-6.87}
        self.planetNameList = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
        self.selectedPlanets = [1, 2, 4, 5, 6, 7, 8]
        self.planetCodes = {planetKey:self.planets[self.planetList[planetKey]] for planetKey in self.planetList.keys()}
    #get alt and az of planet by name time and location and store in obj
    def getPlanetObj(self, planetName, time, location):
        apparent = location.at(time).observe(self.planetCodes[planetName]).apparent()
        alt, az, distance = apparent.altaz()
        planetData = Planet(self.planetList[planetName], planetName, alt, az, distance, self.planetMagnitudes[planetName], self.planetCodes[planetName])
        return planetData
    #toggle planet selection by number
    def togglePlanetSelection(self, number):
        if number in self.selectedPlanets:
            self.selectedPlanets.remove(number)
        else:
            self.selectedPlanets.append(number)
    #get string names of all selected planet numbers
    def getSelectedPlanets(self):
        for number in self.selectedPlanets:
            for planet in self.planetNameList:
                if self.planetList[planet] == number:
                    yield planet
    #get planet objects of all selected planets using string names function
    def getSelectedPlanetsObjs(self, time, location):
        planets = []
        for planet in self.getSelectedPlanets():
            if planet != None:
                planets.append(self.getPlanetObj(planet, time, location))
        return planets
    #get all planet objects of selected planets which are visible at time and location
    def getVisiblePlanets(self, time, location):
        planets = []
        for planet in self.getSelectedPlanets():
            if planet != None:
                planetObj = self.getPlanetObj(planet, time, location)
                if planetObj.alt > 0:
                    planets.append(planetObj)
        
        greatestMagnitude = -70000
        lowestMagnitude = 80000
        for planet in planets:
            if planet.magnitude > greatestMagnitude:
                greatestMagnitude = planet.magnitude
            elif planet.magnitude < lowestMagnitude:
                lowestMagnitude = planet.magnitude
        for planet in planets:
            planet.normMagnitude = 1-(planet.magnitude + abs(lowestMagnitude))/(greatestMagnitude + abs(lowestMagnitude)) 
        return planets