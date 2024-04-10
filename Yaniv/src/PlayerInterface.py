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
        self.buttonTake.place(relx=0.6, rely=0.5, relwidth=0.08, relheight=0.08)
        self.buttonDiscard.place(relx=0.3, rely=0.5, relwidth=0.09, relheight=0.08)
        
        cards = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC']

        imagem = tk.PhotoImage(file="/home/bridge/Documentos/INE5417/Yaniv/cards/back.png")
        w = tk.Label(self.window, image=imagem, bd=0, bg="darkgreen")
        w.imagem = imagem
        w.place(relx=0.3, rely=0.3)

def main():
    root = tk.Tk()
    app = PlayerInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
