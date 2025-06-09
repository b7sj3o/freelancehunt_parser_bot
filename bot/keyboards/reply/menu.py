from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import bot.services as rq


async def menu_keyboard(user_id: int):
    is_superuser = await rq.users.is_superuser(user_id)

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Адмін-панель")] if is_superuser else [],
            [KeyboardButton(text="Перевірити доступні вакансії")],
            [
                KeyboardButton(text="Переглянути активні теми"),
                KeyboardButton(text="Змінити теми"),
            ],
            [
                KeyboardButton(text="Змінити фільтри"),
            ],
            [KeyboardButton(text="Допомога / Зв'язатись з нами")],
            [KeyboardButton(text="Деактивувати бота")],
        ],
        resize_keyboard=True
    )

def admin_keyboard() -> ReplyKeyboardMarkup:
    """Creates a reply keyboard for admin users."""
    
    buttons = [
        [KeyboardButton(text="Створити тему"), KeyboardButton(text="Створити підтему")],
        [KeyboardButton(text="На головну")],
    ]
    
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def filters_keyboard() -> ReplyKeyboardMarkup:
    """Creates a reply keyboard for filters."""
    
    buttons = [
        [KeyboardButton(text="Мін/Макс ціна проекту")],
        [KeyboardButton(text="Максимальна к-сть ставок")],
        [KeyboardButton(text="Чорний список слів")],
        [KeyboardButton(text="На головну")],
    ]
    
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)