from typing import List
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder

import bot.services as rq
from bot.db.models import CategoryItem


async def reply_categories_keyboard():
    categories = await rq.categories.get_categories()
    builder = KeyboardBuilder(button_type=KeyboardButton)
    for category in categories:
        builder.add(KeyboardButton(text=category.name))

    return builder.as_markup(resize_keyboard=True)


async def reply_category_items_keyboard(category_items: List[CategoryItem]):
    builder = KeyboardBuilder(button_type=KeyboardButton)
    for item in category_items:
        builder.add(KeyboardButton(text=item.name))

    if not category_items:
        builder.add(KeyboardButton(text="Підкатегорій немає"))

    return builder.as_markup(resize_keyboard=True)


