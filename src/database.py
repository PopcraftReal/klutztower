import os

from pathlib import Path
from typing import cast

import mysql.connector
from mysql.connector import Error, errorcode
from mysql.connector.abstracts import MySQLCursorAbstract

SCHEMA_PATH = Path("./sql_schemas/")

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

def load_all_schemas():
    for file_path in SCHEMA_PATH.glob("*.sql"):
        run_schema(str(file_path))

def run_schema(schema_file_path: str):
    assert cnx_pool is not None
    connection = None
    cursor: None | MySQLCursorAbstract = None
    try:
        connection = cnx_pool.get_connection()
        if not connection.is_connected():
            return
        cursor: None | MySQLCursorAbstract = connection.cursor()
        if cursor is None:
            return
        
        # 2. Read the SQL schema file
        with open(schema_file_path, 'r', encoding='utf-8') as file:
            schema_sql = file.read()
        
        print(f"Executing SQL schema from {schema_file_path}...")
        cursor.execute(schema_sql)
        print("Schema executed and applied successfully!")
    except Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(error)
        if connection is not None and connection.is_connected():
            connection.rollback()
        return
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def execute_fetch(prompt: str):
    assert cnx_pool is not None
    connection = None
    try:
        connection = cnx_pool.get_connection()
        cursor: MySQLCursorAbstract = connection.cursor()
        cursor.execute(prompt)
        result = cursor.fetchall()
    except Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(error)
        return None
    finally:
        if connection is not None and connection.is_connected():
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