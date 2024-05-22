class Card:
    def __init__(self, value: str, suit: str, points: int):
        self.value = value
        self.suit = suit
        self.points = points
        self.selected = False
    
    def getValue(self) -> str:
        return self.value
    
    def getSuit(self) -> str:
        return self.suit

    def getPoints(self) -> int:
        return self.points

    def isSelected(self) -> bool:
        return self.selected