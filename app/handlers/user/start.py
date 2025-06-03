from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.db.crud.user as rq
import app.keyboards as kb
from app.core.config import config
from app.utils import texts

router = Router(name="user_start")

class UserStartState(StatesGroup):
    main_menu = State()
    current_category = State()
    category_items = State()

@router.message(CommandStart())
async def start(message: Message):
    user = await rq.get_user_by_id(message.chat.id)

    if user:
        # if user is authenticated, but has no categories
        if not user.category_items:
            await message.answer(
                text=texts.start_text_no_categories.format(
                    first_name=message.from_user.first_name,
                ),
                reply_markup=await kb.categories.register_categories_keyboard()
            )
            return
        # if user is authenticated and has categories
        await message.answer(
            text=texts.start_text_auth.format(
                first_name=message.from_user.first_name,
            ),
            reply_markup=await kb.user.base_reply_keyboard(message.chat.id)
        )
    else:
        # if user is not authenticated
        await rq.create_user(message.chat.id)
        await message.answer(
            text=texts.start_text_unauth.format(
                first_name=message.from_user.first_name,
            ),
            reply_markup=await kb.categories.register_categories_keyboard()
        )


@router.callback_query(F.data.startswith("register_category:"))
async def register_category_callback(callback: CallbackQuery, state: FSMContext):
    category_name = callback.data.split(":")[1]
    category_items = await rq.get_category_items(category_name=category_name)
    
    selected_items = await state.get_data()
    selected_items = selected_items.get("selected_items", [])

    category_items = [(item, item.name in selected_items) for item in category_items]
    await callback.message.edit_text(
        text=texts.register_category_items_text.format(
            category_name=category_name
        ),
        reply_markup=await kb.categories.register_category_items_keyboard(category_items)
    )
    await state.update_data(current_category=category_name)
    await state.set_state(UserStartState.category_items)
    await callback.answer()


@router.callback_query(F.data == "submit_register")
async def submit_register_callback(callback: CallbackQuery, state: FSMContext):
    selected_items = await state.get_data()
    await rq.set_user_category_items(callback.from_user.id, selected_items.get("selected_items", []))
    await callback.message.answer(
        text=texts.register_success_text,
        reply_markup=await kb.user.base_reply_keyboard(callback.from_user.id)
    )
    await callback.message.delete()
    await state.clear()
    await callback.answer()


@router.callback_query(UserStartState.category_items)
async def register_category_items_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data == "go_back_register":
        selected_items = await state.get_data()
        selected_items_list = selected_items.get("selected_items", [])
        

        await callback.message.edit_text(
            text=texts.register_main_text.format(
                selected_items="\n- ".join(str(item) for item in selected_items_list) if selected_items_list else "Немає обраних категорій"
            ),
            reply_markup=await kb.categories.register_categories_keyboard()
        )
        await state.set_state(UserStartState.main_menu)
        await callback.answer()
        return

    item_name = callback.data.split(":")[1]
    selected_items = await state.get_data()
    selected_items_list = selected_items.get("selected_items", [])
    
    if item_name in selected_items_list:
        selected_items_list.remove(item_name)
    else:
        selected_items_list.append(item_name)

    await state.update_data(selected_items=selected_items_list)

    category_items = await rq.get_category_items(category_name=selected_items.get("current_category", []))
    category_items = [(item, item.name in selected_items_list) for item in category_items]
    
    await callback.message.edit_text(
        text=texts.register_category_items_text.format(
            category_name=selected_items.get("current_category", "Unknown Category")
        ),
        reply_markup=await kb.categories.register_category_items_keyboard(category_items=category_items)
    )
    await callback.answer()
    
    