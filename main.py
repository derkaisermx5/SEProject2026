import os
import sys

# Debian blocks pip installs on the system Python, so Install.py puts the packages in ./venv.
# If that venv exists and we were not started from it, restart this program using it.
_venv_python = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "bin", "python")
if sys.prefix == sys.base_prefix and os.path.exists(_venv_python):
    os.execv(_venv_python, [_venv_python] + sys.argv)
import argparse
import tkinter as tk
from screeninfo import get_monitors

from Splash import SplashScreen
from PlayerEntryScreen import Window
from PlayActionScreen import PlayActionScreen
from Screen_utils import fit_current_screen
from udp_network import UDPNetwork, DEFAULT_NETWORK

# Optional: pick the UDP network at launch, e.g.  python main.py --network 192.168.1.20
# (it can also be changed while the app is running with F2)
parser = argparse.ArgumentParser(description="Laser tag game")
parser.add_argument("--network", default=DEFAULT_NETWORK,
                    help=f"IPv4 address for the UDP sockets (default {DEFAULT_NETWORK})")
args = parser.parse_args()

udp = UDPNetwork(args.network)  # broadcast on 7500, receive on 7501


entry_screen = None
play_screen = None


def launch_main_screen():
    global entry_screen
    fit_current_screen(root)
    root.configure(bg="gray1")
    entry_screen = Window(root, udp, on_start=start_game)
    entry_screen.place(relx=0.5, rely=0.5, anchor="center")


def start_game(red_players, green_players):  # F5 on the entry screen
    global play_screen
    entry_screen.place_forget()  # hide the entry screen (kept so we can come back later)
    play_screen = PlayActionScreen(root, red_players, green_players, udp)
    play_screen.pack(fill="both", expand=True)
    play_screen.start_game()


def on_close():
    udp.close()
    root.destroy()


root = tk.Tk()
root.withdraw()
root.protocol("WM_DELETE_WINDOW", on_close)

SplashScreen(root, on_done=lambda: [root.deiconify(), launch_main_screen()])

root.mainloop()
