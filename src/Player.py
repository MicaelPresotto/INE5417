from Card import Card

class Player:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.turn = False
        self.totalPoints = 0
        self.currentHand = []
        self.winner = False

    def addCard(self, card: Card):
        self.currentHand.append(card)

    def getSelectedCards(self) -> list:
        return [card for card in self.currentHand if card.isSelected()]

    def removeCardsFromHand(self, cards: list):
        for card in cards:
            self.currentHand.remove(card)

    def clearHand(self) -> list:
        previous_hand = self.currentHand.copy()
        self.currentHand = []
        return previous_hand
    
    def toggleTurn(self):
        self.turn = not self.turn
    
    def getTotalPoints(self) -> int:
        return self.totalPoints
    
    def checkIfLowestHand(self, playersQueue: list) -> bool:
        turnPlayerCurrentPoints = 0
        for card in self.getCurrentHand():
            turnPlayerCurrentPoints += card.getPoints()
        for player in playersQueue:
            if not player.getTurn():
                playerCurrentPoints = 0
                for card in player.getCurrentHand():
                    playerCurrentPoints += card.getPoints()
                if playerCurrentPoints <= turnPlayerCurrentPoints:
                    return False
        return True

    def updateTotalPoints(self, value: int):
        self.totalPoints += value

    def getCurrentHand(self) -> list:
        return self.currentHand.copy()
    
    def setCurrentHand(self, hand: list):
        self.currentHand = hand.copy()
    
    def setTotalPoints(self, points: int):
        self.totalPoints = points

    def getId(self) -> str:
        return self.id
    
    def setWinner(self, winner: bool):
        self.winner = winner
        
    def getTurn(self) -> bool:
        return self.turn
    
    def setTurn(self, turn: bool):
        self.turn = turn

    def getName(self) -> str:
        return self.name
    
    def isWinner(self) -> bool:
        return self.winner
    
    def findSelectedCardById(self, cardId: int) -> Card:
        for card in self.currentHand:
            if card.getId() == cardId:
                return card
        return None