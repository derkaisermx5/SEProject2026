import tkinter as tk
# not sure if order matters when importing is calling a seperate file's function
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk

from udp_network import UDPNetwork, local_network_choices, validate_network

from database import get_codename, add_player
 
MAX_PLAYERS = 20
 
class Window(tk.Frame):
    def __init__(self, master, udp=None):
        super().__init__(master)
        master.title("Player Entry")
        self.configure(bg='gray1')
        self.udp = udp if udp is not None else UDPNetwork()  # UDP sockets (broadcast 7500 / receive 7501)
        self.red_team = []
        self.green_team = []
        self.equipment_ids = {}  # (team, slot) -> equipment id
        self.edit_mode = False
        self.create_title()
        self.create_fkeys()
        self.create_teams()
        self.create_players()
        self.create_status_bar()
 
        master.bind_all("<Control-q>", lambda e: self.print_players())  # hotkey to print the players on each team to console
        master.bind_all("<F1>", self.edit_game)  # hotkey to edit the players in the game
        master.bind_all("<F2>", self.change_network)  # hotkey to pick a different network for the UDP sockets
 
    def create_title(self):
        title = tk.Label(self, text="Entry Terminal", fg='gray100', bg='gray1', font=("Arial", 30, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(10, 15))
 
    def create_teams(self):  # creates the titles and text for both teams
        self.red_bg = tk.Frame(self, bg="Firebrick1")
        self.green_bg = tk.Frame(self, bg="SpringGreen3")
 
        self.red_bg.grid(row=1, column=0, padx=20, sticky="n")
        self.green_bg.grid(row=1, column=1, padx=20, sticky="n")
 
        red_title = tk.Label(self.red_bg, text="RED TEAM", fg='gray100', bg='Firebrick1', font=("Arial", 14, "bold"), width=20)
        green_title = tk.Label(self.green_bg, text="GREEN TEAM", fg='gray100', bg='SpringGreen3', font=("Arial", 14, "bold"), width=20)
 
        red_title.grid(row=0, column=0, columnspan=3, pady=5)
        green_title.grid(row=0, column=0, columnspan=3, pady=5)
 
    def create_players(self):  # adds labels and entries for each team so player can input their player name
        for i in range(MAX_PLAYERS):
            label = tk.Label(self.red_bg, text=i, fg='gray100', bg='Firebrick1', font=("Arial", 10))
            label.grid(row=i+1, column=0, sticky="w", pady=5)
            entry1 = tk.Entry(self.red_bg, font=("Arial", 10), state="disabled")
            entry1.grid(row=i+1, column=1, sticky="w")
            entry1.bind("<Return>", lambda e, slot=i: self.player_entered("red", slot))
            self.red_team.append(entry1)
 
        for i in range(MAX_PLAYERS):
            label = tk.Label(self.green_bg, text=i, fg='gray100', bg='SpringGreen3', font=("Arial", 10))
            label.grid(row=i+1, column=0, sticky="w", pady=5)
            entry1 = tk.Entry(self.green_bg, font=("Arial", 10), state="disabled")
            entry1.grid(row=i+1, column=1, sticky="w")
            entry1.bind("<Return>", lambda e, slot=i: self.player_entered("green", slot))
            self.green_team.append(entry1)
 
    def create_fkeys(self):  # adds the square boxes outlining what the f-keys do
        key_frame = tk.Frame(self, bg='gray1')
        key_frame.grid(row=1, column=2, padx=20, sticky="n")
 
        f1_box = tk.Frame(key_frame, bg='gray1', highlightbackground='gray50', highlightthickness=2, width=120, height=70)
        f1_box.grid(row=0, column=0, pady=3)
        f1_label = tk.Label(f1_box, text="F1\nEdit Game", fg='lime', bg='gray1', font=("Arial", 10, "bold"))
        f1_label.pack()
        for w in (f1_box, f1_label):  # boxes are clickable too (Mac F-keys need fn)
            w.bind("<Button-1>", self.edit_game)

        f2_box = tk.Frame(key_frame, bg='gray1', highlightbackground='gray50', highlightthickness=2, width=120, height=70)
        f2_box.grid(row=1, column=0, pady=3)
        f2_label = tk.Label(f2_box, text="F2\nChange Network", fg='lime', bg='gray1', font=("Arial", 10, "bold"))
        f2_label.pack()
        for w in (f2_box, f2_label):
            w.bind("<Button-1>", self.change_network)

        self.network_label = tk.Label(key_frame, text="", fg='gray100', bg='gray1', font=("Arial", 10), justify="center")
        self.network_label.grid(row=2, column=0, pady=(10, 3))
        self.update_network_label()

    def create_status_bar(self):  # one line under the teams showing the last UDP action
        self.status_label = tk.Label(self, text="Press F1, then Enter in a slot to look up/add player by ID.",
                                     fg='gray70', bg='gray1', font=("Arial", 10))
        self.status_label.grid(row=2, column=0, columnspan=3, pady=(10, 5))

    def set_status(self, text, color='gray70'):
        self.status_label.config(text=text, fg=color)

    def update_network_label(self):
        self.network_label.config(text=f"UDP network:\n{self.udp.network}")

    # ---------------- UDP: equipment codes ----------------
    def player_entered(self, team, slot):  # Enter pressed in a player's name box
        if not self.edit_mode:
            return
        entries = self.red_team if team == "red" else self.green_team

        # 1st - ask user for the database player ID
        player_id = simpledialog.askinteger(
            "Player ID", "Enter the player ID:", parent=self
        )
        if player_id is None:
            return

        # 2nd - Here its about look up/inserting in PostgreSQL
        try:
            name = get_codename(player_id)
            if name is None:
                name = simpledialog.askstring(
                    "New Player",
                    f"No player with ID {player_id}. Enter a codename:",
                    parent=self,
                )
                if not name or not name.strip():
                    return
                name = name.strip()
                add_player(player_id, name)
                self.set_status(f"Saved new player {player_id} ({name}) to database", "green")
            else:
                self.set_status(f"Found player {player_id} ({name}) in database", "green")
        except Exception as e:
            self.set_status(f"Database error: {e}", "Firebrick1")
            return

        # 3rd - here i have to put codename in the entry box
        entries[slot].delete(0, "end")
        entries[slot].insert(0, name)

        # 4th - small adjustment to the UDP previously updated
        equipment_id = simpledialog.askinteger("Equipment ID", f"Enter the equipment ID for {name}:", parent=self)
        if equipment_id is None:  # cancelled
            return
        self.player_added(team, slot, name, equipment_id)
        

    def player_added(self, team, slot, name, equipment_id):
        """Call this every time a player is added to a team.
        It broadcasts the player's equipment code over UDP (port 7500)."""
        self.equipment_ids[(team, slot)] = equipment_id
        try:
            self.udp.broadcast_equipment_id(equipment_id)
        except OSError as e:
            self.set_status(f"Could not broadcast equipment ID {equipment_id}: {e}", 'Firebrick1')
            return
        self.set_status(f"Added {name} ({team} team) - broadcast equipment ID {equipment_id} to {self.udp.network}:7500", 'lime')

    # ---------------- UDP: network selection ----------------
    def change_network(self, event=None):  # F2: pick a different network for the UDP sockets
        NetworkDialog(self, self.udp, on_changed=self.network_changed)

    def network_changed(self, address):
        self.update_network_label()
        self.set_status(f"UDP network changed to {address}", 'lime')
 
    def edit_game(self, event=None):  # method to add and edit the players in the game
        if self.edit_mode == False:
            self.edit_mode = True
 
            for entry in self.red_team:
                entry.config(state="normal")
 
            for entry in self.green_team:
                entry.config(state="normal")
 
            print("Edit mode enabled")
 
        else:
            self.edit_mode = False
 
            for entry in self.red_team:
                entry.config(state="disabled")
 
            for entry in self.green_team:
                entry.config(state="disabled")
 
            print("Edit mode disabled")
 
    def print_players(self):  # print players on each team
        for entry in self.red_team:
            print(entry.get())
 
        for entry in self.green_team:
            print(entry.get())
 
 
class NetworkDialog(tk.Toplevel):  # small popup to choose the network address for the UDP sockets
    def __init__(self, master, udp, on_changed=None):
        super().__init__(master)
        self.udp = udp
        self.on_changed = on_changed
        self.title("Select Network")
        self.configure(bg='gray1', padx=20, pady=15)
        self.resizable(False, False)
        self.transient(master.winfo_toplevel())

        tk.Label(self, text="Network address for UDP sockets", fg='gray100', bg='gray1',
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 8))
        tk.Label(self, text=f"Current: {udp.network}", fg='gray70', bg='gray1',
                 font=("Arial", 10)).grid(row=1, column=0, columnspan=2, pady=(0, 8))

        self.choice = tk.StringVar(value=udp.network)
        choices = local_network_choices()
        if udp.network not in choices:
            choices.insert(0, udp.network)
        combo = ttk.Combobox(self, textvariable=self.choice, values=choices, width=22)
        combo.grid(row=2, column=0, columnspan=2, pady=(0, 4))
        combo.focus_set()
        combo.selection_range(0, "end")

        tk.Label(self, text="Pick one or type any IPv4 address (default 127.0.0.1)", fg='gray70', bg='gray1',
                 font=("Arial", 9)).grid(row=3, column=0, columnspan=2, pady=(0, 6))
        self.error_label = tk.Label(self, text="", fg='Firebrick1', bg='gray1', font=("Arial", 9))
        self.error_label.grid(row=4, column=0, columnspan=2)

        tk.Button(self, text="Apply", width=10, command=self.apply).grid(row=5, column=0, padx=5, pady=(6, 0))
        tk.Button(self, text="Cancel", width=10, command=self.destroy).grid(row=5, column=1, padx=5, pady=(6, 0))
        self.bind("<Return>", lambda e: self.apply())
        self.bind("<Escape>", lambda e: self.destroy())

        # make sure the popup shows up centered and on top of the full-screen window
        self.update_idletasks()
        top = master.winfo_toplevel()
        x = top.winfo_rootx() + (top.winfo_width() - self.winfo_reqwidth()) // 2
        y = top.winfo_rooty() + (top.winfo_height() - self.winfo_reqheight()) // 3
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        self.attributes("-topmost", True)
        self.lift()
        self.focus_force()
        combo.focus_set()
        self.after(10, self.grab_set)

    def apply(self):
        try:
            address = self.udp.set_network(validate_network(self.choice.get()))
        except ValueError:
            self.error_label.config(text=f"'{self.choice.get()}' is not a valid IPv4 address")
            return
        except OSError as e:
            self.error_label.config(text=f"Could not open sockets: {e}")
            return
        if self.on_changed:
            self.on_changed(address)
        self.destroy()


# Lets you run just this file on its own to test the screen, without going
# through main.py or the splash.
if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    app = Window(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
    app.udp.close()
 