from Card import Card

class Player:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.turn = False
        self.totalPoints = 0
        self.active = True
        self.currentHand = []

    def addCard(self, card: Card):
        self.currentHand.append(card)

    def getSelectedCards(self) -> list:
        return [card for card in self.currentHand if card.isSelected()]

    def removeCardsFromHand(self, cards: list):
        for card in cards:
            self.currentHand.remove(card)
    
    def clearStatus(self):
        ...
    
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
        return self.currentHand
    
    def getTurn(self) -> bool:
        return self.turn
