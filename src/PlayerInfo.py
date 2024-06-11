class PlayerInfo:
    def __init__(self, playerId: str, numberOfCards: int, points: int):
        self.playerId = playerId
        self.numberOfCards = numberOfCards
        self.points = points

    def getPlayerId(self) -> str:
        return self.playerId

    def setPlayerId(self, playerId: str):
        self.playerId = playerId

    def getNumberOfCards(self) -> int:
        return self.numberOfCards

    def setNumberOfCards(self, numberOfCards: int):
        self.numberOfCards = numberOfCards

    def getPoints(self) -> int:
        return self.points

    def setPoints(self, points: int):
        self.points = points
