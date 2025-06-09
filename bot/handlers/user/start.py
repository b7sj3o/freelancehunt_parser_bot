from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import bot.services as rq
import bot.keyboards as kb
from bot.core.config import settings
from bot.utils import texts

router = Router(name="user_start")

@router.message(CommandStart())
async def start(message: Message):
    user = await rq.users.get_user_by_id(message.chat.id)

    if user:
        # if user is authenticated, but has no categories
        if not user.category_items:
            await message.answer(
                text=texts.start_text_no_categories.format(
                    first_name=message.from_user.first_name,
                ),
                reply_markup=await kb.inline.categories.update_categories()
            )
            return
        # if user is authenticated and has categories
        await message.answer(
            text=texts.start_text_auth.format(
                first_name=message.from_user.first_name,
            ),
            reply_markup=await kb.reply.menu.menu_keyboard(message.chat.id)
        )
    else:
        # if user is not authenticated
        await rq.users.create_user(message.chat.id)
        await message.answer(
            text=texts.start_text_unauth.format(
                first_name=message.from_user.first_name,
            ),
            reply_markup=await kb.inline.categories.update_categories()
        )


 
    