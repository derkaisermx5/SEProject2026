#Martin Almaraz
#Software Engineering CSCE 35103-001 Fall 2026
# August 8, 2026

import tkinter as tk
from PIL import Image, ImageTk 

from Screen_utils import get_current_monitor 
# use the tkinker to make the splash screen 
# make it be 3 seconds with the milliseconds thing 
# close out of it and make the program continue
# image appears too big on the screen i need to find a way so it can fit into the entire screen used 


class SplashScreen(tk.Toplevel):
    def __init__(self, master, image_path="images/logo.jpg", duration_ms=3000,on_done=None):
        super().__init__(master)
        self.on_done = on_done

        monitor = get_current_monitor(master)
        self.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")

        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((monitor.width, monitor.height))

        self.tk_image = ImageTk.PhotoImage(pil_image)     # stored in self not locally

        label = tk.Label(self, image=self.tk_image)
        label.pack(fill="both", expand=True)

        self.after(duration_ms, self.finish)

    def finish(self):
        self.destroy()
        if self.on_done:
            self.on_done()


    