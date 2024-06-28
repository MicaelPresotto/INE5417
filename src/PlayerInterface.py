import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from Table import Table
from GUIImage import GUIImage
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
        self.connectingToDogServer()
        self.mainWindow.mainloop()
    
    def connectingToDogServer(self):
        playerName = simpledialog.askstring("Player name", "Enter your name")
        msg = self.dogActor.initialize(playerName, self)
        messagebox.showinfo("Connection", msg)
        if msg == "Conectado a Dog Server":
            return
        exit()

    def receive_start(self, start_status):
        code = int(start_status.code)
        if code == 0 or code == 1:
            messagebox.showinfo("Problema", start_status.message)
            return
        messagebox.showinfo("Start", start_status.message)

    def createWidgets(self):
        self.buyLabel = tk.Label(
            self.mainWindow,
            text="Buy deck",
            bg="darkgreen",
            font=("Arial", 15),
            fg="white",
        )
        self.discardLabel = tk.Label(
            self.mainWindow,
            text="Discard deck",
            bg="darkgreen",
            font=("Arial", 15),
            fg="white",
        )
        self.buyLabel.place(relx=0.29, rely=0.34)
        self.discardLabel.place(relx=0.55, rely=0.34)

        self.discardButton = tk.Button(
            self.mainWindow,
            text="Discard",
            command=self.discard,
            width=10,
            height=2,
            bg="white",
        )
        self.discardButton.place(relx=0.44, rely=0.6)

        self.callYanivButton = tk.Button(
            self.mainWindow,
            text="Call yaniv",
            command = lambda : self.optYaniv(True),
            width=10,
            height=2,
            bg="white",
        )

        self.callYanivButton.place(relx=0.3, rely=0.7)

        self.dontCallYanivButton = tk.Button(
            self.mainWindow,
            text="Don't call yaniv",
            command= lambda : self.optYaniv(False),
            width=12,
            height=2,
            bg="white",
        )
        self.dontCallYanivButton.place(relx=0.58, rely=0.7)

        imageBuyDeck= tk.PhotoImage(file="cards/back.png")
        buyDeck = tk.Label(self.mainWindow, image=imageBuyDeck, bd=0, bg="darkgreen")
        buyDeck.imagem = imageBuyDeck
        buyDeck.place(relx=0.3, rely=0.4)
        buyDeck.bind("<Button-1>", lambda event: self.buyCard(isBuyDeck=True))

        self.discardDeck= tk.Label(
            self.mainWindow, image="", bd=0, bg="darkgreen"
        )
        self.discardDeck.place(relx=0.58, rely=0.4)
        self.discardDeck.bind("<Button-1>", lambda event: self.buyCard(isBuyDeck=False))

        self.roundLabel = tk.Label(
            self.mainWindow,
            text="Round: 0",
            bg="darkgreen",
            font=("Arial", 15),
            fg="white",
        )

        self.roundLabel.place(relx=0.85, rely=0.02)

        self.messageLabel = tk.Label(
            self.mainWindow,
            text="",
            bg="darkgreen",
            font=("Arial", 12),
            fg="white",
        )

        self.messageLabel.place(relx=0.42, rely=0.2)

        self.roundLabel.place(relx=0.85, rely=0.02)

        self.player1Cards: list[tk.Label] = []
        self.player2Cards: list[tk.Label] = []
        self.player3Cards: list[tk.Label] = []
        self.player4Cards: list[tk.Label] = []
        # bottom
        for i in range(6):
            card = tk.Label(self.mainWindow, bd=0, bg="darkgreen")
            card.place(relx=0.25 + i * 0.07, rely=0.8)
            self.player1Cards.append(card)

        # left
        for i in range(6):
            card = tk.Label(self.mainWindow, bd=0, bg="darkgreen")
            card.place(relx=0.02, rely=0.3 + i * 0.07)
            self.player4Cards.append(card)

        # right
        for i in range(6):
            card = tk.Label(self.mainWindow, bd=0, bg="darkgreen")
            card.place(relx=0.85, rely=0.3 + i * 0.07)
            self.player2Cards.append(card)


        # top
        for i in range(6):
            card = tk.Label(self.mainWindow, bd=0, bg="darkgreen")
            card.place(relx=0.3 + i * 0.07, rely=0.02)
            self.player3Cards.append(card)

        frameScorePlayer1 = tk.Frame(
            self.mainWindow,
            bg="white",
            bd=1,
            borderwidth=2,
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
        )
        frameScorePlayer1.place(relx=0.7, rely=0.9, relwidth=0.15, relheight=0.07)
        self.labelPlayer1 = tk.Label(
            frameScorePlayer1, text="Player 1", bg="white", font=("Arial", 8)
        )
        self.labelPlayer1.place(relx=0.33, rely=0.01)
        self.labelPontuacaoPlayer1 = tk.Label(
            frameScorePlayer1, text="Score: 0", bg="white", font=("Arial", 8)
        )
        self.labelPontuacaoPlayer1.place(relx=0.32, rely=0.5)

        frameScorePlayer2 = tk.Frame(
            self.mainWindow,
            bg="white",
            bd=1,
            borderwidth=2,
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
        )
        frameScorePlayer2.place(relx=0.84, rely=0.2, relwidth=0.15, relheight=0.07)
        self.labelPlayer2 = tk.Label(
            frameScorePlayer2, text="Player 2", bg="white", font=("Arial", 8)
        )
        self.labelPlayer2.place(relx=0.33, rely=0.01)
        self.labelPontuacaoPlayer2 = tk.Label(
            frameScorePlayer2, text="Score: 0", bg="white", font=("Arial", 8)
        )
        self.labelPontuacaoPlayer2.place(relx=0.32, rely=0.5)

        frameScorePlayer3 = tk.Frame(
            self.mainWindow,
            bg="white",
            bd=1,
            borderwidth=2,
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
        )
        frameScorePlayer3.place(relx=0.12, rely=0.05, relwidth=0.15, relheight=0.07)
        self.labelPlayer3 = tk.Label(
            frameScorePlayer3, text="Player 3", bg="white", font=("Arial", 8)
        )
        self.labelPlayer3.place(relx=0.33, rely=0.01)
        self.labelPontuacaoPlayer3 = tk.Label(
            frameScorePlayer3, text="Score: 0", bg="white", font=("Arial", 8)
        )
        self.labelPontuacaoPlayer3.place(relx=0.32, rely=0.5)

        frameScorePlayer4 = tk.Frame(
            self.mainWindow,
            bg="white",
            bd=1,
            borderwidth=2,
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
        )
        frameScorePlayer4.place(relx=0.02, rely=0.72, relwidth=0.15, relheight=0.07)
        self.labelPlayer4 = tk.Label(
            frameScorePlayer4, text="Player 4", bg="white", font=("Arial", 8)
        )
        self.labelPlayer4.place(relx=0.33, rely=0.01)
        self.labelPontuacaoPlayer4 = tk.Label(
            frameScorePlayer4, text="Score: 0", bg="white", font=("Arial", 8)
        )
        self.labelPontuacaoPlayer4.place(relx=0.32, rely=0.5)

    def createMenu(self):
        self.menu = tk.Menu(self.mainWindow)
        self.menu.option_add("*tearOff", False)
        self.mainWindow["menu"] = self.menu

        self.menuFile = tk.Menu(self.menu, bg="white", fg="black")
        self.menu.add_cascade(menu=self.menuFile, label="Menu")

        self.menuFile.add_command(label="Rules", command=self.onClickRules)
        self.menuFile.add_command(label="Start game", command=self.startMatch)
        self.menuFile.add_command(label="Reset game", command=self.onClickReset)
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Exit", command=self.onClickExit)

    def buyCard(self, isBuyDeck):
        self.table.buyCard(isBuyDeck)
        #send move
        guiImage = self.table.getGUIImage()
        self.updateGui(guiImage)

    def discard(self):
        self.table.discard()
        #send move
        guiImage = self.table.getGUIImage()
        self.updateGui(guiImage)

    def selectCard(self, cardId):
        self.table.selectCard(cardId)
        guiImage = self.table.getGUIImage()
        self.updateGui(guiImage)

    def onClickRules(self):
        messagebox.showinfo("Rules", "Rules clicked")

    def onClickReset(self):
        self.table.resetGame()
        # send_move
        guiImage = self.table.getGUIImage()
        self.updateGui(guiImage)

    def onClickExit(self):
        messagebox.showinfo("Exit", "Exit clicked")

    def optYaniv(self, opt):
        match_finished = self.table.optYaniv(opt)
        print(f"match_finished: {match_finished} and opt: {opt}")
        # send_move
        if match_finished is not None:
            if opt and not match_finished:
                print("entrei")
                self.table.setStatus(self.table.DEFINE_FINISHED_ROUND)
                self.table.resetRound()
                #send_move
        guiImage = self.table.getGUIImage()
        self.updateGui(guiImage)
    
    def startMatch(self):
        status = self.table.getStatus()
        if status == self.table.DEFINE_NO_MATCH:
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
                    self.table.startMatch()
                # send_move
                guiImage = self.table.getGUIImage()
                self.updateGui(guiImage)
        else:
            messagebox.showinfo("Erro ao iniciar partida", "Partida já iniciada")

    def receive_move(self, a_move):
        self.table.receiveMove(a_move)
        guiImage = self.table.getGUIImage()
        self.updateGui(guiImage)
                
    def updateGui(self, guiImage: GUIImage):
        # função lambda para selecionar uma carta
        select_card = lambda x: (lambda p: self.selectCard(x))
        # para cada carta na mão do jogador
        for i, card in enumerate(guiImage.getLocalPlayerCurrentHand()):
            cardLabel = self.player1Cards[i]
            # obtem a imagem correspondente
            cardImage = ImageTk.PhotoImage(Image.open(f"cards/{card.getValue()}{card.getSuit()}.png"))
            # deixa com borda se ta selecionada
            cardLabel.config(image = cardImage, borderwidth = 2 if card.isSelected() else 0, relief="solid")
            cardLabel.photo_ref = cardImage
            cardLabel.bind("<Button-1>", select_card(card.getId()))
        # limpa as "restantes"
        for j in range(6 - len(guiImage.getLocalPlayerCurrentHand())):
            cardLabel = self.player1Cards[-(j + 1)]
            cardLabel.config(image = "", borderwidth = 0)
        
        topOfDiscardDeck = guiImage.getDiscardDeckFirstCard()
        if topOfDiscardDeck is not None:
            cardImage = ImageTk.PhotoImage(Image.open(f"cards/{topOfDiscardDeck.getValue()}{topOfDiscardDeck.getSuit()}.png"))
            self.discardDeck.config(image = cardImage)
            self.discardDeck.photo_ref = cardImage

        isBuyDeckEmpty = guiImage.getBuyDeckEmpty()
        if isBuyDeckEmpty:
            self.buyDeck.config(image = "")

        round = guiImage.getRound()
        self.roundLabel.config(text = f"Round: {round}")

        message = guiImage.getMessage()
        self.messageLabel.config(text = message)

        playersInfo = guiImage.getPlayersInfo()

        i = self.table.getPlayerIndexById(self.table.getLocalPlayerId())

        self.labelPontuacaoPlayer1.config(text = f"Score: {playersInfo[self.table.getLocalPlayerId()].getPoints()}")

        if NUMBER_OF_PLAYERS == 4:
            pontuacao = [self.labelPontuacaoPlayer2, self.labelPontuacaoPlayer3, self.labelPontuacaoPlayer4]
            cards = [self.player2Cards, self.player3Cards, self.player4Cards]
            cards_images = ["backRight", "backUpsideDown", "backLeft"]
        elif NUMBER_OF_PLAYERS == 2:
            pontuacao = [self.labelPontuacaoPlayer2]
            cards = [self.player2Cards]
            cards_images = ["backRight"]

        playersQueue = self.table.getPlayersQueue()
        for j in range(len(pontuacao)):
            playerInfo = playersInfo[playersQueue[(i+j+1) % NUMBER_OF_PLAYERS].getId()]
            pontuacao[j].config(text = f"Score: {playerInfo.getPoints()}")
            for m in range(playerInfo.getNumberOfCards()):
                img = ImageTk.PhotoImage(Image.open(f"cards/{cards_images[j]}.png"))
                cards[j][m].config(image = img)
                cards[j][m].photo_ref = img
            for n in range(6 - playerInfo.getNumberOfCards()):
                cards[j][-(n+1)].config(image = "")
