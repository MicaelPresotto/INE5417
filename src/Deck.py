from Card import Card

class Deck:
    def __init__(self):
        self.cards = []
    
    def popCard(self) -> Card:
        return self.cards.pop()

    def clearDeck(self):
        self.cards = []