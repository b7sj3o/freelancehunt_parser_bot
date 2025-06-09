import asyncio
import time
from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

import bot.keyboards as kb
import bot.services.users as rq
from bot.filters.admin import AdminFilter
from bot.parser.freelancehunt import parse_data

router = Router(name="user_text_handlers")


@router.message(F.text == "На головну")
async def handle_home(message: Message):
    await message.answer(
        "Повертаємось на головну",
        reply_markup=await kb.reply.menu.menu_keyboard(message.chat.id),
    )


# @router.message(F.text == "Адмін-панель", AdminFilter())
# async def handle_admin_panel(message: Message):
#     await message.answer("Вітаємо, адмін!", reply_markup=kb.reply.menu.admin_keyboard())


@router.message(F.text == "Перевірити доступні вакансії")
async def handle_check_vacancies(message: Message):
    user = await rq.get_user_by_id(message.chat.id)

    links = [item.link for item in user.category_items]
    data = []
    
    for link in links:
        data.extend(await parse_data(link, user))

    for count, item in enumerate(data):
        if count >= 5:
            break

        await message.answer(
            text=f"Вакансія: {item.title}\n"
            f"Ціна: {item.price}грн\n"
            f"Опис: {item.description}\n"
            f"Теги: {', '.join(item.tags)}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Перейти до вакансії",
                            url=item.link,
                        )
                    ]
                ]
            ),
        )
        await asyncio.sleep(0.5)

    if len(data) > 5:
        await message.answer(
            text="Ось! Це вакансії, які ми знайшли за вашими темами👆",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Показати ще 5 вакансій",
                            callback_data=f"next_vacancy:{count}",
                        )
                    ]
                ]
            ),
        )
    elif len(data) == 0:
        await message.answer(
            text="На жаль, ми не знайшли вакансій за вашими темами та фільтрами. Спробуйте пізніше, додайте нові теми або редагуйте фільтри.",
            reply_markup=await kb.reply.menu.menu_keyboard(message.chat.id),
        )


@router.message(F.text == "Переглянути активні теми")
async def handle_active_topics(message: Message):
    user = await rq.get_user_by_id(message.chat.id)
    user_categories = list(dict.fromkeys(item.category for item in user.category_items))

    await message.answer(
        text=f"Ваші активні теми👇",
        reply_markup=await kb.inline.categories.inline_categories_to_delete(
            categories=user_categories
        ),
    )


@router.message(F.text == "Змінити теми")
async def handle_update_topics(message: Message):
    await message.answer(
        text="Оберіть категорії, які вас цікавлять👇",
        reply_markup=await kb.inline.categories.update_categories()
    )