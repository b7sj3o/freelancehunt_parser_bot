from typing import List, Tuple
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import bot.services as rq
from bot.db.models import Category, CategoryItem


async def inline_categories_to_delete(categories: List[Category]):
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.add(
            InlineKeyboardButton(
                text=category.name,
                callback_data=f"delete_category:{category.id}"
            )
        )

    if len(categories) > 10:
        builder.adjust(3)
    elif len(categories) > 5:
        builder.adjust(2)
    else:
        builder.adjust(1)

    return builder.as_markup()

async def inline_category_items_delete(category_items: List[CategoryItem]):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="Підтема", callback_data="pass"),
        InlineKeyboardButton(text="Видалити", callback_data="pass")
    )

    for item in category_items:
        builder.row(
            InlineKeyboardButton(text=item.name, callback_data="pass"),
            InlineKeyboardButton(text="❌", callback_data=f"delete_category_item:{item.id}")
        )

    if not category_items:
        builder.row(InlineKeyboardButton(text="Підкатегорій немає", callback_data="pass"))

    builder.row(
        InlineKeyboardButton(text="Повернутись🔙", callback_data="back_to_categories")
    )

    return builder.as_markup()

async def update_categories():
    categories = await rq.categories.get_categories(with_children=True)
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.add(InlineKeyboardButton(text=category.name, callback_data=f"update_category:{category.id}"))

    if len(categories) > 7:
        builder.adjust(2)
    else:
        builder.adjust(1)

    builder.row(InlineKeyboardButton(text="Підтвердити✅", callback_data="submit_update_categories"))

    return builder.as_markup(resize_keyboard=True)


async def update_category_items(category_items: List[Tuple[CategoryItem, bool]]):
    builder = InlineKeyboardBuilder()
    for item, is_selected in category_items:
        builder.add(InlineKeyboardButton(text=f"{item.name} {"✅" if is_selected else ""}", callback_data=f"update_category_item:{item.id}"))

    if len(category_items) > 7:
        builder.adjust(2)
    else:
        builder.adjust(1)


    builder.row(
        InlineKeyboardButton(text="Підтвердити✅", callback_data="submit_category_items")
    )

    return builder.as_markup(resize_keyboard=True)
