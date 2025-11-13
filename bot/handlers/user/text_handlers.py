import asyncio
import time
from typing import Any, List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

import bot.keyboards as kb
import bot.services.users as rq
from bot.filters.admin import AdminFilter
from bot.parser.freelancehunt import parse_data

router = Router(name="user_text_handlers")

VACANCIES_BATCH_SIZE = 5


def _serialize_project(project) -> dict[str, Any]:
    return {
        "title": project.title,
        "link": project.link,
        "description": project.description,
        "price": project.price,
        "tags": project.tags,
    }


def _build_more_button(next_offset: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Показати ще 5 вакансій",
                    callback_data=f"next_vacancy:{next_offset}",
                )
            ]
        ]
    )


async def _send_vacancy_batch(
    message: Message,
    projects: List[dict[str, Any]],
    start_index: int,
) -> tuple[int, bool]:
    end_index = min(start_index + VACANCIES_BATCH_SIZE, len(projects))
    batch = projects[start_index:end_index]

    for project in batch:
        tags = project.get("tags") or []
        tags_text = ", ".join(tags) if tags else "—"

        await message.answer(
            text=(
                f"Вакансія: {project.get('title')}\n"
                f"Ціна: {project.get('price')}грн\n"
                f"Опис: {project.get('description')}\n"
                f"Теги: {tags_text}"
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Перейти до вакансії",
                            url=project.get("link"),
                        )
                    ]
                ]
            ),
        )
        await asyncio.sleep(0.5)

    return end_index, end_index < len(projects)


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
async def handle_check_vacancies(message: Message, state: FSMContext):
    user = await rq.get_user_by_id(message.chat.id)

    links = list(dict.fromkeys(item.link for item in user.category_items))
    projects: List[dict[str, Any]] = []
    seen_links: set[str] = set()

    for link in links:
        parsed_projects = await parse_data(link, user)
        for project in parsed_projects:
            if project.link in seen_links:
                continue
            seen_links.add(project.link)
            projects.append(_serialize_project(project))

    if not projects:
        await message.answer(
            text="На жаль, ми не знайшли вакансій за вашими темами та фільтрами. Спробуйте пізніше, додайте нові теми або редагуйте фільтри.",
            reply_markup=await kb.reply.menu.menu_keyboard(message.chat.id),
        )
        await state.update_data(vacancies=[], vacancies_offset=0)
        return

    next_offset, has_more = await _send_vacancy_batch(message, projects, 0)

    if has_more:
        await state.update_data(vacancies=projects, vacancies_offset=next_offset)
        await message.answer(
            text="Ось! Це вакансії, які ми знайшли за вашими темами👆",
            reply_markup=_build_more_button(next_offset),
        )
    else:
        await state.update_data(vacancies=[], vacancies_offset=0)
        await message.answer("Ми показали всі знайдені вакансії 👆")


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


@router.callback_query(F.data.startswith("next_vacancy:"))
async def handle_next_vacancy(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    projects: List[dict[str, Any]] = data.get("vacancies", [])

    if not projects:
        await callback.answer("Список вакансій недоступний. Спробуйте оновити пошук.", show_alert=True)
        await callback.message.edit_text("Список вакансій недоступний. Спробуйте запустити пошук ще раз.")
        return

    offset_str = callback.data.split(":", 1)[1]
    try:
        start_index = int(offset_str)
    except ValueError:
        await callback.answer("Невірний запит", show_alert=True)
        return

    if start_index >= len(projects):
        await callback.answer("Більше вакансій немає")
        await callback.message.edit_text("Ми показали всі знайдені вакансії 👆")
        await state.update_data(vacancies=[], vacancies_offset=0)
        return

    next_offset, has_more = await _send_vacancy_batch(callback.message, projects, start_index)

    if has_more:
        await state.update_data(vacancies=projects, vacancies_offset=next_offset)
        await callback.message.edit_reply_markup(
            reply_markup=_build_more_button(next_offset)
        )
    else:
        await state.update_data(vacancies=[], vacancies_offset=0)
        await callback.message.edit_text("Ми показали всі знайдені вакансії 👆")

    await callback.answer()