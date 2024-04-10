import tkinter as tk
import sys
from PlayerInterface import PlayerInterface

class YanivInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Main menu")
        self.window.geometry("800x600")
        self.window.config(bg="purple")
        self.window.resizable(width=True, height=True)
        self.create_widgets()

    def create_widgets(self):
        self.buttonPlay = tk.Button(self.window, text="Play", command=self.open_player_interface)
        self.buttonExit = tk.Button(self.window, text="Exit", command=sys.exit)
        self.buttonPlay.place(relx=0.4, rely=0.5, relwidth=0.08, relheight=0.08)
        self.buttonExit.place(relx=0.5, rely=0.5, relwidth=0.08, relheight=0.08)

        self.labelYaniv = tk.Label(self.window, text="Yaniv", bg="purple", fg="white", font=("Arial", 24))
        self.labelPlayers = tk.Label(self.window, text="Players: 1/4", bg="purple", fg="white", font=("Arial", 24))
        self.labelYaniv.place(relx=0.45, rely=0.1)
        self.labelPlayers.place(relx=0.45, rely=0.3)

    def open_player_interface(self):
        self.window.destroy()
        window = tk.Tk()
        PlayerInterface(window)
    
        
        
window = tk.Tk()
app = YanivInterface(window)
window.mainloop()
