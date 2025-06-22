from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

# ===== GENERAL SETTINGS =====
DEBUG            = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
SECRET_KEY       = os.getenv("SECRET_KEY", "default-secret-key")
ADMIN_HOST       = os.getenv("ADMIN_HOST", "localhost")
ADMIN_PORT       = int(os.getenv("ADMIN_PORT", "8000"))
ADMIN_PASSWORD   = os.getenv("ADMIN_PASSWORD", "default-admin-password")


# ========= DATABASE =========
def database_url() -> str:
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "freelancehunt-db")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "")

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

SQLALCHEMY_DATABASE_URI = database_url()
SQLALCHEMY_ECHO = False
