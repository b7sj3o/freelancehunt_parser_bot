from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.db.crud.user as rq
import app.keyboards as kb
from app.core.config import config

router = Router(name="user_text_handlers")

@router.message(F.text)
async def handle_text(message: Message):
    await message.delete()
    if message.text == "На головну":
        await message.answer("Повертаємось на головну", reply_markup=await kb.user.base_reply_keyboard(message.chat.id))
        return
    elif message.text == "Адмін-панель":
        if await rq.is_superuser(message.chat.id):
            await message.answer("Вітаємо, адмін!", reply_markup=kb.admin.admin_keyboard)
        return

    category_items = await rq.get_category_items(category_name=message.text.strip())

    if not category_items:
        await message.answer("Немає підкатегорій")
        return
    
    await message.answer("Ось підкатегорії", reply_markup=await kb.categories.reply_category_items_keyboard(category_items))
