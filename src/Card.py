class Card:
    def __init__(self, value: str, suit: str, points: int):
        self.value = value
        self.suit = suit
        self.points = points
        self.selected = False
    
    def get_value(self) -> str:
        return self.value
    
    def get_suit(self) -> str:
        return self.suit