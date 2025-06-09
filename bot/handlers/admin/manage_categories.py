from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import bot.services as rq
import bot.keyboards as kb
from bot.filters.admin import AdminFilter
from bot.core.config import settings

router = Router(name="admin_manage_categories")

class CreateCategoryState(StatesGroup):
    name = State()


class CreateCategoryItemState(StatesGroup):
    category = State()
    name = State()


# @router.message(Command("admin"))
# async def admin_command(message: Message):
#     if await rq.users.is_superuser(message.chat.id):
#         await message.answer("Вітаємо, адмін!", reply_markup=kb.reply.menu.admin_keyboard())
#     else:
#         password = message.text.strip().split(" ", 1)[1] if len(message.text.strip().split(" ")) > 1 else ""
        
#         if password == settings.ADMIN_PASSWORD:
#             await rq.users.set_user_admin(message.chat.id)
#             await message.answer("Ви успішно стали адміном!", reply_markup=kb.reply.menu.admin_keyboard())


# # -------------- СТВОРЕННЯ ТЕМИ ------------------
# @router.message(F.text == "Створити тему", AdminFilter())
# async def create_category(message: Message, state: FSMContext):
#     await state.set_state(CreateCategoryState.name)
#     await message.answer("Введіть назву категорії:\n(або надішліть '-' для скасування)")


# @router.message(CreateCategoryState.name, AdminFilter())
# async def create_category_name(message: Message, state: FSMContext):
#     category_name = message.text.strip()
#     if not category_name:
#         await message.answer("Назва категорії не може бути порожньою.")
#         return
#     elif category_name == "-":
#         await state.clear()
#         return

#     result = await rq.categories.create_category(message.chat.id, category_name)
#     await message.answer(result)
#     await state.set_state(CreateCategoryState.name)


# # -------------- СТВОРЕННЯ ПІДТЕМИ ------------------
# @router.message(F.text == "Створити підтему", AdminFilter())
# async def create_category_item(message: Message, state: FSMContext):
#     categories = await rq.categories.get_categories()

#     if not categories:
#         await message.answer("Немає доступних категорій для створення підтеми.")
#         return

#     await state.set_state(CreateCategoryItemState.category)
#     await message.answer(
#         text="Оберіть тему для підтеми",
#         reply_markup=await kb.reply.categories.reply_categories_keyboard()
#     )


# @router.message(CreateCategoryItemState.category, AdminFilter())
# async def create_category_item_category(message: Message, state: FSMContext):
#     category_name = message.text.strip()

#     if not await rq.categories.get_category(name=category_name):
#         await message.answer("Категорія не знайдена.")
#         return

#     await state.update_data(category=category_name)
#     await state.set_state(CreateCategoryItemState.name)
#     await message.answer("Введіть назву підтеми:")


# @router.message(CreateCategoryItemState.name, AdminFilter())
# async def create_category_item_name(message: Message, state: FSMContext):
#     name = message.text.strip()
#     if not name:
#         await message.answer("Назва підтеми не може бути порожньою.")
#         return

#     await state.update_data(name=name)
#     data = await state.get_data()
#     result = await rq.categories.create_category_item(
#         user_id=message.chat.id,
#         category_name=data["category"], 
#         item_name=data["name"]
#     )
#     await message.answer(result)
#     await state.clear()
