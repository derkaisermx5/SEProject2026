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
- **Linux only:** tkinter and pip isn't bundled with Python the way it is on Windows/Mac and needs a separate install:
  ```bash
  sudo apt install python3-tk
  sudo apt install python3-pip
  ```

## Install

From the project folder:

```bash
python Install.py / python3 Install.py
```

This install Python packages from `requirements.txt` (Pillow, screeninfo, psycopg2-binary).

When running Install.py on Debian, make sure it is ran in a virtual environment.
Install Python's virtual environments.
```bash
sudo apt update 
sudo apt install python3-venv
```
After that, start a virtual environment in the directory where all the code is stored with these commands.
```bash
python3 -m venv venv
source venv/bin/activate
```
This will create a virtual environment folder in the directory and allow the install script to work.
PostgreSQL itself is not installed by this script — set that up separately.

## Database setup

```bash
psql -U postgres -d postgres -f create_database.sql
psql -U postgres -d photon -f players.sql
```

The app reads your PostgreSQL password from an environment variable named `PHOTON_DB_PASSWORD` (it's never hardcoded in the code). Set it to whatever password you chose for the `postgres` user during your own PostgreSQL install.

**If you're just testing/grading this once**, use the temporary version — it only lasts for your current terminal window and leaves nothing behind afterward:

- Windows (Command Prompt): `set PHOTON_DB_PASSWORD=your_postgres_password`
- Linux/Mac (bash): `export PHOTON_DB_PASSWORD=your_postgres_password`

**If this is your own dev machine** and you'll be running the app repeatedly, set it permanently instead so you don't have to retype it every session:

- Windows: search "Edit the system environment variables" → Environment Variables → under *User variables*, click New → Name: `PHOTON_DB_PASSWORD`, Value: your password. Open a new terminal afterward for it to take effect.
- Linux/Mac: add `export PHOTON_DB_PASSWORD=your_postgres_password` to `~/.bashrc` (or `~/.zshrc` on Mac), then run `source ~/.bashrc`.

## Run

```bash
python main.py / python3 main.py
```

Optional network for UDP (if needed):

```bash
python main.py --network 127.0.0.1 (python3 main.py --network 127.0.0.1
```

### Player entry (quick)

1. After the splash, press **F1** (or click F1 Edit Game)
2. Click a team slot and press **Enter**
3. Enter a **player ID** — looked up in the `players` table; if missing, enter a new codename to save it, no duplicate player ID's can be used
4. Enter an **equipment ID** — broadcast over UDP, equipment ID's range from 1 to 80

### Play action screen
Both teams will be displayed onto the screen with the red team on the left and the green team on the right. Each players codename will be shown.

### Network / ports

- App **sends** on port **7500**
- App **listens** on port **7501**
- Default address: **127.0.0.1**

