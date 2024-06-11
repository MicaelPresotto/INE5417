from Player import Player
from DiscardDeck import DiscardDeck
from BuyDeck import BuyDeck

class Table:
    def __init__(self):
        self.players = [Player(f"Player {i}") for i in range(4)]
        self.discardDeck = DiscardDeck()
        self.buyDeck = BuyDeck()

    def identifyTurnPlayer(self) -> Player:
        ...

    def getStatus(self) -> int:
        ...

    def setTableStatus(self, status: int):
        ...

    def isSet(self, cards: list) -> bool:
        value = cards[0].getValue()
        for card in cards[1:]:
            if card.getValue() != value: return False
        return True

    def isSequence(self, cards: list) -> bool:
        cards.sort(key = lambda c: c.getValue())
        suit = cards[0].getSuit()
        for i in range(1, len(cards)):
            if cards[i].getSuit() != suit or cards[i].getValue() - 1 != cards[i-1].getValue(): return False
        return True

    def buyDeck(self):
        ...

    def discardDeck(self):
        ...

    def receive_withdrawal_notification(self):
        ...

    def start_match(self):
        ...

    def reset_game(self):
        ...
    
    def receive_move(self, a_move):
        ...

    def distribute_cards(self):
        ...

    def getGUIImage(self):
        ...

    def resetPlayerQueue(self):
        ...

    def orderPlayerQueue(self):
        ...
    
    def applyPenaltyToOtherPlayers(self, playersQueue: list):
        for player in playersQueue:
            if player.getTurn == False:
                player.updateTotalPoints(10)

    def applyPenaltyToPlayer(self, player: Player):
        ...

    def endRound(self):
        ...

    def verifyEndOfMatch(self, playersQueue: list) -> bool:
        ...
    
    def isSet(self, cards : list) -> bool:
        s = set()
        for card in cards:
            value = card.getValue()
            if value != "0": s.add(value)
        return len(s) == 1