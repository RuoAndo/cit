#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import random

# the number of characters: 100
# the number of players: 30

dbname = 'cit-db-2024-08.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

try:
    comstr1 = "DROP TABLE IF EXISTS character;"
    cur.execute(comstr1)
except Exception as e:
    print(f"Error dropping table: {e}")

# Create table with proper structure
comstr2 = """
CREATE TABLE character (
    character_id INTEGER, 
    player_id INTEGER, 
    character_name VARCHAR(20), 
    HP INTEGER, 
    MP INTEGER, 
    EXP INTEGER, 
    character_rank INTEGER
);
"""
cur.execute(comstr2)
conn.commit()

# Insert 200 characters
for number in range(200):
    l = ['doraemon', 'akinator', 'golgo', 'begita', 'bikkuriko']
    l_weight = [10, 1, 1, 1, 1]
    
    character_name = random.choices(l, weights=l_weight)[0]
    playerID = random.randint(1, 30)  # Range includes 30
    HP = random.randint(1, 100)
    MP = random.randint(1, 100)
    EXP = random.randint(1, 100)
    character_rank = random.randint(1, 10)

    # Correctly formatted SQL statement
    comstr = f"""
    INSERT INTO character (character_id, player_id, character_name, HP, MP, EXP, character_rank) 
    VALUES ({number}, {playerID}, '{character_name}', {HP}, {MP}, {EXP}, {character_rank});
    """
    cur.execute(comstr)

conn.commit()

# Fetch and display the first 10 rows
cur = conn.cursor()
cur.execute('SELECT * FROM character LIMIT 200')

for row in cur:
    print(row)

cur.close()
conn.close()
