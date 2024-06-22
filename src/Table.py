from Player import Player
from DiscardDeck import DiscardDeck
from BuyDeck import BuyDeck
from GUIImage import GUIImage
from PlayerInfo import PlayerInfo
from tkinter import messagebox
class Table:
    def __init__(self):
        self.playersQueue = [Player(f"Player {i}") for i in range(4)]
        self.discardDeck = DiscardDeck()
        self.buyDeck = BuyDeck()
        self.message = ""
        self.round = 0
        self.status = 0
        self.selectedDeck = None
        self.playersQueueIndex = 0
        self.localPlayerId = ""

        self.DEFINE_NO_MATCH = 0
        self.DEFINE_BUY_CARD_ACTION = 1
        self.DEFINE_DISCARD_OR_SELECT_CARD_ACTION = 2
        self.DEFINE_OPT_YANIV = 3
        self.DEFINE_WAITING_FOR_REMOTE_ACTION = 4
        self.DEFINE_FINISHED_MATCH = 5
        self.DEFINE_WITHDRAWAL = 6
        self.DEFINE_FINISHED_ROUND = 7

    def identifyTurnPlayer(self) -> Player:
        for player in self.playersQueue:
            if player.getTurn(): return Player

    def getStatus(self) -> int:
        return self.status

    def setStatus(self, status: int):
        self.status = status

    def isSet(self, cards : list) -> bool:
        s = set()
        for card in cards:
            value = card.getValue()
            if value != "0": s.add(value)
        return len(s) == 1

    def isSequence(self, cards: list) -> bool:
        for i in range(1,len(cards)):
            if cards[i].getSuit() != cards[i-1].getSuit(): return False

        values = [card.getValue() for card in cards].sort()
        for i in range(1, len(values)):
            if values[i] - values[i-1] != 1: return False
        return True

    def buyCard(self):
        turnPlayer = self.identifyTurnPlayer()
        status = self.getStatus()
        localPlayerId = self.getLocalPlayerId()
        numCards = self.buyDeck.getSize()
        if status == self.DEFINE_BUY_CARD_ACTION and turnPlayer.getId() == localPlayerId and numCards > 0:
            card = self.buyDeck.popCard()
            turnPlayer.addCard(card)
            self.setStatus(self.DEFINE_DISCARD_OR_SELECT_CARD_ACTION)
            # send_move
        else:
            messagebox.showinfo("Invalid action", "You can't buy a card now")
    def discard(self):
        turnPlayer = self.identifyTurnPlayer()
        status = self.getStatus()
        localPlayerId = self.getLocalPlayerId()
        if status == self.DEFINE_DISCARD_OR_SELECT_CARD_ACTION and turnPlayer.getId() == localPlayerId:
            selectedCards = turnPlayer.getSelectedCards()
            if len(selectedCards) >= 2:
                is_set = self.isSet(selectedCards)
            elif len(selectedCards) >= 3:
                is_sequence = self.isSequence(selectedCards)
            if len(selectedCards) == 1 or is_sequence or is_set:
                self.discardCards(selectedCards)
                self.discardDeck.addCardsToDeck(selectedCards)
                turnPlayer.removeCardsFromHand(selectedCards)
                self.setStatus(self.DEFINE_OPT_YANIV)
                # send_move
            else:
                messagebox.showinfo("Invalid action", "Invalid move")


    def receiveWithdrawalNotification(self):
        self.setStatus(self.DEFINE_WITHDRAWAL)
        


    def receiveMove(self, a_move):
        ...

    def resetGame(self):
        ...
        #msma coisa do start match

    def startMatch(self):
        ...
        # acho que nao existe isso aqui?, pelo diagrama ta no player interface
    
    def optYaniv(self, yanivOpt: bool) -> bool:
        turnPlayer = self.identifyTurnPlayer()
        status = self.getStatus()
        localPlayerId = self.getLocalPlayerId()
        if status == self.DEFINE_OPT_YANIV and turnPlayer.getId() == localPlayerId:
            totalPoints = turnPlayer.getTotalPoints()
            if yanivOpt:
                if totalPoints <= 6:
                    isLowest = turnPlayer.checkIfLowestHand(self.playersQueue)
                    if isLowest:
                        self.applyPenaltyToOtherPlayers(self.playersQueue)
                if totalPoints > 6 or not isLowest:
                    turnPlayer.updateTotalPoints(30)
                match_finished = self.verifyEndOfMatch()
                if match_finished:
                    self.setStatus(self.DEFINE_FINISHED_MATCH)
            else:
                self.setStatus(self.DEFINE_WAITING_FOR_REMOTE_ACTION)
            turnPlayer.toggleTurn()
            self.updatePlayersQueueIndex()
            self.playersQueue[0].toggleTurn()
            # send_move
            if yanivOpt and not match_finished:
                self.setStatus(self.DEFINE_FINISHED_ROUND)
                self.resetRound()
                #send_move
        else:
            messagebox.showinfo("Invalid action", "Invalid move")
            

    def distributeCards(self):
        for player in self.playersQueue:
            for _ in range(5):
                card = self.buyDeck.popCard()
                player.addCard(card)

    def getGUIImage(self) -> GUIImage:
        guiImage = GUIImage()
        turnPlayer = self.identifyTurnPlayer()
        name = turnPlayer.getName()
        cards = self.discardDeck.getCards()
        guiImage.setDiscardDeckFirstCard(cards[0])
        lenBuyDeck = self.buyDeck.getSize()
        guiImage.setBuyDeckEmpty(lenBuyDeck == 0)
        playersInfo = []
        for player in self.playersQueue:
            playerHand = player.getCurrentHand()
            id = player.getId()
            if id == self.getLocalPlayerId(): guiImage.setLocalPlayerCurrentHand(playerHand)
            nCards = len(playerHand)
            points = player.getTotalPoints()
            playerInfo = PlayerInfo(id, nCards, points)
            playersInfo.append(playerInfo)
        if "regularMove": #EGL 10/06/2024 -> discutir como obter regularMove, provavelmente
                          # setar uma variavel membro booleana regularMove e atualizar a cada acao 
            match self.status:
                case self.DEFINE_NO_MATCH:
                    message = "Start a match in the menu"
                case self.DEFINE_BUY_CARD_ACTION:
                    message = name + " must buy a card"
                case self.DEFINE_DISCARD_OR_SELECT_CARD_ACTION:
                    message = name + " must discard"
                case self.DEFINE_OPT_YANIV:
                    message = name + " must opt for yaniv"
                case self.DEFINE_WAITING_FOR_REMOTE_ACTION:
                    message = "Turn player: " + name
                case self.DEFINE_FINISHED_MATCH:
                    winner = self.getWinner()
                    message = "Winner: " + winner
                case self.DEFINE_WITHDRAWAL:
                    message = "Match abandonned by oponnent"
                case self.DEFINE_FINISHED_ROUND:
                    message = "Round finished!"
        else:
            message = "Irregular move"
        guiImage.setMessage(message)
        return guiImage

        
    def resetPlayerQueue(self):
        ...

    def orderPlayerQueue(self):
        ...
    
    def applyPenaltyToOtherPlayers(self, playersQueue: list):
        for player in playersQueue:
            if player.getTurn == False:
                player.updateTotalPoints(10)

    def resetRound(self):
        self.setStatus(self.DEFINE_BUY_CARD_ACTION)
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
    
    def getWinner(self) -> Player:
        for player in self.playersQueue:
            if player.getIsWinner(): return player

    def discardCards(self, cards: list):
        ...