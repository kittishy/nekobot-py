import json
import os
import logging

logger = logging.getLogger(__name__)

ROLE_ID_FILE_PATH = 'role_id.json'

# Inicializar arquivo se não existir
if not os.path.exists(ROLE_ID_FILE_PATH):
    try:
        with open(ROLE_ID_FILE_PATH, 'w') as file:
            json.dump({"role_id": None}, file, indent=4)
        logger.info(f"Arquivo {ROLE_ID_FILE_PATH} criado")
    except Exception as e:
        logger.error(f"Erro ao criar arquivo {ROLE_ID_FILE_PATH}: {e}")


def get_role_id():
    """Obtém o ID do cargo Double Booster configurado."""
    try:
        with open(ROLE_ID_FILE_PATH, 'r') as file:
            data = json.load(file)
        return data.get("role_id")
    except FileNotFoundError:
        logger.warning(f"Arquivo {ROLE_ID_FILE_PATH} não encontrado")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON em {ROLE_ID_FILE_PATH}: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao ler {ROLE_ID_FILE_PATH}: {e}")
        return None


def set_role_id(role_id):
    """Define o ID do cargo Double Booster."""
    try:
        with open(ROLE_ID_FILE_PATH, 'w') as file:
            json.dump({"role_id": role_id}, file, indent=4)
        logger.info(f"Role ID definido: {role_id}")
    except Exception as e:
        logger.error(f"Erro ao salvar role ID {role_id}: {e}")
        raise