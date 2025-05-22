from datetime import datetime, timedelta
import discord 
from discord.ext import commands
from discord import app_commands
import os
import json

BOOST_FILE_PATH = 'boosts.json'

if not os.path.exists(BOOST_FILE_PATH):
    with open(BOOST_FILE_PATH, 'w') as file:
        json.dump({}, file)


def read_json():
    with open(BOOST_FILE_PATH, 'r') as file:
        return json.load(file)
    

def write_json(data):
    with open(BOOST_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)


async def changeBoost(user, boost):
    data = read_json()
    user_id_str = str(user.id)
    data[user_id_str] = {"boosts": boost}
    write_json(data)
    return data[user_id_str]

async def addBoost(user):
    user_id_str = str(user.id)
    data = read_json()
    if user_id_str not in data:
        data[user_id_str] = {"boosts": 1}
    else:
        data[user_id_str]["boosts"] +=1
    write_json(data)
    return data[user_id_str]["boosts"]

async def getBoosts(user):
    user_id_str = str(user.id)
    data = read_json()
    return data.get(user_id_str, {"boost": 0})["boosts"]