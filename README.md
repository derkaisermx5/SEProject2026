# Photon Laser Tag

Entry terminal software for Photon laser tag (splash screen, player entry, UDP equipment codes, PostgreSQL player lookup).


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
- **Linux only:** tkinter isn't bundled with Python the way it is on Windows/Mac and needs a separate install:
  ```bash
  sudo apt install python3-tk
  ```

## Install

From the project folder:

```bash
python Install.py
```

This install Python packages from `requirements.txt` (Pillow, screeninfo, psycopg2-binary).

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
python main.py
```

Optional network for UDP (if needed):

```bash
python main.py --network 127.0.0.1
```

### Player entry (quick)

1. After the splash, press **F1** (or click F1 Edit Game)
2. Click a team slot and press **Enter**
3. Enter a **player ID** — looked up in the `players` table; if missing, enter a new codename to save it
4. Enter an **equipment ID** — broadcast over UDP

## Network / ports

- App **sends** on port **7500**
- App **listens** on port **7501**
- Default address: **127.0.0.1**

## Debugging for Debian
If pip commands aren't working, Debian's repository configurations need to be fixed
1. Back up current repository configuration
```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
``` 
2. Open the repository configuration
```bash
sudo nano /etc/apt/sources.list
```
3. When inside the configuration, comment out any "security.debian.org" lines or "bullseye-security" with a # in the front
4. Add this line `deb http://archive.debian.org/debian bullseye main contrib non-free`
5. Save with CTRL + o and exit with CTRL + x
6. Run the update command to verify if everything worked
```bash
sudo apt update
```
7. Run the pip command to install python3 pip and tkinter
```bash
sudo apt install python3-pip
```
```bash
sudo apt install python3-tk
```
8. Everything should be set to run the Install script
