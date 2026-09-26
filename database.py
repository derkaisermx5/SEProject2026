# this is the updated sample from Dr. Strother python-pg.py file

import os
import psycopg2

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'postgres',
    'password': os.environ.get('PHOTON_DB_PASSWORD'),
    #'host': 'localhost',
    #'port': '5432'
}

def get_connection():
    # I have to open a connection to the phton database.
    return psycopg2.connect(**connection_params)


# I think the app/program would read this like get_codename(1) which turns to "txt" or None
def get_codename(player_id):
    # now I have to return the codename for player_id, or None, if its not in the table
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT codename FROM players WHERE id = %s",
            (player_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None
    finally:
        if conn:
            conn.close()


# if None, ask for name, then it should be add_player(1, "txt")
def add_player(player_id, codename):
    "Insert a new player"
    # Raises if id already existss or the database is 
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            # this part was a little confusing.
            " INSERT INTO players (id, codename) VALUES (%s, %s);",
            (player_id, codename),
        )
        conn.commit()
        cursor.close()
    finally:
        if conn:
            conn.close()