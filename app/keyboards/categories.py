from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder, InlineKeyboardBuilder

import app.db.crud.user as rq
from app.db.models import CategoryItem

async def register_categories_keyboard():
    categories = await rq.get_categories()
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.add(InlineKeyboardButton(text=category.name, callback_data=f"register_category:{category.name}"))
    
    if len(categories) > 10:
        builder.adjust(3)
    elif len(categories) > 5:
        builder.adjust(2)
    else:
        builder.adjust(1)

    builder.row(InlineKeyboardButton(text="Підтвердити", callback_data="submit_register"))

    return builder.as_markup(resize_keyboard=True)


async def register_category_items_keyboard(category_items: List[Tuple[CategoryItem, bool]]):
    builder = InlineKeyboardBuilder()
    for item, is_selected in category_items:
        builder.add(InlineKeyboardButton(text=f"{item.name} {"✅" if is_selected else ""}", callback_data=f"category_item:{item.name}"))

    if len(category_items) > 10:
        builder.adjust(3)
    elif len(category_items) > 5:
        builder.adjust(2)
    else:
        builder.adjust(1)


    builder.row(
        InlineKeyboardButton(text="Назад", callback_data="go_back_register"),
        # InlineKeyboardButton(text="Підтвердити", callback_data="submit_category_items")
    )

    return builder.as_markup(resize_keyboard=True)


async def reply_categories_keyboard():
    categories = await rq.get_categories()
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