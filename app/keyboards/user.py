from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import app.db.crud.user as rq


async def base_reply_keyboard(chat_id: int):
    is_superuser = await rq.is_superuser(chat_id)

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Адмін-панель")] if is_superuser else [],
            [
                KeyboardButton(text="Переглянути активні теми"),
                KeyboardButton(text="Змінити теми"),
            ],
            [
                KeyboardButton(text="Переглянути фільтри"),
                KeyboardButton(text="Змінити фільтри"),
            ],
            [KeyboardButton(text="Допомога / Зв'язатись з нами")],
            [KeyboardButton(text="Деактивувати бота")],
        ],
        resize_keyboard=True
    )



