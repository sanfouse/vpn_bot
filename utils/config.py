import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
ADMIN_IDS = []

USERNAME = str(os.getenv('USERNAME'))
PASSWORD = str(os.getenv('PASSWORD'))
HOST = str(os.getenv('HOST'))
PORT = str(os.getenv('PORT'))
DATABASE = str(os.getenv('DATABASE'))

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
