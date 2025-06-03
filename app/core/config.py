from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    DATABSE_URL = os.getenv("DATABSE_URL")



config = Config()