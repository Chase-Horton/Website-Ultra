class Messier:
    def __init__(self, MCode, NGC, NGCNames, RA, Dec, Mag, distance, Size, Type, Constellation, yearDiscovered, discoverer, imageUrl):
        self.MCode = MCode
        self.NGC = NGC
        self.NGCNames = NGCNames
        if ":" in RA:
            self.ra = [float(item) for item in RA.split(':')]
            self.dec = [float(item) for item in Dec.split(':')]
        else:
            RA.append(float(0))
            Dec.append(float(0))
            self.ra = RA
            self.dec = Dec
        self.magnitude = float(Mag)
        self.distance = float(distance)
        self.size = Size
        self.type = Type
        self.constellation = Constellation
        self.yearDiscovered = yearDiscovered
        self.discoverer = discoverer
        self.imageUrl = imageUrl
        self.loc = []
    def setLoc(self, loc):
        self.loc = loc