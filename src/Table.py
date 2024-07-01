import json
import random
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
            if cards[i].getValue() == "Joker" or cards[i-1].getValue() == "Joker": continue
            if cards[i].getSuit() != cards[i-1].getSuit(): return False

        values = [card.getNumber() for card in cards]
        values.sort()
        countJokers = 0
        for i in range(1, len(values)):
            if values[i] == 0: 
                countJokers += 1
                continue
            if values[i-1] == 0: continue
            diff = values[i] - values[i-1]
            if diff == 0: return False
            if diff != 1:
                if countJokers >= diff - 1:
                    countJokers -= diff - 1
                else:
                    return False
        return True

    def buyCard(self, isBuyDeck: bool) -> bool:
        turnPlayer = self.identifyTurnPlayer()
        selectedDeck = self.buyDeck if isBuyDeck else self.discardDeck
        if selectedDeck.getSize() == 0: return False
        card = selectedDeck.popCard()
        turnPlayer.addCard(card)
        return True

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

    def receiveMove(self, a_move: dict):
        code = ""
        if "code" in a_move: 
            code = a_move["code"].upper()
        if "playersQueue" in a_move:
            for p in json.loads(a_move["playersQueue"]):
                self.playersQueue.append(Player(p["id"], p["name"], p["turn"], p["totalPoints"], [], p["winner"] ))
        if "hands" in a_move:
            playersHands = json.loads(a_move['hands'])
            for player in self.playersQueue:
                playerHand = playersHands[player.getId()]
                hands_restored = [Card(card["id"], card["value"], card["suit"], card["points"], card["number"]) for card in playerHand]
                player.setCurrentHand(hands_restored)
        if "discardDeck" in a_move and "buyDeck" in a_move:
            self.discardDeck.setCards([Card(card["id"], card["value"], card["suit"], card["points"], card["number"]) for card in json.loads(a_move["discardDeck"])])
            self.buyDeck.setCards([Card(card["id"], card["value"], card["suit"], card["points"], card["number"]) for card in json.loads(a_move["buyDeck"])])
        if "playersQueueIndex" in a_move:
                self.setPlayersQueueIndex(json.loads(a_move["playersQueueIndex"]))
        if code == "RESET ROUND":
            self.round = json.loads(a_move["round"])
            turnPlayer = self.identifyTurnPlayer()
            self.setStatus(self.DEFINE_BUY_CARD_ACTION if turnPlayer.getId() == self.getLocalPlayerId() else self.DEFINE_WAITING_FOR_REMOTE_ACTION)
        elif code == "BUY CARD":
            self.buyCard(a_move["isBuyDeck"])
        elif code == "DISCARD":
            selected_cards = json.loads(a_move["selected_cards"])
            turnPlayerCurrentHand = self.identifyTurnPlayer().getCurrentHand()
            for card in turnPlayerCurrentHand:
                if card.getId() in selected_cards: card.setSelected(True)
            self.discard()
        elif code == "OPT YANIV":
            self.optYaniv(a_move["opt"])
            turnPlayer = self.identifyTurnPlayer()
            if turnPlayer.getId() == self.getLocalPlayerId():
                self.setStatus(self.DEFINE_BUY_CARD_ACTION)
        if a_move["match_status"] == "finished":
            self.setStatus(self.DEFINE_FINISHED_MATCH)
    
    def optYaniv(self, yanivOpt: bool) -> bool:
        turnPlayer = self.identifyTurnPlayer()
        totalPoints = turnPlayer.getCurrentHandTotalPoints()
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
                message = "You must buy a card"
            case self.DEFINE_DISCARD_OR_SELECT_CARD_ACTION:
                message = "You must discard"
            case self.DEFINE_OPT_YANIV:
                message = "You must opt for yaniv"
            case self.DEFINE_WAITING_FOR_REMOTE_ACTION:
                message = "Turn player: " + turnPlayer.getName()
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
    
    def setWinner(self):
        playersPoints = [player.getTotalPoints() for player in self.getPlayersQueue()]
        for player in self.getPlayersQueue():
            if player.getTotalPoints() == min(playersPoints):
                player.setWinner(True)
        winners = [player for player in self.getPlayersQueue() if player.isWinner()]
        winner = winners[0]
        if len(winners) > 1:
            minPoints = winners[0].getCurrentHandTotalPoints()
            for player in winners:
                playerCurrHandPoints = player.getCurrentHandTotalPoints()
                if playerCurrHandPoints < minPoints:
                    minPoints = playerCurrHandPoints
            winners = [player for player in winners if player.getCurrentHandTotalPoints() == minPoints]        
            winner = winners[0]
            if len(winners) > 1:
                winner = random.choice(winners)
            for player in self.table.getPlayersQueue():
                if player.getId() != winner.getId():
                    player.setWinner(False)