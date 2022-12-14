class ConstellationLine:
    def __init__(self, TwoStars):
        self.star1 = TwoStars[0]
        self.star2 = TwoStars[1]
        self.pos1 = self.star1.loc
        self.pos2 = self.star2.loc
        self.line = (self.pos1, self.pos2)
    def getLineCoords(self):
        return self.line