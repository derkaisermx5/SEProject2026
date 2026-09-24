import tkinter as tk
from screeninfo import get_monitors

from Splash import SplashScreen
from PlayerEntryScreen import Window
from Screen_utils import fit_current_screen


def launch_main_screen():
    fit_current_screen(root)
    root.configure(bg="gray1")
    app = Window(root)
    app.place(relx=0.5, rely=0.5, anchor="center")

root = tk.Tk()
root.withdraw()

SplashScreen(root, on_done=lambda: [root.deiconify(), launch_main_screen()])

root.mainloop()



