import asyncio
from datetime import datetime
import logging
import os
from pathlib import Path
from typing import Any, cast

import aiomysql as asql

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
        db=os.getenv("DATABASE")
    ))

async def load_all_schemas():
    for file_path in SCHEMA_PATH.glob("*.sql"):
        await run_schema(str(file_path))

def open_file(schema_file_path: str):
    with open(schema_file_path, 'r', encoding='utf-8') as file:
        schema_sql = file.read()
    return schema_sql

async def run_schema(schema_file_path: str):
    schema_sql = await asyncio.to_thread(open_file, schema_file_path)
    await execute_fetch(schema_sql)

async def get_connection():
    cnx = await cnx_pool.acquire()
    try:
        await cnx.ping(reconnect=True)
    except Exception:
        cnx_pool.release(cnx)
        cnx = await cnx_pool.acquire()
    return cnx

async def __fetch[T](cursor: asql.Cursor, prompt: str, *args, _type: type[T] = tuple[Any]) -> list[T]:
    await cursor.execute(prompt, args)
    return await cursor.fetchall()

async def execute_fetch[T](prompt: str, *args, _type: type[T] = tuple[Any]) -> list[T] | None:
    assert cnx_pool is not None
    connection = None
    try:
        async with cnx_pool.acquire() as _connection:
            connection = cast(asql.Connection, _connection)
            await connection.ping()
            async with connection.cursor() as _cur:
                cursor = cast(asql.Cursor, _cur)
                result = await asyncio.wait_for(
                    __fetch(cursor, prompt, *args, _type=_type),
                    timeout=10
                )
            await connection.commit()
    except asql.IntegrityError as e:
        logger.error(f"Integrity Error '{prompt}': {e}")
        return None
    except asql.OperationalError as e:
        logger.error(f"Database operational error: {e}")
        return None
    except asql.Error as e:
        logger.error(f"Unexpected database error: {e}")
        return None
    return result

async def get_sounds() -> list[str]:
    data = await execute_fetch("SELECT * FROM furry_sound;", _type = tuple[str])
    if data is None:
        return []
    return [s[0] for s in data]

async def add_sound(sound: str):
    await execute_fetch("INSERT IGNORE INTO furry_sound VALUES (%s);", sound)

async def remove_sound(sound: str):
    await execute_fetch("DELETE FROM furry_sound WHERE sound=%s;", sound)

async def get_meme_ids() -> list[int]:
    prompt = "SELECT id FROM memes;"
    
    data = await execute_fetch(prompt, _type = tuple[int])
    if data is None:
        return []
    return [s[0] for s in data]

async def get_meme(id: int) -> tuple[str, bytes]:
    prompt = "SELECT meme_name, meme_data FROM memes WHERE id=%s;"
    
    data = await execute_fetch(prompt, id, _type = tuple[str, bytes])
    if data is None:
        return "", bytes(0)
    if len(data) == 0:
        return "", bytes(0)
    return data[0]

async def get_meme_by_name(name: str) -> list[tuple[int, str]]:
    prompt = "SELECT id, meme_name FROM memes WHERE meme_name REGEXP %s"
    
    data = await execute_fetch(prompt, name, _type=tuple[int, str])
    if data is None:
        return []
    return data

async def add_meme(file_name: str, file_data: bytes):
    result = await execute_fetch("INSERT IGNORE INTO memes (id, meme_name, meme_data) VALUES (NULL, %s, %s)", file_name, file_data)
    return result is not None

async def get_people_by_birthday(birthdate: datetime):
    prompt = "SELECT user FROM birthday WHERE birthdate = %s"
    
    bd = birthdate.strftime('%Y-%m-%d')
    
    data = await execute_fetch(prompt, bd, _type = tuple[int])
    if data is None:
        return None
    if len(data) == 0:
        return None
    return data[0][0]

async def get_birthday_by_person(user_id: int):
    prompt = "SELECT birthdate FROM birthday WHERE user = %s"
    
    data = await execute_fetch(prompt, user_id, _type = tuple[datetime])
    if data is None:
        return None
    if len(data) == 0:
        return None
    return data[0][0]

async def set_birthday(user_id: int, birthdate: datetime):
    bd = birthdate.strftime('%Y-%m-%d')
    await execute_fetch("INSERT INTO birthday (user, birthdate) VALUES (%s, %s) ON DUPLICATE KEY UPDATE birthdate=%s", user_id, bd, bd)

async def remove_birthday(user_id: int):
    await execute_fetch("DELETE FROM birthday WHERE user=%s", user_id)