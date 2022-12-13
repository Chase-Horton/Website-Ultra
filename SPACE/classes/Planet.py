class Planet:
    def __init__(self, id, name, alt, az, dist, magnitude, planetObj):
        self.loc = []
        self.name = name
        self.type = 'planet'
        self.ID = id
        self.magnitude = magnitude
        self.az = az.degrees
        self.alt = alt.degrees
        self.distance = dist
        self.starObj = planetObj
    #set x,y coords on graph
    def setLoc(self, loc):
        self.loc = loc
    #return info string
    def info(self):
        return f'Name: {self.name}\nAltitude: {self.alt}\nAzimuth: {self.az}\nDistance: {self.distance}\nMagnitude: {self.magnitude}'