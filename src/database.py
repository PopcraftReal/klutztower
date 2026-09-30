import os
from typing import cast

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLCursorAbstract

cursor = None
cnx_pool: mysql.connector.pooling.MySQLConnectionPool

def init():
    global cnx_pool
    cnx_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mainPool",
        pool_size=3,
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DATABASE")
    )

def execute_fetch(prompt: str):
    assert cnx_pool is not None
    
    try:
        connection = cnx_pool.get_connection()
        cursor: MySQLCursorAbstract = connection.cursor()
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
    if data is None:
        return []
    return [s[0] for s in data]

def add_sound(sound: str):
    try:
        execute_fetch(f"INSERT INTO furry_sound VALUES ('{sound}');")
    except:  # noqa: E722
        return

def remove_sound(sound: str):
    try:
        execute_fetch(f"DELETE FROM furry_sound WHERE sound='{sound}';")
    except:  # noqa: E722
        return