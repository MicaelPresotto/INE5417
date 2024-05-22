from Deck import Deck
from Card import Card

class BuyDeck(Deck):
    def __init__(self):
        super().__init__() # EGL -> Verificar necessidade dessa linha
        suits = ["C","E","O","P"]
        special_values = ["A", "J", "Q", "K"]
        for c in range(52):
            value = str(c % 13 + 1) if (c % 13 + 1) not in [1,11,12,13] else special_values[(c % 13) % 9]
            suit = suits[c // 13]
            points = min((c % 13 + 1), 10)
            self.cards.append(Card(value, suit, points))
        for c in range(2):
            self.cards.append(Card("Joker", "?", 0))