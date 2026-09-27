import discord

from dotenv import load_dotenv
import os

from src.BotClient import BotClient
import mysql.connector

PREFIX = '-'
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
        host="db-par-02.apollopanel.com:3306",
        user="u238708_dHu0geqITK",
        password="BwJJ8JApz_9tPHjBg3Egk_lp"
    )
    mycursor = mydb.cursor()
    
    mycursor.execute("SHOW DATABASES")

    for x in mycursor: # type: ignore
        print(x)
    client.run(token)