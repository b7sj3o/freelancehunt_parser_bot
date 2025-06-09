# from typing import List, Tuple
# from aiogram.types import InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder

# import bot.services as rq
# from bot.db.models import CategoryItem


# async def register_categories_keyboard():
#     categories = await rq.categories.get_categories()
#     builder = InlineKeyboardBuilder()

#     for category in categories:
#         builder.add(InlineKeyboardButton(text=category.name, callback_data=f"register_category:{category.id}"))

#     if len(categories) > 7:
#         builder.adjust(2)
#     else:
#         builder.adjust(1)

#     builder.row(InlineKeyboardButton(text="Підтвердити", callback_data="submit_register"))

#     return builder.as_markup(resize_keyboard=True)


# async def register_category_items_keyboard(category_items: List[Tuple[CategoryItem, bool]]):
#     builder = InlineKeyboardBuilder()
#     for item, is_selected in category_items:
#         builder.add(InlineKeyboardButton(text=f"{item.name} {"✅" if is_selected else ""}", callback_data=f"category_item:{item.id}"))

#     if len(category_items) > 7:
#         builder.adjust(2)
#     else:
#         builder.adjust(1)


#     builder.row(
#         InlineKeyboardButton(text="Підтвердити✅", callback_data="submit_category")
#     )

#     return builder.as_markup(resize_keyboard=True)
