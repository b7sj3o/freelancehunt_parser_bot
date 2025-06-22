import asyncio
from aiogram import Bot, Dispatcher

from bot.core.config import settings
from bot.handlers import (
    start_router,
    text_handlers_router,
    manage_categories_router,
    manage_data_router,
    filters_router,
)
from bot.db.models import create_db
from bot.core import logger

async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        start_router, manage_categories_router, text_handlers_router, manage_data_router, filters_router
    )

    await create_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Starting bot...")
        asyncio.run(main(), debug=True)
    except KeyboardInterrupt:
        print("Bot stopped by user.")
