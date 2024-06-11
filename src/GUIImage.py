from Card import Card

class GUIImage:
    
    def getDiscardDeckFirstCard(self) -> list:
        return self.discardDeckFirstCard

    def setDiscardDeckFirstCard(self, card: Card):
        self.discardDeckFirstCard = card
    
    def getMessage(self) -> str:
        return self.message

    def setMessage(self, message: str):
        self.message = message
    
    def getBuyDeckEmpty(self) -> bool:
        return self.buyDeckEmpty

    def setBuyDeckEmpty(self, empty: bool):
        self.buyDeckEmpty = empty
    
    def getPlayersInfo(self) -> list:
        return self.playersInfo.copy()

    def setPlayersInfo(self, playersInfo: list):
        self.playersInfo = playersInfo.copy()
    
    def getLocalPlayerCurrentHand(self) -> list:
        return self.localPlayerCurrentHand.copy()

    def setLocalPlayerCurrentHand(self, cards: list):
        self.localPlayerCurrentHand = cards.copy()

    