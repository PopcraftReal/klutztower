from typing import cast

import mysql.connector
from mysql.connector import errorcode

HOST = "db-par-02.apollopanel.com"
DATABASE = "s238708_game"

cursor = None

def execute_fetch(prompt: str):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user="u238708_dHu0geqITK",
            password="BwJJ8JApz_9tPHjBg3Egk_lp",
            database=DATABASE
        )
        cursor = connection.cursor()
        cursor.execute(prompt)
        result = cursor.fetchall()
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(error)
        return None
    else:
        connection.close()
    return result

def get_sounds() -> list[str]:
    data: list[tuple[str]] = cast(list[tuple[str]], execute_fetch("SELECT * FROM furry_sound;"))
    return [s[0] for s in data]