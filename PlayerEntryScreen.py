import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

MAX_PLAYERS = 20

window = tk.Tk()
window.state('zoomed')
window.title("Player Entry")
window.configure(bg='gray1')

#window.columnconfigure(0, weight=1)
title = tk.Label(window, text="Entry Terminal", fg='gray100',bg='gray1',font=("Arial", 30, "bold"))
title.grid(row=0, column=0, columnspan=2, pady=(10,15))

red_bg = tk.Frame(window, bg="Firebrick1")
green_bg = tk.Frame(window, bg="SpringGreen3")

red_bg.grid(row=1, column=0, padx=20, sticky="n")
green_bg.grid(row=1, column=1, padx=20, sticky="n")

red_title = tk.Label(red_bg, text="RED TEAM", fg='gray100', bg='Firebrick1', font=("Arial", 14, "bold"), width=20)
green_title = tk.Label(green_bg, text="GREEN TEAM", fg='gray100', bg='SpringGreen3', font=("Arial", 14, "bold"), width=20)

red_title.grid(row=0, column=0, columnspan=3, pady=5)
green_title.grid(row=0, column=0,columnspan=3,pady=5)
for i in range(MAX_PLAYERS):
    label = tk.Label(window, text=i, fg='gray100',bg='gray1', font=("Arial", 10))
    label.grid(row=i+1, column=0, sticky="w", pady=12)
    
window.mainloop()
