from Card import Card

class Deck:
    def __init__(self):
        self.cards = []
    
    def popCard(self) -> Card:
        return self.cards.pop()

    def getSize(self) -> int:
        return len(self.cards)

    def addCardsToDeck(self, cards: list):
        self.cards.extend(cards.copy())
    
    def setCards(self, cards: list):
        self.cards = cards.copy()

    def getCards(self) -> list:
        return self.cards.copy()