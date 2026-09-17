import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

MAX_PLAYERS = 20

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state('zoomed')
        self.title("Player Entry")
        self.configure(bg='gray1')
        self.create_title()
        self.create_teams()
        self.create_players()

    def create_title(self):
        title = tk.Label(self, text="Entry Terminal", fg='gray100',bg='gray1',font=("Arial", 30, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(10,15))

    def create_teams(self):
        self.red_bg = tk.Frame(self, bg="Firebrick1")
        self.green_bg = tk.Frame(self, bg="SpringGreen3")

        self.red_bg.grid(row=1, column=0, padx=20, sticky="n")
        self.green_bg.grid(row=1, column=1, padx=20, sticky="n")

        red_title = tk.Label(self.red_bg, text="RED TEAM", fg='gray100', bg='Firebrick1', font=("Arial", 14, "bold"), width=20)
        green_title = tk.Label(self.green_bg, text="GREEN TEAM", fg='gray100', bg='SpringGreen3', font=("Arial", 14, "bold"), width=20)

        red_title.grid(row=0, column=0, columnspan=3, pady=5)
        green_title.grid(row=0, column=0,columnspan=3,pady=5)
        
        
#window.columnconfigure(0, weight=1)

    def create_players(self):
        for i in range(MAX_PLAYERS):
            label = tk.Label(self.red_bg, text=i, fg='gray100',bg='Firebrick1', font=("Arial", 10))
            label.grid(row=i+1, column=0, sticky="w", pady=5)

        for i in range(MAX_PLAYERS):
            label = tk.Label(self.green_bg, text=i, fg='gray100',bg='SpringGreen3', font=("Arial", 10))
            label.grid(row=i+1, column=0, sticky="w", pady=5)

    
window = Window()
window.mainloop()