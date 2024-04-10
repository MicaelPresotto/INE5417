import tkinter as tk
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
        self.buttonTake = tk.Button(self.window, text="Take")
        self.buttonDiscard = tk.Button(self.window, text="Discard")
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



def main():
    root = tk.Tk()
    app = PlayerInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
