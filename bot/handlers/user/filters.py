from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import bot.services as rq
import bot.keyboards as kb
from bot.core.config import settings
from bot.utils import texts

router = Router(name="user_filters")


class MinMaxCostState(StatesGroup):
    min_cost: int = State()
    max_cost: int = State()


class MaxBetsState(StatesGroup):
    max_bets: int = State()


class ExcludedTagsState(StatesGroup):
    excluded_tags: list = State()


@router.message(F.text == "Змінити фільтри")
async def update_filters(message: Message):
    await message.answer(
        text="Виберіть категорію для зміни фільтрів:",
        reply_markup=kb.reply.menu.filters_keyboard(),
    )


# ------- SET MIN/MAX COST FILTERS --------
@router.message(F.text == "Мін/Макс ціна проекту")
async def update_cost_filter(message: Message, state: FSMContext):
    user = await rq.users.get_user_by_id(message.chat.id)
    
    min_cost = user.filter_min_cost if user.filter_min_cost is not None else 0
    max_cost = user.filter_max_cost if user.filter_max_cost is not None else "Не встановлено"
    
    await message.answer(
        f"Поточні фільтри ціни:\nМінімальна ціна: {min_cost} грн\nМаксимальна ціна: {max_cost} грн\n\n"
        "Введіть мінімальну ціну або надішліть '-' для скасування."
    )
    await state.set_state(MinMaxCostState.min_cost)
    

@router.message(MinMaxCostState.min_cost)
async def set_min_cost(message: Message, state: FSMContext):
    min_cost = message.text.strip()
    if min_cost == "-":
        return await state.clear()

    if min_cost.isdigit():
        min_cost = int(min_cost)
        if min_cost < 0:
            return await message.answer("Ціна не може бути від'ємною")
    else:
        return await message.answer("Будь ласка, введіть лише число")

    await state.update_data(min_cost=min_cost)
    await state.set_state(MinMaxCostState.max_cost)
    await message.answer("Тепер напишіть максимальну ціну проекту або надішліть '-' для скасування:")


@router.message(MinMaxCostState.max_cost)
async def set_max_cost(message: Message, state: FSMContext):
    data = await state.get_data()
    min_cost = int(data.get("min_cost", 0))
    max_cost = message.text.strip()
    if max_cost == "-":
        max_cost = None
    else:
        if max_cost.isdigit():
            max_cost = int(max_cost)
            if max_cost < 0:
                return await message.answer("Ціна не може бути від'ємною")
        else:
            return await message.answer("Будь ласка, введіть лише число")


        if min_cost > max_cost:
            return await message.answer(
                "Максимальна ціна не може бути меншою за мінімальну"
            )

    await rq.users.set_min_max_cost(
        user_id=message.chat.id,
        min_cost=min_cost,
        max_cost=max_cost
    )

    await state.clear()
    await message.answer(
        text=f"Фільтри ціни встановлено:\nМінімальна ціна: {min_cost or "---"} грн\nМаксимальна ціна: {max_cost or "---"} грн",
        reply_markup=kb.reply.menu.filters_keyboard(),
    )


# ------- SET MAX BETS FILTER --------
@router.message(F.text == "Максимальна к-сть ставок")
async def update_max_bets_filter(message: Message, state: FSMContext):
    user = await rq.users.get_user_by_id(message.chat.id)
    max_bets = user.filter_max_bets if user.filter_max_bets is not None else "Не встановлено"
    await message.answer(
        f"Поточний фільтр максимальної кількості ставок:\nМаксимальна кількість ставок: {max_bets}\n\n"
        "Введіть нове значення або надішліть '-' для скасування."
    )
    await state.set_state(MaxBetsState.max_bets)


@router.message(MaxBetsState.max_bets)
async def set_max_bets(message: Message, state: FSMContext):
    max_bets = message.text.strip()
    if max_bets == "-":
        return await state.clear()

    if max_bets.isdigit():
        max_bets = int(max_bets)
        if max_bets < 0:
            return await message.answer("Кількість ставок не може бути від'ємною")
    else:
        return await message.answer("Будь ласка, введіть лише число")

    await rq.users.set_max_bets(user_id=message.chat.id, max_bets=max_bets)
    await state.clear()

    await message.answer(
        text=f"Фільтр максимальної кількості ставок встановлено:\nМаксимальна кількість ставок: {max_bets}",
        reply_markup=kb.reply.menu.filters_keyboard(),
    )


# -------- SET EXCLUDED WORDS FILTER --------
@router.message(F.text == "Чорний список слів")
async def update_blackist_filter(message: Message, state: FSMContext):
    user = await rq.users.get_user_by_id(message.chat.id)
    excluded_tags = ", ".join(user.excluded_tags) if user.excluded_tags else "Порожній"

    await message.answer(
        f"Поточний чорний список слів:\n{excluded_tags}\n\n"
        "Введіть нові слова через кому (наприклад: слово1, слово2, слово3), "
        "або надішліть '-' для скасування."
    )

    await state.set_state(ExcludedTagsState.excluded_tags)


@router.message(ExcludedTagsState.excluded_tags)
async def set_excluded_tags(message: Message, state: FSMContext):
    if message.text.strip() == "-":
        return await state.clear()
    
    words = [m.strip().lower() for m in message.text.strip().split(",")]
    
    await rq.users.set_excluded_words(
        user_id=message.chat.id,
        words=words
    )
    await message.answer(
        text=f"Слова успішно додані до чорного списку:\n{', '.join(words)}",
        reply_markup=kb.reply.menu.filters_keyboard(),
    )
    await state.clear()
    