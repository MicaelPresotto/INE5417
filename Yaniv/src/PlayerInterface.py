import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class PlayerInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Yaniv")
        self.window.geometry("800x600")
        self.window.config(bg="darkgreen")
        self.window.resizable(width=False, height=False)
        self.create_widgets()

    def create_widgets(self):
        self.buttonTake = tk.Button(self.window, text="Take", command=self.onClickTake)
        self.buttonDiscard = tk.Button(self.window, text="Discard", command=self.onClickDiscard)
        self.buttonTake.place(relx=0.6, rely=0.6, relwidth=0.08, relheight=0.08)
        self.buttonDiscard.place(relx=0.3, rely=0.6, relwidth=0.09, relheight=0.08)

        imagem = tk.PhotoImage(file="/home/bridge/Documentos/INE5417/Yaniv/cards/back.png")
        w = tk.Label(self.window, image=imagem, bd=0, bg="darkgreen")
        w.imagem = imagem
        w.place(relx=0.3, rely=0.4)
        
        myCards = ['2C', '3C', '4C', '5C', '6C']

        # bottom
        for i in range(len(myCards)):
            imagem = Image.open(f"/home/bridge/Documentos/INE5417/Yaniv/cards/{myCards[i]}.png")
            imagem = ImageTk.PhotoImage(imagem)
            w = tk.Label(self.window, image=imagem, bd=0, bg="darkgreen")
            w.bind("<Button-1>", lambda event, idx=i: self.onclickCard(myCards[idx]))
            w.imagem = imagem
            w.place(relx=0.3 + i * 0.07, rely=0.8)

        # left
        for i in range(5):
            imagem = Image.open("/home/bridge/Documentos/INE5417/Yaniv/cards/backLeft.png")
            imagem = ImageTk.PhotoImage(imagem)
            w = tk.Label(self.window, image=imagem, bd=0, bg="darkgreen")
            w.imagem = imagem
            w.place(relx=0.02, rely=0.3 + i * 0.07)

        # right
        for i in range(5):
            imagem = Image.open("/home/bridge/Documentos/INE5417/Yaniv/cards/backRight.png")
            imagem = ImageTk.PhotoImage(imagem)
            w = tk.Label(self.window, image=imagem, bd=0, bg="darkgreen")
            w.imagem = imagem
            w.place(relx=0.85, rely=0.3 + i * 0.07)

        # top
        for i in range(5):
            imagem = Image.open("/home/bridge/Documentos/INE5417/Yaniv/cards/backUpsideDown.png")
            imagem = ImageTk.PhotoImage(imagem)
            w = tk.Label(self.window, image=imagem, bd=0, bg="darkgreen")
            w.imagem = imagem
            w.place(relx=0.3 + i * 0.07, rely=0.02)

        framePlayer1 = tk.Frame(self.window, bg="white", bd=1, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        framePlayer1.place(relx=0.7, rely=0.9, relwidth=0.15, relheight=0.07)
        self.labelPlayer1 = tk.Label(framePlayer1, text="Player 1", bg="white", font=("Arial", 8))
        self.labelPlayer1.place(relx=0.33, rely=0.01)
        self.labelPontuacaoPlayer1 = tk.Label(framePlayer1, text="Pontuação: 0", bg="white", font=("Arial", 8))
        self.labelPontuacaoPlayer1.place(relx=0.25, rely=0.5)

        framePlayer2 = tk.Frame(self.window, bg="white", bd=1, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        framePlayer2.place(relx=0.12, rely=0.05, relwidth=0.15, relheight=0.07)
        self.labelPlayer2 = tk.Label(framePlayer2, text="Player 2", bg="white", font=("Arial", 8))
        self.labelPlayer2.place(relx=0.33, rely=0.01)
        self.labelPontuacaoPlayer2 = tk.Label(framePlayer2, text="Pontuação: 0", bg="white", font=("Arial", 8))
        self.labelPontuacaoPlayer2.place(relx=0.25, rely=0.5)

        framePlayer3 = tk.Frame(self.window, bg="white", bd=1, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        framePlayer3.place(relx=0.02, rely=0.72, relwidth=0.15, relheight=0.07)
        self.labelPlayer3 = tk.Label(framePlayer3, text="Player 3", bg="white", font=("Arial", 8))
        self.labelPlayer3.place(relx=0.33, rely=0.01)
        self.labelPontuacaoPlayer3 = tk.Label(framePlayer3, text="Pontuação: 0", bg="white", font=("Arial", 8))
        self.labelPontuacaoPlayer3.place(relx=0.25, rely=0.5)


        framePlayer4 = tk.Frame(self.window, bg="white", bd=1, borderwidth=2, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        framePlayer4.place(relx=0.84, rely=0.2, relwidth=0.15, relheight=0.07)
        self.labelPlayer4 = tk.Label(framePlayer4, text="Player 4", bg="white", font=("Arial", 8))
        self.labelPlayer4.place(relx=0.33, rely=0.01)
        self.labelPontuacaoPlayer4 = tk.Label(framePlayer4, text="Pontuação: 0", bg="white", font=("Arial", 8))
        self.labelPontuacaoPlayer4.place(relx=0.25, rely=0.5)

    def onClickDiscard(self):
        messagebox.showinfo("Discard", "Discard clicked")

    def onClickTake(self):
        messagebox.showinfo("Take", "Take clicked")

    def onclickCard(self, card):
        messagebox.showinfo("Card", f"Card {card} clicked")



def main():
    root = tk.Tk()
    PlayerInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
