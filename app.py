from flask import Flask
from threading import Thread
import klutz

from dotenv import load_dotenv
import os

app = Flask('klutztower')

@app.route('/')
def home():
    return "<p>Hello. I am alive!<p>"

def run():
    print("Hello, I'm also alive")
    
    app.run()
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    if (TOKEN is None):
        raise Exception('No token found!')

    klutz.client.run(TOKEN)


def keep_alive():
    t = Thread(target=run)
    t.start()
