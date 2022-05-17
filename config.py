import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
MODEL_PATH = os.getenv("MODEL_PATH")
COLUMN_DATA_PATH = os.getenv("COLUMN_DATA_PATH")
HELP_PIC_PATH = os.getenv("HELP_PIC_PATH")