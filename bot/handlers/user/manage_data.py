from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import bot.services as rq
import bot.keyboards as kb
from bot.utils import texts

router = Router(name="user_manage_data")


# ----------- delete category item ------------
class UserDeleteState(StatesGroup):
    current_category = State()

@router.callback_query(F.data.startswith("delete_category:"))
async def delete_category_callback(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split(":")[1])
    category_items = await rq.users.get_user_category_items(
        user_id=callback.message.chat.id,
        category_id=category_id
    )

    await callback.message.edit_text(
        text="Оберіть підтему, яку бажаєте видалити👇",
        reply_markup=await kb.inline.categories.inline_category_items_delete(category_items)
    )
    await state.update_data(current_category=category_id)
    await state.set_state(UserDeleteState.current_category)


@router.callback_query(UserDeleteState.current_category and F.data.startswith("delete_category_item:"))
async def delete_category_item_callback(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split(":")[1])
    data = await state.get_data()
    category_id = data.get("current_category")
    result = await rq.users.delete_user_category_item(callback.message.chat.id, item_id)
    
    category_items = await rq.users.get_user_category_items(
        user_id=callback.message.chat.id,
        category_id=category_id
    )

    if len(category_items) == 0:
        await callback.message.edit_text(
            text="Більше не залишилось активних тем😊",
            reply_markup=kb.reply.menu.menu_keyboard(callback.message.chat.id)
        )
        return

    await callback.message.edit_text(
        text=f'{result}\nВаші активні теми👇',
        reply_markup=await kb.inline.categories.inline_category_items_delete(category_items)
    )
   

@router.callback_query(F.data == "back_to_categories")
async def back_to_categories_callback(callback: CallbackQuery, state: FSMContext):
    user = await rq.users.get_user_by_id(callback.message.chat.id)
    user_categories = list(dict.fromkeys(item.category for item in user.category_items))

    await callback.message.edit_text(
        text=f"Ваші активні теми👇",
        reply_markup=await kb.inline.categories.inline_categories_to_delete(
            categories=user_categories
        ),
    )
    await state.clear()

# ----------- update active categories ------------
class UserStartState(StatesGroup):
    main_menu = State()
    current_category = State()
    category_items = State()


@router.callback_query(F.data.startswith("update_category:"))
async def register_category_callback(callback: CallbackQuery, state: FSMContext):
    # todo add check if there is a category
    category = await rq.categories.get_category(id=int(callback.data.split(":")[1]))

    category_items = await rq.categories.get_category_items(category_id=category.id)
    
    selected_items = await state.get_data()
    selected_items = selected_items.get("selected_items", [])

    category_items = [(item, item.name in selected_items) for item in category_items]
    await callback.message.edit_text(
        text=texts.register_category_items_text.format(
            category_name=category.name
        ),
        reply_markup=await kb.inline.categories.update_category_items(category_items)
    )
    await state.update_data(current_category=category.name)
    await state.set_state(UserStartState.category_items)
    await callback.answer()


@router.callback_query(F.data == "submit_update_categories")
async def submit_register_callback(callback: CallbackQuery, state: FSMContext):
    selected_items = await state.get_data()
    await rq.users.set_user_category_items(callback.from_user.id, selected_items.get("selected_items", []))
    await callback.message.answer(
        text=texts.register_success_text,
        reply_markup=await kb.reply.menu.menu_keyboard(callback.from_user.id)
    )
    await callback.message.delete()
    await state.clear()
    await callback.answer()


@router.callback_query(UserStartState.category_items)
async def register_category_items_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data == "submit_category_items":
        selected_items = await state.get_data()
        selected_items_list = selected_items.get("selected_items", [])
        

        await callback.message.edit_text(
            text=texts.register_main_text.format(
                selected_items="-"+"\n- ".join(str(item) for item in selected_items_list) if selected_items_list else "Немає обраних категорій"
            ),
            reply_markup=await kb.inline.categories.update_categories()
        )
        await state.set_state(UserStartState.main_menu)
        await callback.answer()
        return

    item_id = int(callback.data.split(":")[1])
    selected_items = await state.get_data()
    selected_items_list: list = selected_items.get("selected_items", [])
    
    if item_id in selected_items_list:
        selected_items_list.remove(item_id)
    else:
        selected_items_list.append(item_id)

    await state.update_data(selected_items=selected_items_list)

    category_items = await rq.categories.get_category_items(category_name=selected_items.get("current_category", []))
    category_items = [(item, item.id in selected_items_list) for item in category_items]
    
    await callback.message.edit_text(
        text=texts.register_category_items_text.format(
            category_name=selected_items.get("current_category", "Unknown Category")
        ),
        reply_markup=await kb.inline.categories.update_category_items(category_items=category_items)
    )
    await callback.answer()
   