from Deck import Deck

class DiscardDeck(Deck):
    def __init__(self):
        super().__init__()
    
    def addCardsToDeck(self, cards: list):
        self.cards.extend(cards)