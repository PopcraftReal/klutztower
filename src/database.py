from typing import cast

import mysql.connector

HOST = "db-par-02.apollopanel.com"
DATABASE = "s238708_game"

cursor = None

def connect():
    global cursor
    mydb = mysql.connector.connect(
        host=HOST,
        user="u238708_dHu0geqITK",
        password="BwJJ8JApz_9tPHjBg3Egk_lp",
        database=DATABASE
    )
    cursor = mydb.cursor()

def execute_fetch(prompt: str):
    assert cursor is not None
    cursor.execute(prompt)
    return cursor.fetchall()

def get_sounds() -> list[str]:
    data: list[tuple[str]] = cast(list[tuple[str]], execute_fetch("SELECT * FROM sound;"))
    return [s[0] for s in data]