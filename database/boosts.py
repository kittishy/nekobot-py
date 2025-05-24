from datetime import datetime, timedelta
import discord 
from discord.ext import commands
from discord import app_commands
import os
import json
import logging

logger = logging.getLogger(__name__)

BOOST_FILE_PATH = 'boosts.json'

# Inicializar arquivo se não existir
if not os.path.exists(BOOST_FILE_PATH):
    try:
        with open(BOOST_FILE_PATH, 'w') as file:
            json.dump({}, file, indent=4)
        logger.info(f"Arquivo {BOOST_FILE_PATH} criado")
    except Exception as e:
        logger.error(f"Erro ao criar arquivo {BOOST_FILE_PATH}: {e}")


def read_json():
    """Lê os dados de boost do arquivo JSON."""
    try:
        with open(BOOST_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning(f"Arquivo {BOOST_FILE_PATH} não encontrado, criando novo")
        write_json({})
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON em {BOOST_FILE_PATH}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Erro ao ler {BOOST_FILE_PATH}: {e}")
        return {}
    

def write_json(data):
    """Escreve os dados de boost no arquivo JSON."""
    try:
        with open(BOOST_FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logger.error(f"Erro ao escrever em {BOOST_FILE_PATH}: {e}")
        raise


async def changeBoost(user, boost):
    """Altera o número de boosts de um usuário."""
    try:
        data = read_json()
        user_id_str = str(user.id)
        data[user_id_str] = {"boosts": boost}
        write_json(data)
        logger.info(f"Boosts do usuário {user} alterados para {boost}")
        return data[user_id_str]
    except Exception as e:
        logger.error(f"Erro ao alterar boosts do usuário {user}: {e}")
        raise

async def addBoost(user):
    """Adiciona um boost para um usuário."""
    try:
        user_id_str = str(user.id)
        data = read_json()
        
        if user_id_str not in data:
            data[user_id_str] = {"boosts": 1}
        else:
            data[user_id_str]["boosts"] += 1
            
        write_json(data)
        boost_count = data[user_id_str]["boosts"]
        logger.info(f"Boost adicionado para {user}. Total: {boost_count}")
        return boost_count
    except Exception as e:
        logger.error(f"Erro ao adicionar boost para {user}: {e}")
        raise

async def getBoosts(user):
    """Obtém o número de boosts de um usuário."""
    try:
        user_id_str = str(user.id)
        data = read_json()
        return data.get(user_id_str, {"boosts": 0})["boosts"]
    except Exception as e:
        logger.error(f"Erro ao obter boosts do usuário {user}: {e}")
        return 0

async def removeBoost(user):
    """Remove um boost de um usuário."""
    try:
        user_id_str = str(user.id)
        data = read_json()
        
        if user_id_str in data and data[user_id_str]["boosts"] > 0:
            data[user_id_str]["boosts"] -= 1
            write_json(data)
            boost_count = data[user_id_str]["boosts"]
            logger.info(f"Boost removido de {user}. Total: {boost_count}")
            return boost_count
        else:
            logger.warning(f"Tentativa de remover boost de {user} que não possui boosts")
            return 0
    except Exception as e:
        logger.error(f"Erro ao remover boost de {user}: {e}")
        raise

async def getAllBoosts():
    """Obtém todos os dados de boost."""
    try:
        return read_json()
    except Exception as e:
        logger.error(f"Erro ao obter todos os boosts: {e}")
        return {}