import tkinter as tk
from screeninfo import get_monitors

from Splash import SplashScreen
from PlayerEntryScreen import Window
from Screen_utils import fit_current_screen


def launch_main_screen():
    fit_current_screen(root)
    app = Window(root)
    app.pack(fill="both", expand=True)

root = tk.Tk()
root.withdraw()

SplashScreen(root, on_done=lambda: [root.deiconify(), launch_main_screen()])

root.mainloop()



