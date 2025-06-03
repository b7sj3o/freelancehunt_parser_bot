from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.db.crud.user as rq
import app.keyboards as kb
from app.core.config import config

router = Router(name="admin_manage_categories")

class CreateCategoryState(StatesGroup):
    name = State()


class CreateCategoryItemState(StatesGroup):
    category = State()
    name = State()


@router.message(Command("admin"))
async def admin_command(message: Message):
    if await rq.is_superuser(message.chat.id):
        await message.answer("Вітаємо, адмін!", reply_markup=kb.admin.admin_keyboard)
    else:
        password = message.text.strip().split(" ", 1)[1] if len(message.text.strip().split(" ")) > 1 else ""
        
        if password == config.ADMIN_PASSWORD:
            await rq.set_user_admin(message.chat.id)
            await message.answer("Ви успішно стали адміном!", reply_markup=kb.admin.admin_keyboard)


# -------------- СТВОРЕННЯ ТЕМИ ------------------
@router.message(F.text == "Створити тему")
async def create_category(message: Message, state: FSMContext):
    if not await rq.is_superuser(message.chat.id):
        return

    await state.set_state(CreateCategoryState.name)
    await message.answer("Введіть назву категорії:")

@router.message(CreateCategoryState.name)
async def create_category_name(message: Message, state: FSMContext):
    category_name = message.text.strip()
    if not category_name:
        await message.answer("Назва категорії не може бути порожньою.")
        return
    elif category_name == "-":
        await state.clear()
        return

    result = await rq.create_category(message.chat.id, category_name)
    await message.answer(result)
    await state.set_state(CreateCategoryState.name)


# -------------- СТВОРЕННЯ ПІДТЕМИ ------------------
@router.message(F.text == "Створити підтему")
async def create_category_item(message: Message, state: FSMContext):
    if not await rq.is_superuser(message.chat.id):
        return

    categories = await rq.get_categories()
    if not categories:
        await message.answer("Немає доступних категорій для створення підтеми.")
        return

    await state.set_state(CreateCategoryItemState.category)
    await message.answer(
        text="Оберіть тему для підтеми",
        reply_markup=await kb.categories.reply_categories_keyboard()
    )


@router.message(CreateCategoryItemState.category)
async def create_category_item_category(message: Message, state: FSMContext):
    category_name = message.text.strip()

    if not await rq.get_category_by_name(category_name):
        await message.answer("Категорія не знайдена.")
        return

    await state.update_data(category=category_name)
    await state.set_state(CreateCategoryItemState.name)
    await message.answer("Введіть назву підтеми:")


@router.message(CreateCategoryItemState.name)
async def create_category_item_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Назва підтеми не може бути порожньою.")
        return

    await state.update_data(name=name)
    data = await state.get_data()
    result = await rq.create_category_item(
        chat_id=message.chat.id,
        category_name=data["category"], 
        item_name=data["name"]
    )
    await message.answer(result)
    await state.clear()


@router.message(Command("create"))
async def create_random_category_items(message: Message):
    if not await rq.is_superuser(message.chat.id):
        return
    
    categories = await rq.get_categories()
    if not categories:
        await message.answer("Немає доступних категорій для створення підтеми.")
        return
    
    for category in categories:
        await rq.create_random_category_items(
            chat_id=message.chat.id, 
            category_name=category.name
        )