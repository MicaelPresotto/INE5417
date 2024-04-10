import tkinter as tk
from PIL import Image, ImageTk

class PlayerInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Yaniv")
        self.window.geometry("800x600")
        self.window.config(bg="darkgreen")
        self.window.resizable(width=True, height=True)
        self.create_widgets()

    def create_widgets(self):
        self.buttonTake = tk.Button(self.window, text="Take")
        self.buttonDiscard = tk.Button(self.window, text="Discard")
        self.buttonTake.place(relx=0.4, rely=0.5, relwidth=0.05, relheight=0.05)
        self.buttonDiscard.place(relx=0.2, rely=0.5, relwidth=0.05, relheight=0.05)

        imagem = tk.PhotoImage(file="/home/bridge/Área de Trabalho/Yaniv/images/discardMount.svg")
        w = tk.Label(self.window, image=imagem, width=100, height=100)
        w.imagem = imagem
        w.pack()

def main():
    root = tk.Tk()
    app = PlayerInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
