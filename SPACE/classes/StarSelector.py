from skyfield.api import Star as SkyStar
from Star import Star
class StarSelector:
    def __init__(self, df):
        self.df = df
        starNames = open('./data/stars', 'r', encoding="utf-8")
        constNames = open('./data/constellations', 'r', encoding="utf-8")
        constStars = open('./data/constellationship', 'r', encoding='utf-8')
        self.nameDict = {}
        self.constellNameDict = {}
        self.starConstellDict = {}
        #make dict of star ids and names
        for line in starNames.readlines():
            line = line.split('|')
            starId = int(line[0])
            name = self.getBetween('"', line[1])
            self.nameDict[starId] = name
        #make dict of contellation ids and names
        for line in constNames.readlines():
            line = line.split('\t')
            symbol = line[0]
            name = line[1][1:-1]
            self.constellNameDict[symbol] = name
        #make dict of star ids and constellation names
        for line in constStars.readlines():
            line = line.split(' ')
            symbol = line[0]
            line = line[2:]
            for code in line:
                self.starConstellDict[int(code)] = symbol
    # helper func to get string between symbols for const and star tables
    def getBetween(self, symbol, string):
        start = string.index(symbol) + 1
        end = string.index(symbol, start)
        return string[start:end]
    
    def selectStarsByConstellations(self, time, location, constellations, starsToMap=[]):
        tempStars = self.df[self.df["magnitude"] <= 12]
        stars = []
        for index, star in tempStars.iterrows():
            starObj = SkyStar.from_dataframe(tempStars.loc[index])
            id = int(star.name)

            try:
                symbol = self.starConstellDict[id]
                constell = self.constellNameDict[symbol]
            except:
                symbol = "nan"
                constell = "nan"
            if symbol not in constellations:
                continue
            else:
                pass
            #calculate apparent alt az and dist at t from loc
            apparent = location.at(time).observe(starObj).apparent()
            alt, az, distance = apparent.altaz()
            
            mag = star['magnitude']
            try:
                name = self.nameDict[id]
            except:
                name = "nan"
            starsToMap.append(Star(id, name, constell, symbol, mag, alt, az, distance, starObj))
        greatestMagnitude = -70000
        lowestMagnitude = 80000
        for star in starsToMap:
            if star.magnitude > greatestMagnitude:
                greatestMagnitude = star.magnitude
            elif star.magnitude < lowestMagnitude:
                lowestMagnitude = star.magnitude
        for star in starsToMap:
            star.normMagnitude = 1-(star.magnitude + abs(lowestMagnitude))/(greatestMagnitude + abs(lowestMagnitude)) 
        return starsToMap

    def selectStarsByMag(self, filter, time, location):
        #select all stars less than magnitude filter
        tempStars = self.df[self.df["magnitude"] <= filter]
        starsToMap = []

        for index, star in tempStars.iterrows():
            starObj = SkyStar.from_dataframe(tempStars.loc[index])
            #calculate apparent alt az and dist at t from loc
            apparent = location.at(time).observe(starObj).apparent()
            alt, az, distance = apparent.altaz()
            
            mag = star['magnitude']
            id = int(star.name)
            try:
                name = self.nameDict[id]
            except:
                name = "nan"
            try:
                symbol = self.starConstellDict[id]
                constell = self.constellNameDict[symbol]
            except:
                symbol = "nan"
                constell = "nan"
            starsToMap.append(Star(id, name, constell, symbol, mag, alt, az, distance, starObj))
        starsToMap.reverse()
        greatestMagnitude = -70000
        lowestMagnitude = 80000
        for star in starsToMap:
            if star.magnitude > greatestMagnitude:
                greatestMagnitude = star.magnitude
            elif star.magnitude < lowestMagnitude:
                lowestMagnitude = star.magnitude
        for star in starsToMap:
            star.normMagnitude = 1-(star.magnitude + abs(lowestMagnitude))/(greatestMagnitude + abs(lowestMagnitude)) 
        return starsToMap
