import os

from dotenv import load_dotenv


load_dotenv()

PATH_DB = str(os.getenv('PATH_DB'))

APP_LOG_FILE = str(os.getenv('LOG_FILE_NAME'))

API_TOKEN = str(os.getenv('API_TOKEN'))

OWNER_ID = os.getenv('OWNER')

GREETINGS_TEXT = str(os.getenv('GREETINGS_TEXT'))

HELP_TEXT = str(os.getenv('HELP_TEXT'))

ITEMS_NAME = str(os.getenv('NAME_ITEMS'))

PATH_CURR_PHOTO = str(os.getenv('PATH_CURR_PHOTO'))

LIST_USERS = str(os.getenv('LIST_USERS'))