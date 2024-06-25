from Player import Player
from DiscardDeck import DiscardDeck
from BuyDeck import BuyDeck
from GUIImage import GUIImage
from PlayerInfo import PlayerInfo
from tkinter import messagebox
class Table:
    def __init__(self):
        self.playersQueue = []
        self.discardDeck = DiscardDeck()
        self.buyDeck = BuyDeck()
        self.message = ""
        self.round = 0
        self.status = 0
        self.playersQueueIndex = 0
        self.localPlayerId = ""
        self.regularMove = True

        self.DEFINE_NO_MATCH = 0
        self.DEFINE_BUY_CARD_ACTION = 1
        self.DEFINE_DISCARD_OR_SELECT_CARD_ACTION = 2
        self.DEFINE_OPT_YANIV = 3
        self.DEFINE_WAITING_FOR_REMOTE_ACTION = 4
        self.DEFINE_FINISHED_MATCH = 5
        self.DEFINE_WITHDRAWAL = 6
        self.DEFINE_FINISHED_ROUND = 7

    def setLocalPlayerId(self, localPlayerId: str):
        self.localPlayerId = localPlayerId

    def toggleTurnById(self, id: str):
        for player in self.playersQueue:
            if player.getId() == id:
                player.toggleTurn()
    
    def setPlayersQueue(self, playersQueue: list):
        self.playersQueue = [Player(p[1], p[0]) for p in playersQueue]

    def identifyTurnPlayer(self) -> Player:
        for player in self.playersQueue:
            if player.getTurn(): return player
            print('não é o player da vez')

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
            # se for coringa, não verifica se tem o mesmo naipe
            if cards[i].getValue() == "Joker" or cards[i-1].getValue() == "Joker": continue
            if cards[i].getSuit() != cards[i-1].getSuit(): return False

        values = [card.getNumber() for card in cards].sort()
        # contador de coringas
        countJokers = 0
        for i in range(1, len(values)):
            # se leu coringa, incrementa
            if values[i] == 0: 
                countJokers += 1
                continue
            # se a carta atual ou a anterior for um coringa, continua
            if values[i] == 0 or values[i-1] == 0: continue
            # se a carta atual - a anterior não for 1, tenta gastar um coringa
            diff = values[i] - values[i-1]
            if diff == 0: return False
            if diff != 1:
                # se tem coringas, gasta quantos precisam pra preencher o "espaço" entre as cartas
                if countJokers >= diff - 1:
                    countJokers -= diff - 1
                # senão ta errado
                else:
                    return False
        return True

    def buyCard(self, isBuyDeck: bool):
        turnPlayer = self.identifyTurnPlayer()
        print(f"Player da vez é {turnPlayer.getName()}")
        status = self.getStatus()
        localPlayerId = self.getLocalPlayerId()
        selectedDeck = self.buyDeck if isBuyDeck else self.discardDeck
        numCards = selectedDeck.getSize()
        if status == self.DEFINE_BUY_CARD_ACTION and turnPlayer.getId() == localPlayerId and numCards > 0:
            card = selectedDeck.popCard()
            turnPlayer.addCard(card)
            self.setStatus(self.DEFINE_DISCARD_OR_SELECT_CARD_ACTION)
            self.regularMove = True
        else:
            print(f"DEFINE_BUY_CARD_ACTION != {status} ou {localPlayerId} != {turnPlayer.getId()} ou {numCards} <= 0:")
            messagebox.showinfo("Invalid action", "You can't buy a card now")
            self.regularMove = False

    def discard(self):
        turnPlayer = self.identifyTurnPlayer()
        status = self.getStatus()
        localPlayerId = self.getLocalPlayerId()
        if status == self.DEFINE_DISCARD_OR_SELECT_CARD_ACTION and turnPlayer.getId() == localPlayerId:
            selectedCards = turnPlayer.getSelectedCards()
            if len(selectedCards) == 0:
                messagebox.showinfo("Selecione uma carta", "Selecione pelo menos uma carta")
                return False
            if len(selectedCards) >= 2:
                is_set = self.isSet(selectedCards)
            if len(selectedCards) >= 3:
                is_sequence = self.isSequence(selectedCards)
            if len(selectedCards) == 1 or is_set or is_sequence:
                self.discardDeck.addCardsToDeck(selectedCards)
                turnPlayer.removeCardsFromHand(selectedCards)
                self.setStatus(self.DEFINE_OPT_YANIV)
                self.regularMove = True
            else:
                messagebox.showinfo("Invalid action", "Invalid move")
                self.regularMove = False


    def receiveWithdrawalNotification(self):
        self.setStatus(self.DEFINE_WITHDRAWAL)
        
    def receiveMove(self, a_move: dict):
        code = a_move["code"]
        if code == "RESET ROUND":
            for player in self.playersQueue:
                player.setCurrentHand(a_move[f"player{player.getId()} hand"])
            self.discardDeck.setCards(a_move["discardDeck"])
            self.buyDeck.setCards(a_move["buyDeck"])
        if code == "BUY CARD":
            self.buyCard()
        if code == "DISCARD":
            self.discard()
        if code == "YANIV":
            self.optYaniv(a_move["yanivOpt"])
        if code == "WITHDRAWAL":
            self.receiveWithdrawalNotification()
    
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
            self.regularMove = True
            return match_finished
        else:
            messagebox.showinfo("Invalid action", "Invalid move")
            self.regularMove = False
            

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
        guiImage.setDiscardDeckFirstCard(cards[0] if len(cards) else None)
        lenBuyDeck = self.buyDeck.getSize()
        guiImage.setBuyDeckEmpty(lenBuyDeck == 0)
        playersInfo = []
        for player in self.playersQueue:
            playerHand = player.getCurrentHand()
            id = player.getId()
            if id == self.getLocalPlayerId(): 
                guiImage.setLocalPlayerCurrentHand(playerHand)
                for card in playerHand:
                    print(card.__dict__)
            nCards = len(playerHand)
            points = player.getTotalPoints()
            playerInfo = PlayerInfo(id, nCards, points)
            playersInfo.append(playerInfo)
        if self.regularMove: #EGL 10/06/2024 -> discutir como obter regularMove, provavelmente
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
        self.playersQueue.sort(key=lambda x: x.id)
    
    def applyPenaltyToOtherPlayers(self):
        for player in self.playersQueue:
            if player.getTurn == False:
                player.updateTotalPoints(10)

    def resetGame(self):
        status = self.getStatus()
        turnPlayer = self.identifyTurnPlayer()
        if status == self.DEFINE_FINISHED_MATCH or status == self.DEFINE_WITHDRAWAL:
            for player in self.playersQueue:
                player.setTotalPoints(0)
                player.setWinner(False)
            self.resetRound()
            turnPlayer.toggleTurn()
            self.updatePlayersQueueIndex()
            self.playersQueue[0].toggleTurn()
        else:
            messagebox.showinfo("Invalid action", "You can't reset the game now")


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
    
    def startMatch(self):
        self.resetRound()
        self.toggleTurnById(self.localPlayerId)
        #self.orderPlayerQueue()
    
    def selectCard(self, cardId: int):
        print("chegou ", cardId)
        turnPlayer = self.identifyTurnPlayer()
        status = self.getStatus()
        localPlayerId = self.getLocalPlayerId()
        if status == self.DEFINE_DISCARD_OR_SELECT_CARD_ACTION and turnPlayer.getId() == localPlayerId:
            selectedCard = turnPlayer.findSelectedCardById(cardId)
            print("achou", selectedCard.__dict__)
            selectedCard.toggleSelected()
        else:
            print(f"Status = {status} != 2 ou {turnPlayer.getId()} != {localPlayerId} ")
            messagebox.showinfo("Invalid action", "You can't select a card now")