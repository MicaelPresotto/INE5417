import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class PlayerInterface:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.mainWindow.title("Yaniv")
        self.mainWindow.geometry("800x600")
        self.mainWindow.config(bg="darkgreen")
        self.mainWindow.resizable(width=False, height=False)
        self.create_widgets()
        self.createMenu()

    def create_widgets(self):
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
            command=self.onClickDiscard,
            width=10,
            height=2,
            bg="white",
        )
        self.discardButton.place(relx=0.44, rely=0.6)

        self.callYanivButton = tk.Button(
            self.mainWindow,
            text="Call yaniv",
            command=self.onClickCallYaniv,
            width=10,
            height=2,
            bg="white",
        )

        self.callYanivButton.place(relx=0.3, rely=0.7)

        self.dontCallYanivButton = tk.Button(
            self.mainWindow,
            text="Don't call yaniv",
            command=self.onClickDontCallYaniv,
            width=12,
            height=2,
            bg="white",
        )
        self.dontCallYanivButton.place(relx=0.58, rely=0.7)

        imageBuyDeck= tk.PhotoImage(file="cards/back.png")
        buyDeck = tk.Label(self.mainWindow, image=imageBuyDeck, bd=0, bg="darkgreen")
        buyDeck.imagem = imageBuyDeck
        buyDeck.place(relx=0.3, rely=0.4)
        buyDeck.bind("<Button-1>", lambda event: self.onClickBuy())

        imageDiscardDeck= tk.PhotoImage(file="cards/7C.png")
        discardDeck= tk.Label(
            self.mainWindow, image=imageDiscardDeck, bd=0, bg="darkgreen"
        )
        discardDeck.imagem = imageDiscardDeck
        discardDeck.place(relx=0.58, rely=0.4)
        discardDeck.bind("<Button-1>", lambda event: self.onClickDiscardDeck())

        self.roundLabel = tk.Label(
            self.mainWindow,
            text="Round: X",
            bg="darkgreen",
            font=("Arial", 15),
            fg="white",
        )

        self.roundLabel.place(relx=0.85, rely=0.02)

        myCards = ["2C", "3C", "4C", "5C", "6C"]

        # bottom
        for i in range(len(myCards)):
            cardImage = Image.open(f"cards/{myCards[i]}.png")
            cardImage = ImageTk.PhotoImage(cardImage)
            w = tk.Label(self.mainWindow, image=cardImage, bd=0, bg="darkgreen")
            w.bind("<Button-1>", lambda event, idx=i: self.onClickCard(myCards[idx]))
            w.image = cardImage
            w.place(relx=0.3 + i * 0.07, rely=0.8)

        # left
        for i in range(5):
            cardImage = Image.open("cards/backLeft.png")
            cardImage = ImageTk.PhotoImage(cardImage)
            w = tk.Label(self.mainWindow, image=cardImage, bd=0, bg="darkgreen")
            w.image = cardImage
            w.place(relx=0.02, rely=0.3 + i * 0.07)

        # right
        for i in range(5):
            cardImage = Image.open("cards/backRight.png")
            cardImage = ImageTk.PhotoImage(cardImage)
            w = tk.Label(self.mainWindow, image=cardImage, bd=0, bg="darkgreen")
            w.image = cardImage
            w.place(relx=0.85, rely=0.3 + i * 0.07)

        # top
        for i in range(5):
            cardImage = Image.open("cards/backUpsideDown.png")
            cardImage = ImageTk.PhotoImage(cardImage)
            w = tk.Label(self.mainWindow, image=cardImage, bd=0, bg="darkgreen")
            w.image = cardImage
            w.place(relx=0.3 + i * 0.07, rely=0.02)

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
        self.labelScorePlayer3 = tk.Label(
            frameScorePlayer3, text="Score: 0", bg="white", font=("Arial", 8)
        )
        self.labelScorePlayer3.place(relx=0.32, rely=0.5)

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
        self.labelScorePlayer4 = tk.Label(
            frameScorePlayer4, text="Score: 0", bg="white", font=("Arial", 8)
        )
        self.labelScorePlayer4.place(relx=0.32, rely=0.5)

    def createMenu(self):
        self.menu = tk.Menu(self.mainWindow)
        self.menu.option_add("*tearOff", False)
        self.mainWindow["menu"] = self.menu

        self.menuFile = tk.Menu(self.menu, bg="white", fg="black")
        self.menu.add_cascade(menu=self.menuFile, label="Menu")

        self.menuFile.add_command(label="Rules", command=self.onClickRules)
        self.menuFile.add_command(label="Start game", command=self.onClickStart)
        self.menuFile.add_command(label="Reset game", command=self.onClickReset)
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Exit", command=self.onClickExit)

    def onClickBuy(self):
        messagebox.showinfo("Buy Deck", "Buy deck clicked")

    def onClickDiscard(self):
        messagebox.showinfo("Discard", "Discard clicked")

    def onClickDiscardDeck(self):
        messagebox.showinfo("Discard Deck", "Discard deck clicked")

    def onClickCard(self, card):
        messagebox.showinfo("Card", f"Card {card} clicked")

    def onClickTake(self):
        messagebox.showinfo("Take", "Take clicked")

    def onClickRules(self):
        messagebox.showinfo("Rules", "Rules clicked")

    def onClickStart(self):
        messagebox.showinfo("Start", "Start clicked")

    def onClickReset(self):
        messagebox.showinfo("Reset", "Reset clicked")

    def onClickExit(self):
        messagebox.showinfo("Exit", "Exit clicked")

    def onClickCallYaniv(self):
        messagebox.showinfo("Call yaniv", "Call yaniv clicked")

    def onClickDontCallYaniv(self):
        messagebox.showinfo("Call yaniv", "Call yaniv clicked")


def main():
    root = tk.Tk()
    PlayerInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()