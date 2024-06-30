import json
from Player import Player
from DiscardDeck import DiscardDeck
from BuyDeck import BuyDeck
from GUIImage import GUIImage
from PlayerInfo import PlayerInfo
from utils import POINTS_TO_END_A_MATCH

from Card import Card
from utils import NUMBER_OF_PLAYERS
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
    
    def setPlayersQueueIndex(self, index: int):
        self.playersQueueIndex = index

    def getPlayerQueueIndex(self) -> int:
        return self.playersQueueIndex
    
    def setPlayersQueue(self, playersQueue: list):
        self.playersQueue = [Player(p[1], p[0]) for p in playersQueue]

    def identifyTurnPlayer(self) -> Player:
        for player in self.playersQueue:
            if player.getTurn(): return player

    def getStatus(self) -> int:
        return self.status

    def setStatus(self, status: int):
        self.status = status

    def getRound(self) -> int:
        return self.round

    def isSet(self, cards : list) -> bool:
        s = set()
        for card in cards:
            value = card.getValue()
            if value != "Joker": s.add(value)
        return len(s) == 1

    def isSequence(self, cards: list) -> bool:
        for i in range(1,len(cards)):
            # se for coringa, não verifica se tem o mesmo naipe
            if cards[i].getValue() == "Joker" or cards[i-1].getValue() == "Joker": continue
            if cards[i].getSuit() != cards[i-1].getSuit(): return False

        values = [card.getNumber() for card in cards]
        values.sort()
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
        selectedDeck = self.buyDeck if isBuyDeck else self.discardDeck
        
        card = selectedDeck.popCard()
        turnPlayer.addCard(card)

    def discard(self):
        turnPlayer = self.identifyTurnPlayer()
        selectedCards = turnPlayer.getSelectedCards()
        if len(selectedCards) == 0:
            return False
        is_sequence = False
        if len(selectedCards) >= 2: is_set = self.isSet(selectedCards)
        if len(selectedCards) >= 3: is_sequence = self.isSequence(selectedCards)
        if len(selectedCards) == 1 or is_set or is_sequence:
            self.discardDeck.addCardsToDeck(selectedCards)
            turnPlayer.removeCardsFromHand(selectedCards)
            return True
        return False

    def receiveWithdrawalNotification(self):
        self.setStatus(self.DEFINE_WITHDRAWAL)
        
    def receiveMove(self, a_move: dict):
        code = ""
        if "code" in a_move: 
            code = a_move["code"].upper()
        if "playersQueue" in a_move:
            for p in json.loads(a_move["playersQueue"]):
                id = p["id"]
                name = p["name"]
                turn = p["turn"]
                isWinner = p["winner"]
                totalPoints = p["totalPoints"]
                player = Player(id, name)
                player.setTurn(turn)
                player.setWinner(isWinner)
                player.setTotalPoints(totalPoints)
                self.playersQueue.append(player)
        if code == "RESET ROUND":
            self.round = json.loads(a_move["round"])
            playersHands = json.loads(a_move['hands'])
            for player in self.playersQueue:
                playerHand = playersHands[player.getId()]
                hands_restored = [Card(card["id"], card["value"], card["suit"], card["points"], card["number"]) for card in playerHand]
                player.setCurrentHand(hands_restored)
            turnPlayer = self.identifyTurnPlayer()
            if turnPlayer.getId() == self.getLocalPlayerId():
                self.setStatus(self.DEFINE_BUY_CARD_ACTION)
            else:
                self.setStatus(self.DEFINE_WAITING_FOR_REMOTE_ACTION)
            self.discardDeck.setCards([Card(card["id"], card["value"], card["suit"], card["points"], card["number"]) for card in json.loads(a_move["discardDeck"])])
            self.buyDeck.setCards([Card(card["id"], card["value"], card["suit"], card["points"], card["number"]) for card in json.loads(a_move["buyDeck"])])
            if "playersQueueIndex" in a_move:
                self.setPlayersQueueIndex(json.loads(a_move["playersQueueIndex"]))
        if code == "BUY CARD":
            self.buyCard(a_move["isBuyDeck"])
        if code == "DISCARD":
            selected_cards = json.loads(a_move["selected_cards"])
            turnPlayerCurrentHand = self.identifyTurnPlayer().getCurrentHand()
            for card in turnPlayerCurrentHand:
                if card.getId() in selected_cards:
                    card.setSelected(True)
            self.discard()
        if code == "OPT YANIV":
            self.optYaniv(a_move["opt"])
            turnPlayer = self.identifyTurnPlayer()
            # Se o novo jogador da vez é o player remoto que recebeu a jogada do opt yaniv
            # seu status deve se tornar buy card action
            if turnPlayer.getId() == self.getLocalPlayerId():
                self.setStatus(self.DEFINE_BUY_CARD_ACTION)
        if code == "WITHDRAWAL":
            self.receiveWithdrawalNotification()
        #TODO: testar
        if a_move["match_status"] == "finished":
            self.playersQueue = []
            playersHands = json.loads(a_move['hands'])
            for p in json.loads(a_move["playersQueue"]):
                id = p["id"]
                name = p["name"]
                turn = p["turn"]
                isWinner = p["winner"]
                totalPoints = p["totalPoints"]
                player = Player(id, name)
                player.setTurn(turn)
                player.setWinner(isWinner)
                player.setTotalPoints(totalPoints)
                self.playersQueue.append(player)
                playerHand = playersHands[id]
                hands_restored = [Card(card["id"], card["value"], card["suit"], card["points"], card["number"]) for card in playerHand]
                player.setCurrentHand(hands_restored)
            self.setStatus(self.DEFINE_FINISHED_MATCH)


    
    def optYaniv(self, yanivOpt: bool) -> bool:
        turnPlayer = self.identifyTurnPlayer()
        totalPoints = sum([card.getPoints() for card in turnPlayer.getCurrentHand()])
        if yanivOpt:
            if totalPoints <= 6:
                isLowest = turnPlayer.checkIfLowestHand(self.playersQueue)
                if isLowest:
                    self.applyPenaltyToOtherPlayers()
            if totalPoints > 6 or not isLowest:
                turnPlayer.updateTotalPoints(30)
            match_finished = self.verifyEndOfMatch()
            
        turnPlayer.toggleTurn()

        self.updatePlayersQueueIndex()
        self.playersQueue[self.playersQueueIndex].toggleTurn()
        return match_finished if yanivOpt else False
            
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
        guiImage.setDiscardDeckFirstCard(cards[-1] if len(cards) else None)
        lenBuyDeck = self.buyDeck.getSize()
        guiImage.setBuyDeckEmpty(lenBuyDeck == 0)
        playersInfo = {}
        guiImage.setRound(self.round)
        for player in self.playersQueue:
            playerHand = player.getCurrentHand()
            id = player.getId()
            if id == self.getLocalPlayerId(): 
                guiImage.setLocalPlayerCurrentHand(playerHand)
            nCards = len(playerHand)
            points = player.getTotalPoints()
            pName = player.getName()
            playersInfo[id] = PlayerInfo(pName, id, nCards, points)
        guiImage.setPlayersInfo(playersInfo)
        match self.getStatus():
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
                message = "Winner: " + winner.getName()
            case self.DEFINE_WITHDRAWAL:
                message = "Match abandonned by oponnent"
            case self.DEFINE_FINISHED_ROUND:
                message = "Round finished!"

        guiImage.setMessage(message)
        return guiImage
    
    def applyPenaltyToOtherPlayers(self):
        for player in self.playersQueue:
            if not player.getTurn():
                player.updateTotalPoints(10)

    def resetGame(self):
        self.playersQueue = []
        self.discardDeck = DiscardDeck()
        self.buyDeck = BuyDeck()
        self.message = ""
        self.round = 0
        self.status = 0
        self.playersQueueIndex = 0
        self.localPlayerId = ""

    def resetRound(self):
        self.round += 1
        for player in self.playersQueue:
            cards = player.getCurrentHand()
            player.clearHand()
            self.buyDeck.addCardsToDeck(cards)
        discardCards = self.discardDeck.cleanAndReturnCards()
        self.buyDeck.addCardsToDeck(discardCards)
        self.buyDeck.shuffle()
        self.distributeCards()

    def verifyEndOfMatch(self) -> bool:
        MAXSCORE = POINTS_TO_END_A_MATCH
        for player in self.playersQueue:
            if player.getTotalPoints() >= MAXSCORE:
                return True
        return False

    def updatePlayersQueueIndex(self):
        self.playersQueueIndex = (self.playersQueueIndex + 1) % NUMBER_OF_PLAYERS

    def getLocalPlayerId(self) -> str:
        return self.localPlayerId
    
    def getWinner(self) -> Player:
        for player in self.playersQueue:
            if player.isWinner(): return player
    
    def startMatch(self):
        self.resetRound()
        self.toggleTurnById(self.localPlayerId)
    
    def selectCard(self, cardId: int):
        turnPlayer = self.identifyTurnPlayer()
        selectedCard = turnPlayer.findSelectedCardById(cardId)
        selectedCard.toggleSelected()

    def getPlayerIndexById(self, playerId: str) -> int:
        for i, player in enumerate(self.playersQueue):
            if player.getId() == playerId: return i

    def getPlayersQueue(self) -> list[Player]:
        return self.playersQueue.copy()