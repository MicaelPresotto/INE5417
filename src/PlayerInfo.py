class PlayerInfo:
    def __init__(self, playerId: str, numberOfCards: int, points: int):
        self.playerId = playerId
        self.numberOfCards = numberOfCards
        self.points = points

    def getPlayerId(self):
        return self.playerId

    def setPlayerId(self, playerId):
        self.playerId = playerId

    def getNumberOfCards(self):
        return self.numberOfCards

    def setNumberOfCards(self, numberOfCards):
        self.numberOfCards = numberOfCards

    def getPoints(self):
        return self.points

    def setPoints(self, points):
        self.points = points
