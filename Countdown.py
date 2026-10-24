import math
import os
import time
import tkinter as tk
from PIL import Image, ImageTk

COUNTDOWN_SECONDS = 30
ZERO_HOLD_MS = 1000 

# The image file sits next to this file 
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

def missing_images(seconds, image_dir):
    names = [f"countdown{n}.jpg" for n in range(seconds, -1, -1)]
    return [name for name in names if not os.path.exists(os.path.join(image_dir, name))]


class CountdownScreen(tk.Frame):
    def __init__(self, master, seconds = COUNTDOWN_SECONDS, on_done=None, image_dir=IMAGE_DIR, zero_hold_ms=ZERO_HOLD_MS):
        # This checks the pictures first
        missing = missing_images(seconds, image_dir)
        if missing:
            shown = ", ".join(missing[:5]) + (f" and {len(missing) - 5} more" if len(missing) > 5 else "")
            raise FileNotFoundError(f"Picture missing from {image_dir}: {shown}")

        super().__init__(master, bg="gray1") 
        self.seconds = seconds
        self.on_done = on_done 
        self.image_dir = image_dir
        self.zero_hold_ms = zero_hold_ms
        self._after_id = None
        self._shown = None
        self._photo_cache = {}

        # this covers the whole window 
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.lift()
    
        self.image_label = tk.Label(self, bg="gray1", borderwidth=0)
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # this accomadates for when the user changes the window size 
        self.bind("<Configure>", self._resize)
        self.update_idletasks()

        #Counts against the clock 
        self._end_time = time.monotonic() + seconds
        self._tick()


    # Drawing the images 
    def _get_image(self, number, width, height):
        key = (number, width, height)
        if key not in self._photo_cache:
            img = Image.open(os.path.join(self.image_dir, f"countdown{number}.jpg"))
            scale  = min(width / img.width, height / img.height) # keeps the proportions
            size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
            self._photo_cache[key] = ImageTk.PhotoImage(img.resize(size, Image.LANCZOS))
        return self._photo_cache[key]

    def _show(self, number):
        self._shown = number
        width, height = self.winfo_width(), self.winfo_height()
        if width <= 1 or height <= 1: 
            return
        photo = self._get_image(number, width, height)
        self.image_label.config(image=photo)
        self.image_label.image = photo 


    def _resize(self, event):
        self._photo_cache.clear() 
        if self._shown is not None:
            self._show(self._shown)


    # Getting the timing right
    def _tick(self):
        self._after_id = None
        remaining = math.ceil(self._end_time - time.monotonic())
        if remaining <= 0:
            self._show(0)   # countdown reaches 0 
            self._after_id = self.after(self.zero_hold_ms, self.finish)
            return 
        if remaining != self._shown:
            self._show(remaining)
        self._after_id = self.after(100, self._tick)


    def cancel(self):
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None 


    def finish(self):
        self.cancel()
        self.destroy()
        if self.on_done:
            self.on_done()

    def destroy(self):
        self.cancel()
        super().destroy()

# This is to test the file by itself to test the countdown 
if __name__ == "__main__":
    from Screen_utils import fit_current_screen

    root = tk.Tk()
    root.title("Countdown Screen")
    root.configure(bg = "gray1")
    fit_current_screen(root)

    def done():
        print("Countdown finished ")
        root.destroy()

    CountdownScreen(root, on_done=done)
    root.mainloop()
 