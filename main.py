import argparse
import tkinter as tk
from screeninfo import get_monitors

from Splash import SplashScreen
from PlayerEntryScreen import Window
from Screen_utils import fit_current_screen
from udp_network import UDPNetwork, DEFAULT_NETWORK

# Optional: pick the UDP network at launch, e.g.  python main.py --network 192.168.1.20
# (it can also be changed while the app is running with F2)
parser = argparse.ArgumentParser(description="Laser tag game")
parser.add_argument("--network", default=DEFAULT_NETWORK,
                    help=f"IPv4 address for the UDP sockets (default {DEFAULT_NETWORK})")
args = parser.parse_args()

udp = UDPNetwork(args.network)  # broadcast on 7500, receive on 7501


def launch_main_screen():
    fit_current_screen(root)
    root.configure(bg="gray1")
    app = Window(root, udp)
    app.place(relx=0.5, rely=0.5, anchor="center")


def on_close():
    udp.close()
    root.destroy()


root = tk.Tk()
root.withdraw()
root.protocol("WM_DELETE_WINDOW", on_close)

SplashScreen(root, on_done=lambda: [root.deiconify(), launch_main_screen()])

root.mainloop()
