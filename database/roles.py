import json
import os

ROLE_ID_FILE_PATH='role_id.json'

if not os.path.exists(ROLE_ID_FILE_PATH):
    with open(ROLE_ID_FILE_PATH, 'w') as file:
      json.dump({"role_id": None},file)


def get_role_id():
   with open(ROLE_ID_FILE_PATH, 'r') as file:
      data = json.load(file)
   return data.get("role_id")


def set_role_id(role_id):
   with open(ROLE_ID_FILE_PATH, 'w') as file:
      json.dump({"role_id": role_id}, file, indent=4)