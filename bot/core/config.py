from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    DATABASE_URL = os.getenv("DATABASE_URL")



settings = Settings()