class Card:
    def __init__(self, id: int, value: str, suit: str, points: int, number: int):
        self.id = id
        self.value = value
        self.suit = suit
        self.points = points
        self.number = number
        self.selected = False
    
    def getValue(self) -> str:
        return self.value
    
    def getSuit(self) -> str:
        return self.suit

    def getPoints(self) -> int:
        return self.points

    def isSelected(self) -> bool:
        return self.selected
    
    def toggleSelected(self):
        self.selected = not self.selected
    
    def getNumber(self) -> int:
        return self.number

    def getId(self) -> int:
        return self.id
    
    def setSelected(self, selected: bool):
        self.selected = selected