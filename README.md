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

## Install

From the project folder:

```bash
python Install.py
```

This install Python packages from `requirements.txt` (Pillow, screeninfo, psycopg2-binary).

PostgreSQL itself is not installed by this script — set that up separately.

## Database setup

```bash
psql -d postgres -f create_database.sql
psql -d photon -f players.sql
```

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
