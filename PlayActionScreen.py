# Play action display.
#
# Shown after F5 is pressed on the player entry screen. It has the three areas
# from the project requirements:
#   1. Team windows (red / green) with every player's codename and score,
#      plus the cumulative team score.
#   2. "Current Game Action" window for play-by-play events (empty for now -
#      events come in a later sprint; use add_event() to post one).
#   3. Time remaining.

import tkinter as tk

GAME_LENGTH_SECONDS = 6 * 60

RED = "Firebrick1"
GREEN = "SpringGreen3"
BG = "gray1"
PANEL_BG = "gray8"


class PlayActionScreen(tk.Frame):
    def __init__(self, master, red_players, green_players, udp=None):
        """
        red_players / green_players -- lists of dicts like
            {"codename": "Opus", "equipment_id": 12}
        udp -- the UDPNetwork used by the rest of the app (optional)
        """
        super().__init__(master, bg=BG)
        master.title("Play Action")
        self.udp = udp
        self.game_running = False

        # every player starts the game with 0 points
        self.teams = {
            "red": [dict(p, score=0) for p in red_players],
            "green": [dict(p, score=0) for p in green_players],
        }
        self.team_frames = {}
        self.team_total_labels = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)   # team windows
        self.rowconfigure(3, weight=2)   # game action window

        self.create_title()
        self.create_team_windows()
        self.create_action_window()
        self.create_timer()

        self.refresh_teams()
        self.set_time_remaining(GAME_LENGTH_SECONDS)

    # ---------------- layout ----------------
    def create_title(self):
        tk.Label(self, text="Current Scores", fg="cyan", bg=BG,
                 font=("Arial", 24, "bold")).grid(row=0, column=0, pady=(10, 5))

    def create_team_windows(self):
        holder = tk.Frame(self, bg=BG)
        holder.grid(row=1, column=0, sticky="nsew", padx=20)
        holder.columnconfigure(0, weight=1, uniform="teams")
        holder.columnconfigure(1, weight=1, uniform="teams")
        holder.rowconfigure(0, weight=1)

        for col, (team, title, color) in enumerate((("red", "RED TEAM", RED), ("green", "GREEN TEAM", GREEN))):
            panel = tk.Frame(holder, bg=PANEL_BG, highlightbackground=color, highlightthickness=3)
            panel.grid(row=0, column=col, sticky="nsew", padx=10)
            panel.columnconfigure(0, weight=1)
            panel.rowconfigure(1, weight=1)

            tk.Label(panel, text=title, fg="gray100", bg=color,
                     font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="ew")

            players_frame = tk.Frame(panel, bg=PANEL_BG)   # filled in by refresh_teams()
            players_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
            players_frame.columnconfigure(0, weight=1)
            self.team_frames[team] = players_frame

            total = tk.Label(panel, text="", fg=color, bg=PANEL_BG, font=("Arial", 16, "bold"), anchor="e")
            total.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 8))
            self.team_total_labels[team] = total

    def create_action_window(self):
        tk.Label(self, text="Current Game Action", fg="cyan", bg=BG,
                 font=("Arial", 16, "bold")).grid(row=2, column=0, pady=(12, 4))

        box = tk.Frame(self, bg=PANEL_BG, highlightbackground="gray50", highlightthickness=2)
        box.grid(row=3, column=0, sticky="nsew", padx=30)
        box.columnconfigure(0, weight=1)
        box.rowconfigure(0, weight=1)

        self.action_text = tk.Text(box, height=6, bg=PANEL_BG, fg="gray100", font=("Arial", 12),
                                   relief="flat", state="disabled", wrap="word")
        self.action_text.grid(row=0, column=0, sticky="nsew", padx=8, pady=6)
        scroll = tk.Scrollbar(box, command=self.action_text.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.action_text.config(yscrollcommand=scroll.set)

    def create_timer(self):
        self.timer_label = tk.Label(self, text="", fg="gray100", bg=BG, font=("Arial", 20, "bold"))
        self.timer_label.grid(row=4, column=0, pady=(10, 15))

    # ---------------- updating ----------------
    def refresh_teams(self):
        """Redraw both team windows, players sorted from highest to lowest score."""
        for team, players in self.teams.items():
            frame = self.team_frames[team]
            for widget in frame.winfo_children():
                widget.destroy()

            ranked = sorted(players, key=lambda p: p["score"], reverse=True)
            size = 13 if len(ranked) <= 12 else 11   # smaller rows so a full team still fits
            for row, player in enumerate(ranked):
                tk.Label(frame, text=player["codename"], fg="gray100", bg=PANEL_BG,
                         font=("Arial", size), anchor="w", pady=0).grid(row=row, column=0, sticky="ew")
                tk.Label(frame, text=str(player["score"]), fg="gray100", bg=PANEL_BG,
                         font=("Arial", size), anchor="e", pady=0).grid(row=row, column=1, sticky="e")
            if not ranked:
                tk.Label(frame, text="(no players)", fg="gray50", bg=PANEL_BG,
                         font=("Arial", 12, "italic")).grid(row=0, column=0, sticky="w")

            self.team_total_labels[team].config(text=str(self.team_score(team)))

    def team_score(self, team):
        return sum(p["score"] for p in self.teams[team])

    def add_event(self, text):
        """Add a line to the Current Game Action window (newest at the bottom)."""
        self.action_text.config(state="normal")
        self.action_text.insert("end", text + "\n")
        self.action_text.see("end")
        self.action_text.config(state="disabled")

    def set_time_remaining(self, seconds):
        minutes, secs = divmod(max(0, int(seconds)), 60)
        self.timer_label.config(text=f"Time Remaining: {minutes}:{secs:02d}")

    # ---------------- game control ----------------
    def start_game(self):
        """Start the game: broadcast the start code (202) to the players.
        NOTE for the 30-second countdown task: call this when the countdown
        reaches zero instead of right away."""
        self.game_running = True
        if self.udp is not None:
            try:
                self.udp.broadcast_start()
            except OSError as e:
                print(f"[Game] Could not broadcast start code: {e}")
        print("[Game] Game started")


# Run this file on its own to preview the screen with sample players.
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x800")
    root.configure(bg=BG)
    red = [{"codename": n, "equipment_id": i} for i, n in enumerate(["Opus", "Viper", "Ghost"], 1)]
    green = [{"codename": n, "equipment_id": i} for i, n in enumerate(["Scooby", "Shadow"], 11)]
    screen = PlayActionScreen(root, red, green)
    screen.pack(fill="both", expand=True)
    root.mainloop()
