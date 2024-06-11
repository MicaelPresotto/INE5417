from Player import Player
from DiscardDeck import DiscardDeck
from BuyDeck import BuyDeck
from GUIImage import GUIImage

DEFINE_NO_MATCH = 0
DEFINE_BUY_CARD_ACTION = 1
DEFINE_DISCARD_OR_SELECT_CARD_ACTION = 2
DEFINE_OPT_YANIV = 3
DEFINE_WAITING_FOR_REMOTE_ACTION = 4
DEFINE_FINISHED_MATCH = 5
DEFINE_WITHDRAWAL = 6
DEFINE_FINISHED_ROUND = 7

class Table:
    def __init__(self):
        self.playersQueue = [Player(f"Player {i}") for i in range(4)]
        self.discardDeck = DiscardDeck()
        self.buyDeck = BuyDeck()
        self.message = ""
        self.round = 0
        self.tableStatus = 0
        self.selectedDeck = None
        self.playersQueueIndex = 0
        self.localPlayerId = ""

    def identifyTurnPlayer(self) -> Player:
        for player in self.playersQueue:
            if player.getTurn(): return Player

    def getStatus(self) -> int:
        return self.status

    def setTableStatus(self, status: int):
        self.status = status

    def isSet(self, cards : list) -> bool:
        s = set()
        for card in cards:
            value = card.getValue()
            if value != "0": s.add(value)
        return len(s) == 1

    def isSequence(self, cards: list) -> bool:
        ...

    def buyCard(self):
        ...

    def discard(self):
        ...

    def receiveWithdrawalNotification(self):
        ...

    def receiveMove(self, a_move):
        ...

    def resetGame(self):
        ...

    def startMatch(self):
        ...
    
    def optYaniv(self) -> bool:
        ...

    def distributeCards(self):
        for player in self.playersQueue:
            for _ in range(5):
                card = self.buyDeck.popCard()
                player.addCard(card)

    def getGUIImage(self) -> GUIImage:
        ...

    def resetPlayerQueue(self):
        ...

    def orderPlayerQueue(self):
        ...
    
    def applyPenaltyToOtherPlayers(self, playersQueue: list):
        for player in playersQueue:
            if player.getTurn == False:
                player.updateTotalPoints(10)

    def resetRound(self):
        self.setTableStatus(DEFINE_BUY_CARD_ACTION)
        for player in self.playersQueue:
            cards = player.getCurrentHand()
            player.clearHand()
            self.buyDeck.addCardsToDeck(cards)
        discardCards = self.discardDeck.cleanAndReturnCards()
        self.buyDeck.addCardsToDeck(discardCards)
        self.buyDeck.shuffle()
        self.distributeCards()


    def verifyEndOfMatch(self) -> bool:
        MAXSCORE = 100
        for player in self.playersQueue:
            if player.getTotalPoints() >= MAXSCORE:
                return True
        return False


    def updatePlayersQueueIndex(self):
        self.playersQueueIndex = (self.playersQueueIndex + 1) % len(self.players)

    def getLocalPlayerId(self) -> str:
        return self.localPlayerId