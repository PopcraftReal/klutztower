import discord

from dotenv import load_dotenv
import os

from src.BotClient import BotClient
import mysql.connector

PREFIX = '-'
HOST = "db-par-02.apollopanel.com"
DATABASE = "s238708_game"
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = BotClient(command_prefix=PREFIX, intents=intents)

if __name__ == "__main__":
    load_dotenv()
    token: str | None = os.getenv('DISCORD_TOKEN')
    if token is None:
        token = ""
    mydb = mysql.connector.connect(
        host=HOST,
        user="u238708_dHu0geqITK",
        password="BwJJ8JApz_9tPHjBg3Egk_lp",
        database=DATABASE
    )
    mycursor = mydb.cursor()
    
    mycursor.execute("SHOW DATABASES")

    for x in mycursor: # type: ignore
        print(x)
    client.run(token)