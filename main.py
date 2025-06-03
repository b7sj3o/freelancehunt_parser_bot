import asyncio

from aiogram import Bot, Dispatcher

from app.core.config import config
from app.handlers import start_router, text_handlers_router, manage_categories_router
from app.db.models import create_db


async def main():
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(start_router, manage_categories_router, text_handlers_router)
    
    await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("Starting bot...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
