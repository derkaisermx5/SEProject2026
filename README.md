# Photon Laser Tag

Entry terminal software for Photon laser tag (splash screen, player entry, player action, countdown, UDP equipment codes, PostgreSQL player lookup).


## Team

| GitHub username | Real name |
|-----------------|-----------|
| derkaisermx5 | Jared Ramirez |
| GideonFox | Joshua Fox |
| MartinAlmaraz27 | Martin Almaraz |
| hernandezstephen994-afk | Stephen Hernandez |

## Prerequisites

- Python 3
- PostgreSQL installed and running
- `psql` available in your terminal
- **Linux (Debian) only:** tkinter and venv aren't bundled with Python the way they are on Windows/Mac and need a one-time install:
  ```bash
  sudo apt install python3-tk python3-venv
  ```

## Install

From the project folder.

Windows:

```bash
python Install.py
```

Debian / Linux:

```bash
python3 Install.py
```

This installs the Python packages from `requirements.txt` (Pillow, screeninfo, psycopg2-binary).

On Debian, Install.py creates a virtual environment in the `venv` folder by itself and installs the packages there. main.py uses that folder automatically, so just run `python3 main.py` afterward. You do not need to create or activate a virtual environment yourself.

PostgreSQL itself is not installed by this script — set that up separately.

## Database setup

On the Debian lab image, run these from the project folder. No username or password is needed:

```bash
psql -d postgres -f create_database.sql
psql -d photon -f players.sql
```

### Windows / other machines that need a login (optional)

If your local PostgreSQL asks for a username and password (the Windows installer does), run the setup with `-U postgres`:

```bash
psql -U postgres -d postgres -f create_database.sql
psql -U postgres -d photon -f players.sql
```

Then tell the app how to log in with environment variables before running it. If they are not set, the app connects with no login (the Debian default).

| Variable | Meaning |
|----------|---------|
| `PHOTON_DB_USER` | database user, e.g. `postgres` |
| `PHOTON_DB_PASSWORD` | that user's password |
| `PHOTON_DB_HOST` | optional, e.g. `localhost` |
| `PHOTON_DB_PORT` | optional, e.g. `5432` |

Current terminal window only:

- Windows (Command Prompt): `set PHOTON_DB_USER=postgres` then `set PHOTON_DB_PASSWORD=your_postgres_password`
- Linux/Mac (bash): `export PHOTON_DB_USER=postgres` then `export PHOTON_DB_PASSWORD=your_postgres_password`

To keep them permanently on your own machine:

- Windows: search "Edit the system environment variables" → Environment Variables → under *User variables*, click New for each variable. Open a new terminal afterward.
- Linux/Mac: add the `export` lines to `~/.bashrc` (or `~/.zshrc` on Mac), then run `source ~/.bashrc`.

## Run

Windows:

```bash
python main.py
```

Debian / Linux:

```bash
python3 main.py
```

Optional network for UDP (if needed), for example:

```bash
python3 main.py --network 127.0.0.1
```

### Player entry (quick)

1. After the splash, press **F1** (or click F1 Edit Game)
2. Click a team slot and press **Enter**
3. Enter a **player ID** — looked up in the `players` table; if missing, enter a new codename to save it, no duplicate player ID's can be used
4. Enter an **equipment ID** — broadcast over UDP, equipment ID's range from 1 to 80
5. Press **F5** (or click F5 Start Game) once at least one player is added — a 30-second countdown plays, then the play action screen appears
6. Press **F12** to clear all players, or **F2** to change the UDP network

### Play action screen
Both teams will be displayed onto the screen with the red team on the left and the green team on the right. Each players codename will be shown.

### Network / ports

- App **sends** on port **7500**
- App **listens** on port **7501**
- Default address: **127.0.0.1**