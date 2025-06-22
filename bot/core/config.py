from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    @property
    def DATABASE_URL(self) -> str:
        db_host: str = os.getenv("DB_HOST", "localhost")
        db_port: str = os.getenv("DB_PORT", "5432")
        db_name: str = os.getenv("DB_NAME", "freelancehunt-db")
        db_user: str = os.getenv("DB_USER", "postgres")
        db_password: str = os.getenv("DB_PASSWORD", "")

        return f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


settings = Settings()
