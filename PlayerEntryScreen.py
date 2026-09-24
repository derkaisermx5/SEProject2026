import tkinter as tk
import keyboard
from tkinter import ttk
from PIL import Image, ImageTk

MAX_PLAYERS = 20

class Window(tk.Tk): #initializes the window for the entry screen, sets arrays for each team to store players
    def __init__(self):
        super().__init__()
        self.state('normal')
        self.title("Player Entry")
        self.configure(bg='gray1')
        self.red_team = []
        self.green_team = []
        self.create_title()
        self.create_fkeys()
        self.create_teams()
        self.create_players()
        
        keyboard.add_hotkey('ctrl + q', self.print_players) #hotkey to print the players on each team to console
        

    def create_title(self):
        title = tk.Label(self, text="Entry Terminal", fg='gray100',bg='gray1',font=("Arial", 30, "bold")) #creates the "entry terminal" texr
        title.grid(row=0, column=0, columnspan=3, pady=(10,15))

    def create_teams(self): #creates the titles and text for both teams
        self.red_bg = tk.Frame(self, bg="Firebrick1")
        self.green_bg = tk.Frame(self, bg="SpringGreen3")

        self.red_bg.grid(row=1, column=0, padx=20, sticky="n")
        self.green_bg.grid(row=1, column=1, padx=20, sticky="n")

        red_title = tk.Label(self.red_bg, text="RED TEAM", fg='gray100', bg='Firebrick1', font=("Arial", 14, "bold"), width=20)
        green_title = tk.Label(self.green_bg, text="GREEN TEAM", fg='gray100', bg='SpringGreen3', font=("Arial", 14, "bold"), width=20)

        red_title.grid(row=0, column=0, columnspan=3, pady=5)
        green_title.grid(row=0, column=0,columnspan=3,pady=5)
           
#window.columnconfigure(0, weight=1)

    def create_players(self): #adds labels and entries for each team so player can input their player name
        for i in range(MAX_PLAYERS):
            label = tk.Label(self.red_bg, text=i, fg='gray100',bg='Firebrick1', font=("Arial", 10))
            label.grid(row=i+1, column=0, sticky="w", pady=5)
            entry1 = tk.Entry(self.red_bg, font=("Arial", 10))
            entry1.grid(row=i+1, column=1, sticky="w")
            self.red_team.append(entry1)
            print(self.red_team[0].get())
           

        for i in range(MAX_PLAYERS):
            label = tk.Label(self.green_bg, text=i, fg='gray100',bg='SpringGreen3', font=("Arial", 10))
            label.grid(row=i+1, column=0, sticky="w", pady=5)
            entry1 = tk.Entry(self.green_bg, font=("Arial", 10))
            entry1.grid(row=i+1, column=1, sticky="w")
            self.green_team.append(entry1)

    def create_fkeys(self):
        key_frame = tk.Frame(self, bg='gray1')
        key_frame.grid(row=1, column=2, padx=20, sticky="n")
        
        f1_box = tk.Frame(key_frame, bg='gray1', highlightbackground='gray50', highlightthickness=2, width=120, height=70)
        f1_box.grid(row=0, column=0, pady=3)
        f1_label =tk.Label(f1_box, text="F1\nEdit Game", fg='lime',bg='gray1',font=("Arial", 10, "bold"))
        f1_label.pack()

    def print_players(self): #print players on each team
        for entry in self.red_team:
            print(entry.get())
            
        for entry in self.green_team:
            print(entry.get())
    
window = Window() #loop to keep window open
window.mainloop()