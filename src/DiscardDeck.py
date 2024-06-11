from Deck import Deck

class DiscardDeck(Deck):
    def __init__(self):
        super().__init__()
    
    def cleanAndReturnCards(self) -> list:
        cards = self.cards.copy()
        self.cards = []
        return cards