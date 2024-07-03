import json
import tkinter as tk
from tkinter import messagebox, simpledialog, Frame, Toplevel
from PIL import Image, ImageTk
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from Table import Table
from GUIImage import GUIImage
from Player import Player
from Card import Card
from utils import NUMBER_OF_PLAYERS

class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        self.mainWindow = tk.Tk()
        self.mainWindow.title("Yaniv")
        self.mainWindow.geometry("800x600")
        self.mainWindow.config(bg="darkgreen")
        self.mainWindow.resizable(width=False, height=False)
        self.createWidgets()
        self.createMenu()
        self.table = Table()
        self.dogActor = DogActor()
        self.connectToDogServer()
        self.mainWindow.mainloop()
    
    def connectToDogServer(self):
        playerName = simpledialog.askstring("Player name", "Enter your name")
        msg = self.dogActor.initialize(playerName, self)
        messagebox.showinfo("Connection", msg)
        if msg == "Conectado a Dog Server": return
        exit()

    def receive_start(self, start_status):
        self.table.resetGame()
        code = int(start_status.get_code())
        if code == 0 or code == 1:
            messagebox.showinfo("Problema", start_status.get_message())
            return
        messagebox.showinfo("Start", start_status.get_message())
        self.table.setLocalPlayerId(start_status.get_local_id())

    def createWidgets(self):
        self.buyLabel = tk.Label( self.mainWindow, text="Buy deck", bg="darkgreen", font=("Arial", 15), fg="white")
        self.buyLabel.place(relx=0.29, rely=0.34)
        
        self.discardLabel = tk.Label( self.mainWindow, text="Discard deck", bg="darkgreen", font=("Arial", 15), fg="white")
        self.discardLabel.place(relx=0.55, rely=0.34)

        self.discardButton = tk.Button( self.mainWindow, text="Discard", command=self.discard, width=10, height=2, bg="white")
        self.discardButton.place(relx=0.44, rely=0.6)

        self.callYanivButton = tk.Button( self.mainWindow, text="Call yaniv", command = lambda : self.optYaniv(True), width=10, height=2, bg="white")
        self.callYanivButton.place(relx=0.3, rely=0.7)

        self.dontCallYanivButton = tk.Button( self.mainWindow, text="Don't call yaniv", command= lambda : self.optYaniv(False), width=12, height=2, bg="white")
        self.dontCallYanivButton.place(relx=0.58, rely=0.7)

        self.imageBuyDeck= tk.PhotoImage(file="cards/back.png")
        self.buyDeck = tk.Label(self.mainWindow, image=self.imageBuyDeck, bd=0, bg="darkgreen")
        self.buyDeck.imagem = self.imageBuyDeck
        self.buyDeck.place(relx=0.3, rely=0.4)
        self.buyDeck.bind("<Button-1>", lambda event: self.buyCard(isBuyDeck=True))

        self.discardDeck= tk.Label(self.mainWindow, image="", bd=0, bg="darkgreen")
        self.discardDeck.place(relx=0.58, rely=0.4)
        self.discardDeck.bind("<Button-1>", lambda event: self.buyCard(isBuyDeck=False))

        self.roundLabel = tk.Label( self.mainWindow, text="Round: 0", bg="darkgreen", font=("Arial", 15), fg="white")
        self.roundLabel.place(relx=0.85, rely=0.02)

        self.messageLabel = tk.Label( self.mainWindow, text="", bg="darkgreen", font=("Arial", 12), fg="white")
        self.messageLabel.place(relx=0.42, rely=0.2)

        self.player1Cards, self.player2Cards, self.player3Cards, self.player4Cards = [],[],[],[]
        
        for i in range(6):
            card = tk.Label(self.mainWindow, bd=0, bg="darkgreen")
            card.place(relx=0.25 + i * 0.07, rely=0.8)
            self.player1Cards.append(card)

            card2 = tk.Label(self.mainWindow, bd=0, bg="darkgreen")
            card2.place(relx=0.85, rely=0.3 + i * 0.07)
            self.player2Cards.append(card2)

            card3 = tk.Label(self.mainWindow, bd=0, bg="darkgreen")
            card3.place(relx=0.3 + i * 0.07, rely=0.02)
            self.player3Cards.append(card3)
            
            card4 = tk.Label(self.mainWindow, bd=0, bg="darkgreen")
            card4.place(relx=0.02, rely=0.3 + i * 0.07)
            self.player4Cards.append(card4)

        frameScorePlayer1 = tk.Frame( self.mainWindow, bg="white", bd=1, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        frameScorePlayer1.place(relx=0.7, rely=0.9, relwidth=0.15, relheight=0.07)
        
        self.labelPlayer1 = tk.Label(frameScorePlayer1, text="Player 1", bg="white", font=("Arial", 8))
        self.labelPlayer1.place(relx=0.33, rely=0.01)
        
        self.labelPontuacaoPlayer1 = tk.Label(frameScorePlayer1, text="Score: 0", bg="white", font=("Arial", 8))
        self.labelPontuacaoPlayer1.place(relx=0.32, rely=0.5)

        frameScorePlayer2 = tk.Frame( self.mainWindow, bg="white", bd=1, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        frameScorePlayer2.place(relx=0.84, rely=0.2, relwidth=0.15, relheight=0.07)

        self.labelPlayer2 = tk.Label(frameScorePlayer2, text="Player 2", bg="white", font=("Arial", 8))
        self.labelPlayer2.place(relx=0.33, rely=0.01)
        
        self.labelPontuacaoPlayer2 = tk.Label(frameScorePlayer2, text="Score: 0", bg="white", font=("Arial", 8))
        self.labelPontuacaoPlayer2.place(relx=0.32, rely=0.5)

        frameScorePlayer3 = tk.Frame( self.mainWindow, bg="white", bd=1, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        frameScorePlayer3.place(relx=0.12, rely=0.05, relwidth=0.15, relheight=0.07)

        self.labelPlayer3 = tk.Label(frameScorePlayer3, text="Player 3", bg="white", font=("Arial", 8))
        self.labelPlayer3.place(relx=0.33, rely=0.01)

        self.labelPontuacaoPlayer3 = tk.Label(frameScorePlayer3, text="Score: 0", bg="white", font=("Arial", 8))
        self.labelPontuacaoPlayer3.place(relx=0.32, rely=0.5)

        frameScorePlayer4 = tk.Frame( self.mainWindow, bg="white", bd=1, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        frameScorePlayer4.place(relx=0.02, rely=0.72, relwidth=0.15, relheight=0.07)

        self.labelPlayer4 = tk.Label(frameScorePlayer4, text="Player 4", bg="white", font=("Arial", 8))
        self.labelPlayer4.place(relx=0.33, rely=0.01)

        self.labelPontuacaoPlayer4 = tk.Label(frameScorePlayer4, text="Score: 0", bg="white", font=("Arial", 8))
        self.labelPontuacaoPlayer4.place(relx=0.32, rely=0.5)

    def createMenu(self):
        self.menu = tk.Menu(self.mainWindow)
        self.menu.option_add("*tearOff", False)
        self.mainWindow["menu"] = self.menu

        self.menuFile = tk.Menu(self.menu, bg="white", fg="black")
        self.menu.add_cascade(menu=self.menuFile, label="Menu")

        self.menuFile.add_command(label="Rules", command=self.onClickRules)
        self.menuFile.add_command(label="Start game", command=self.startMatch)
        self.menuFile.add_command(label="Reset game", command=self.resetGame)
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Exit", command=self.onClickExit)

    def buyCard(self, isBuyDeck: bool):
        status = self.table.getStatus()
        turnPlayer = self.table.identifyTurnPlayer()
        localPlayerId = self.table.getLocalPlayerId()
        if status == self.table.DEFINE_BUY_CARD_ACTION and turnPlayer.getId() == localPlayerId:
            if self.table.buyCard(isBuyDeck):
                move_to_send = {
                    "match_status": "progress",
                    "code": "BUY CARD",
                    "isBuyDeck": isBuyDeck
                }
                self.dogActor.send_move(move_to_send)
                self.table.setStatus(self.table.DEFINE_DISCARD_OR_SELECT_CARD_ACTION)
                guiImage = self.table.getGUIImage()
                self.updateGui(guiImage)
            else:
                messagebox.showinfo("Erro ao comprar", "Baralho vazio")
        elif turnPlayer.getId() != localPlayerId:
            messagebox.showinfo("Erro ao comprar", "Não é sua vez de comprar")
        else:
            messagebox.showinfo("Erro ao comprar", "Não é hora de comprar")

    def discard(self):
        status = self.table.getStatus()
        turnPlayer = self.table.identifyTurnPlayer()
        localPlayerId = self.table.getLocalPlayerId()
        if status == self.table.DEFINE_DISCARD_OR_SELECT_CARD_ACTION and turnPlayer.getId() == localPlayerId:
            selected_cards = turnPlayer.getSelectedCards()
            validDiscard = self.table.discard()
            if not validDiscard:
                messagebox.showinfo("Erro ao descartar", "Descarte inválido")
                return
            move_to_send = {
                "match_status": "progress",
                "code": "DISCARD",
                "selected_cards" : json.dumps([card.getId() for card in selected_cards]),
            }
            self.dogActor.send_move(move_to_send)
            self.table.setStatus(self.table.DEFINE_OPT_YANIV)
            guiImage = self.table.getGUIImage()
            self.updateGui(guiImage)
        elif turnPlayer.getId() != localPlayerId: messagebox.showinfo("Erro ao descartar", "Não é sua vez de descartar")
        else: messagebox.showinfo("Erro ao descartar", "Não é hora de descartar")

    def selectCard(self, cardId: int):
        status = self.table.getStatus()
        turnPlayer = self.table.identifyTurnPlayer()
        localPlayerId = self.table.getLocalPlayerId()
        if status == self.table.DEFINE_DISCARD_OR_SELECT_CARD_ACTION and turnPlayer.getId() == localPlayerId:
            self.table.selectCard(cardId)
            guiImage = self.table.getGUIImage()
            self.updateGui(guiImage)
        elif turnPlayer.getId() != localPlayerId: messagebox.showinfo("Erro ao selecionar carta", "Não é sua vez de selecionar carta")
        else: messagebox.showinfo("Erro ao selecionar carta", "Não é hora de selecionar carta")

    def onClickRules(self):
        # Creating de child window
        rules_window=Toplevel(self.mainWindow)
        rules_window.geometry("1080x720")
        rules_window.title("Regras")
        rules_window["bg"]="#FFF7F0"

        # Creating a frame to be inside of the window to handle the layout better
        unique_frame = Frame(rules_window, bg= "#FFF7F0")
        unique_frame.pack(fill= 'both', expand = True, padx= 8, pady=16)

        # Labels to show the actual text of the rules
        # Each Label is a section inside the frame
        tk.Label(unique_frame, text="Regras do jogo\n",
                 justify='left', font="Arial 12 bold", bg="#FFF7F0").grid(sticky = 'w', column=0, row=1)

        tk.Label(unique_frame, text="A cada rodada, todos jogadores iniciam com 5 cartas.\n",
                 justify='left', font="Arial 11", bg="#FFF7F0").grid(sticky = 'w', column=0, row=2)

        tk.Label(unique_frame, text="As jogadas são alternadas. Na sua vez você deve:\n   1. Comprar uma carta (monte de compra ou descarte).\n   2. Descartar.\n   3. Optar por chamar yaniv ou não.",
                 justify='left', font="Arial 11", bg="#FFF7F0").grid(sticky = 'w', column=0, row=3)
        
        tk.Label(unique_frame, text="A pontuação das cartas segue como o seu próprio valor, exceto as especiais(Q,J,K) que valem 10 e o Joker que vale 0.",
                 justify='left', font="Arial 11", bg="#FFF7F0").grid(sticky = 'w', column=0, row=4)

        tk.Label(unique_frame, text="\nVocê pode descartar:\n  - Apenas uma carta;\n  - Sequência de no mínimo 3 cartas do mesmo naipe. Ex: 10 J Q K de ouros;\n  - Conjunto de no mínimo 2 cartas (mesmo valor, naipes diferentes)."+
                " Ex: 3 de ouros e 3 de copas;\nO uso dos coringas pode ser útil para completar uma carta ausente para formar uma sequência válida. Entretanto, lembre-se que o seu valor é 0 e pode ser útil para confundir o adversário acerca do valor da sua mão.",
                 justify='left', font="Arial 11", bg="#FFF7F0").grid(sticky = 'w', column=0, row=5)

        tk.Label(unique_frame, text="\nAo chamar yaniv, a rodada é encerrada. Para quem chamou yaniv ganhar a rodada, o mesmo deve possuir <= 6 pontos em sua mão e ser a pontuação mais baixa da mesa.",
                 justify='left', font="Arial 11", bg="#FFF7F0").grid(sticky = 'w', column=0, row=6)

        tk.Label(unique_frame, text="\nCaso o jogador que chamou yaniv cumprir todos os requisitos, todos outros jogadores recebem uma penalidade de 10 pontos.\nCaso contrário, o jogador recebe 30 pontos de penalidade.",
                 justify='left', font="Arial 11", bg="#FFF7F0").grid(sticky = 'w', column=0, row=7)
        
        tk.Label(unique_frame, text="\nA partida encerra quando um jogador chegar a 100 pontos. Ganha quem possuir a menor pontuação.\nCaso haja empate, ganha o jogador que tiver menos pontos em suas mãos.\nCaso haja novo empate, o vencedor é sorteado.",
                 justify='left', font="Arial 11", bg="#FFF7F0").grid(sticky = 'w', column=0, row=8)

    def resetGame(self):
        status = self.table.getStatus()
        if status == self.table.DEFINE_FINISHED_MATCH or status == self.table.DEFINE_WITHDRAWAL:
            self.table.resetGame()
            self.startMatch()
        else: messagebox.showinfo("Erro ao resetar partida", "Partida já iniciada")

    def onClickExit(self):
        self.mainWindow.destroy()

    def optYaniv(self, opt):
        status = self.table.getStatus()
        turnPlayer = self.table.identifyTurnPlayer()
        localPlayerId = self.table.getLocalPlayerId()
        if status == self.table.DEFINE_OPT_YANIV and turnPlayer.getId() == localPlayerId:
            match_finished = self.table.optYaniv(opt)
            move_to_send = {
                "match_status": "next",
                "code": "OPT YANIV",
                "opt": opt,
            }
            self.dogActor.send_move(move_to_send)
            if opt and not match_finished:
                self.table.setStatus(self.table.DEFINE_WAITING_FOR_REMOTE_ACTION)
                tk.messagebox.showinfo("Round finished", "Round finished")
                self.table.resetRound()
                playersQueue = self.table.getPlayersQueue()
                localPlayerId = self.table.getLocalPlayerId()
                hands = {player.getId(): player.getCurrentHand() for player in playersQueue}
                hands_serializable = {playerId: [card.__dict__ for card in hand] for playerId, hand in hands.items()}
                move_to_send = {
                    "match_status": "next",
                    "code": "RESET ROUND",
                    "hands": json.dumps(hands_serializable),
                    "buyDeck": json.dumps(self.table.buyDeck.getCards(), default=self.convertToJson),
                    "discardDeck": json.dumps(self.table.discardDeck.getCards(), default=self.convertToJson),
                    "round": self.table.getRound(),
                    "fromYaniv": True,
                }
                self.dogActor.send_move(move_to_send)
            elif opt and match_finished:
                self.table.setStatus(self.table.DEFINE_FINISHED_MATCH)
                tk.messagebox.showinfo("Match finished", "Match finished")
                self.table.setGameWinner()
                playersQueue = self.table.getPlayersQueue()
                hands = {player.getId(): player.getCurrentHand() for player in playersQueue}
                hands_serializable = {playerId: [card.__dict__ for card in hand] for playerId, hand in hands.items()}
                move_to_send = {
                    "match_status": "finished",
                    "hands": json.dumps(hands_serializable),
                    "playersQueue": json.dumps(self.table.getPlayersQueue(),  default=self.convertToJson),
                }
                self.dogActor.send_move(move_to_send)
            elif not opt and not match_finished: self.table.setStatus(self.table.DEFINE_WAITING_FOR_REMOTE_ACTION)
            guiImage = self.table.getGUIImage()
            self.updateGui(guiImage)
        elif turnPlayer.getId() != localPlayerId: messagebox.showinfo("Erro ao chamar yaniv", "Não é sua vez de optar por yaniv")
        else: messagebox.showinfo("Erro ao chamar yaniv", "Não é hora de optar por yaniv")
    
    def startMatch(self):
        status = self.table.getStatus()
        if status in (self.table.DEFINE_FINISHED_MATCH, self.table.DEFINE_NO_MATCH, self.table.DEFINE_WITHDRAWAL):
            answer = messagebox.askyesno("Start", "Start a new match?")
            if answer:
                startStatus = self.dogActor.start_match(NUMBER_OF_PLAYERS)
                code = startStatus.get_code()
                message = startStatus.get_message()
                if code == "0" or code == "1":
                    messagebox.showinfo("Dog error", message)
                elif code == "2":
                    players = startStatus.get_players()
                    localPlayerId = startStatus.get_local_id()
                    self.table.setPlayersQueue(players)
                    self.table.setLocalPlayerId(localPlayerId)
                    indexPlayer = self.table.getPlayerIndexById(localPlayerId)
                    self.table.setPlayersQueueIndex(indexPlayer)
                    self.table.startMatch()
                    hands = {player.getId(): player.getCurrentHand() for player in self.table.getPlayersQueue()}
                    hands_serializable = {playerId: [card.__dict__ for card in hand] for playerId, hand in hands.items()}
                        
                    move_to_send = {
                        "match_status": "progress",
                        "code": "RESET ROUND",
                        "hands": json.dumps(hands_serializable),
                        "buyDeck": json.dumps(self.table.buyDeck.getCards(), default=self.convertToJson),
                        "discardDeck": json.dumps(self.table.discardDeck.getCards(), default=self.convertToJson),
                        "playersQueue": json.dumps(self.table.getPlayersQueue(),  default=self.convertToJson),
                        "playersQueueIndex": json.dumps(indexPlayer),
                        "round": self.table.getRound(),
                        "fromYaniv": False,
                    }
                    self.dogActor.send_move(move_to_send)
                    self.table.setStatus(self.table.DEFINE_BUY_CARD_ACTION)
                    guiImage = self.table.getGUIImage()
                    self.updateGui(guiImage)
        else: messagebox.showinfo("Erro ao iniciar partida", "Partida já iniciada")
    
    def convertToJson(self, obj):
        if isinstance(obj, (Card, Player)):
            return obj.__dict__

    def receive_move(self, a_move):
        if "code" in a_move and a_move["code"] == "RESET ROUND":
            if a_move["fromYaniv"]: messagebox.showinfo("Round finished", "Round finished")
        if a_move["match_status"] == "finished": messagebox.showinfo("Match finished", "Match finished")
        self.table.receiveMove(a_move)
        guiImage = self.table.getGUIImage()
        self.updateGui(guiImage)

    def receive_withdrawal_notification(self):
        self.table.setStatus(self.table.DEFINE_WITHDRAWAL)
        guiImage = self.table.getGUIImage()
        self.updateGui(guiImage)
                
    def updateGui(self, guiImage: GUIImage):
        select_card = lambda x: (lambda p: self.selectCard(x))
        for i, card in enumerate(guiImage.getLocalPlayerCurrentHand()):
            cardLabel = self.player1Cards[i]
            cardImage = ImageTk.PhotoImage(Image.open(f"cards/{card.getValue()}{card.getSuit()}.png"))
            cardLabel.config(image = cardImage, borderwidth = 2 if card.isSelected() else 0, relief="solid")
            cardLabel.photo_ref = cardImage
            cardLabel.bind("<Button-1>", select_card(card.getId()))
        for j in range(6 - len(guiImage.getLocalPlayerCurrentHand())):
            cardLabel = self.player1Cards[-(j + 1)]
            cardLabel.config(image = "", borderwidth = 0)
        
        topOfDiscardDeck = guiImage.getDiscardDeckFirstCard()
        if topOfDiscardDeck is not None:
            cardImage = ImageTk.PhotoImage(Image.open(f"cards/{topOfDiscardDeck.getValue()}{topOfDiscardDeck.getSuit()}.png"))
            self.discardDeck.config(image = cardImage)
            self.discardDeck.photo_ref = cardImage
        else:
            self.discardDeck.config(image = "")

        isBuyDeckEmpty = guiImage.getBuyDeckEmpty()
        if isBuyDeckEmpty:
            self.buyDeck.config(image = "")
        else:
            self.buyDeck.config(image = self.imageBuyDeck)
            self.buyDeck.photo_ref = self.imageBuyDeck

        round = guiImage.getRound()
        self.roundLabel.config(text = f"Round: {round}")

        message = guiImage.getMessage()
        self.messageLabel.config(text = message)

        playersInfo = guiImage.getPlayersInfo()

        i = self.table.getPlayerIndexById(self.table.getLocalPlayerId())

        self.labelPontuacaoPlayer1.config(text = f"Score: {playersInfo[self.table.getLocalPlayerId()].getPoints()}")
        self.labelPlayer1.config(text = playersInfo[self.table.getLocalPlayerId()].getPlayerName())

        if NUMBER_OF_PLAYERS == 4:
            names = [self.labelPlayer2, self.labelPlayer3, self.labelPlayer4]
            scores = [self.labelPontuacaoPlayer2, self.labelPontuacaoPlayer3, self.labelPontuacaoPlayer4]
            cards = [self.player2Cards, self.player3Cards, self.player4Cards]
            cards_images = ["backRight", "backUpsideDown", "backLeft"]
        elif NUMBER_OF_PLAYERS == 2:
            names = [self.labelPlayer2]
            scores = [self.labelPontuacaoPlayer2]
            cards = [self.player2Cards]
            cards_images = ["backRight"]

        playersQueue = self.table.getPlayersQueue()
        for j in range(len(scores)):
            playerInfo = playersInfo[playersQueue[(i+j+1) % NUMBER_OF_PLAYERS].getId()]
            scores[j].config(text = f"Score: {playerInfo.getPoints()}")
            names[j].config(text = playerInfo.getPlayerName())
            for m in range(playerInfo.getNumberOfCards()):
                img = ImageTk.PhotoImage(Image.open(f"cards/{cards_images[j]}.png"))
                cards[j][m].config(image = img)
                cards[j][m].photo_ref = img
            for n in range(6 - playerInfo.getNumberOfCards()):
                cards[j][-(n+1)].config(image = "")