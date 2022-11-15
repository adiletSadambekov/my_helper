import os

from dotenv import load_dotenv


load_dotenv()

PATH_DB = str(os.getenv('PATH_DB'))

APP_LOG_FILE = str(os.getenv('LOG_FILE_NAME'))

API_TOKEN = str(os.getenv('API_TOKEN'))

OWNER_ID = int(os.getenv('OWNER'))

GREETINGS_TEXT = str(os.getenv('GREETINGS_TEXT'))

HELP_TEXT = str(os.getenv('HELP_TEXT'))

PATH_CURR_PHOTO = str(os.getenv('PATH_CURR_PHOTO'))

LIST_USERS = str(os.getenv('LIST_USERS'))

LIST_ADMINS_COMMANDS = str(os.getenv('LIST_ADMINS_COMMANDS'))

URL_FOR_PARSER = str(os.getenv('URL_FOR_PARSING'))

USER_AGENT = str(os.getenv('USER_AGENT'))

ITEMS_NAMES = str(os.getenv('ITEMS_NAMES')).split(',')

ITEMS_NAME = str(os.getenv('ITEMS_NAME'))

BISHKEK_TZ = str(os.getenv('BISHKEK_TZ'))

FIRST_USERS_ACCES = int(os.getenv('FIRST_USERS_ACCES'))

TURNOVER = int(os.getenv('TURNOVER'))

PATH_TIMES_FILE = str(os.getenv('PATH_TIMES_FILE'))