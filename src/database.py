import os

from pathlib import Path
from typing import cast

import aiomysql as asql
import logging

logger = logging.getLogger()

SCHEMA_PATH = Path("./sql_schemas/")

cursor = None
cnx_pool: asql.Pool

async def init():
    global cnx_pool
    cnx_pool = cast(asql.Pool, await asql.create_pool(
        minsize=3,
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        db=os.getenv("DATABASE"),
        recycle=1800
    ))

async def load_all_schemas():
    for file_path in SCHEMA_PATH.glob("*.sql"):
        await run_schema(str(file_path))

async def run_schema(schema_file_path: str):
    with open(schema_file_path, 'r', encoding='utf-8') as file:
        schema_sql = file.read()
        await execute_fetch(schema_sql)

async def get_connection():
    cnx = await cnx_pool.acquire()
    try:
        await cnx.ping(reconnect=True)
    except Exception:
        cnx_pool.release(cnx)
        cnx = await cnx_pool.acquire()
    return cnx

async def execute_fetch(prompt: str):
    assert cnx_pool is not None
    connection = None
    try:
        async with cnx_pool.acquire() as _connection:
            connection = cast(asql.Connection, _connection)
            await connection.ping()
            async with connection.cursor() as _cur:
                cursor = cast(asql.Cursor, _cur)
                await cursor.execute(prompt)
                result = await cursor.fetchall()
            await connection.commit()
    except asql.IntegrityError as e:
        logger.error(
            f"Integrity Error '{prompt}': {e}"
        )
        return None
    except asql.OperationalError as e:
        logger.error(f"Database operational error: {e}")
        return None
    except asql.Error as e:
        logger.error(f"Unexpected database error: {e}")
        return None
    return result

def get_sounds() -> list[str]:
    data: list[tuple[str]] = cast(list[tuple[str]], execute_fetch("SELECT * FROM furry_sound;"))
    if data is None:
        return []
    return [s[0] for s in data]

async def add_sound(sound: str):
    await execute_fetch(f"INSERT IGNORE INTO furry_sound VALUES ('{sound}');")

async def remove_sound(sound: str):
    await execute_fetch(f"DELETE FROM furry_sound WHERE sound='{sound}';")