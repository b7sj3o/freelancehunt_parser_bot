from typing import Any, Dict, List

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import bot.services as rq
import bot.keyboards as kb
from bot.utils import texts

router = Router(name="user_manage_data")


def _normalize_selected_items(raw_items: Any) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []

    if not isinstance(raw_items, list):
        return normalized

    for item in raw_items:
        if isinstance(item, dict):
            item_id = item.get("id")
            if item_id is None:
                continue
            try:
                item_id = int(item_id)
            except (TypeError, ValueError):
                continue
            category_id = item.get("category_id")
            if category_id is not None:
                try:
                    category_id = int(category_id)
                except (TypeError, ValueError):
                    category_id = None
            normalized.append({
                "id": item_id,
                "name": item.get("name", ""),
                "category_id": category_id,
            })
        else:
            try:
                item_id = int(item)
            except (TypeError, ValueError):
                continue
            normalized.append({"id": item_id, "name": "", "category_id": None})

    return normalized


def _format_selected_items(selected_items: List[Dict[str, Any]]) -> str:
    selected_names = [item["name"] or str(item["id"]) for item in selected_items]

    if not selected_names:
        return "Немає обраних категорій"

    return "- " + "\n- ".join(selected_names)


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
    data = await state.get_data()
    selected_items = _normalize_selected_items(data.get("selected_items", []))

    user_category_items_map: Dict[int, Any] = {}
    needs_user_items = not selected_items or any(
        item.get("category_id") is None or not item.get("name") for item in selected_items
    )
    if needs_user_items:
        user = await rq.users.get_user_by_id(callback.from_user.id)
        if user:
            user_category_items_map = {item.id: item for item in user.category_items}
            if not selected_items:
                selected_items = [
                    {
                        "id": item.id,
                        "name": item.name,
                        "category_id": item.category_id,
                    }
                    for item in user.category_items
                ]
            else:
                for selected in selected_items:
                    category_item = user_category_items_map.get(selected.get("id"))
                    if category_item is None:
                        continue
                    if not selected.get("name"):
                        selected["name"] = category_item.name
                    selected["category_id"] = category_item.category_id
    selected_ids = {item["id"] for item in selected_items}

    category_items_map = {item.id: item for item in category_items}
    for selected in selected_items:
        category_item = category_items_map.get(selected.get("id"))
        if category_item is None and user_category_items_map:
            category_item = user_category_items_map.get(selected.get("id"))
        if category_item is None:
            continue
        if not selected.get("name"):
            selected["name"] = getattr(category_item, "name", "")
        selected["category_id"] = getattr(category_item, "category_id", None)

    category_items = [(item, item.id in selected_ids) for item in category_items]
    await callback.message.edit_text(
        text=texts.register_category_items_text.format(
            category_name=category.name
        ),
        reply_markup=await kb.inline.categories.update_category_items(category_items)
    )
    await state.update_data(
        current_category={"id": category.id, "name": category.name},
        selected_items=selected_items
    )
    await state.set_state(UserStartState.category_items)
    await callback.answer()


@router.callback_query(F.data == "submit_update_categories")
async def submit_register_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_items = _normalize_selected_items(data.get("selected_items", []))
    selected_item_ids = [item["id"] for item in selected_items]

    await rq.users.set_user_category_items(callback.from_user.id, selected_item_ids)
    await callback.message.answer(
        text=texts.register_success_text,
        reply_markup=await kb.reply.menu.menu_keyboard(callback.from_user.id)
    )
    await callback.message.delete()
    await state.clear()
    await callback.answer()


@router.callback_query(UserStartState.category_items)
async def register_category_items_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_items = _normalize_selected_items(data.get("selected_items", []))
    current_category = data.get("current_category", {})

    if callback.data == "submit_category_items":
        await callback.message.edit_text(
            text=texts.register_main_text.format(
                selected_items=_format_selected_items(selected_items)
            ),
            reply_markup=await kb.inline.categories.update_categories(selected_items)
        )
        await state.set_state(UserStartState.main_menu)
        await state.update_data(selected_items=selected_items)
        await callback.answer()
        return

    item_id = int(callback.data.split(":")[1])
    category_id = current_category.get("id") if isinstance(current_category, dict) else None
    category_name = current_category.get("name") if isinstance(current_category, dict) else current_category

    if category_id is None and not category_name:
        await callback.answer("Категорія не визначена", show_alert=True)
        return

    category_items = await rq.categories.get_category_items(
        category_id=category_id,
        category_name=None if category_id else category_name
    )
    category_items_map = {item.id: item for item in category_items}

    selected_ids = {item["id"] for item in selected_items}

    if item_id in selected_ids:
        selected_items = [item for item in selected_items if item["id"] != item_id]
    else:
        category_item = category_items_map.get(item_id)
        if category_item is None:
            await callback.answer("Підтема не знайдена", show_alert=True)
            return
        selected_items.append({
            "id": item_id,
            "name": category_item.name,
            "category_id": category_item.category_id,
        })

    selected_ids = {item["id"] for item in selected_items}

    category_items = [(item, item.id in selected_ids) for item in category_items]

    category_name_for_text = (
        current_category.get("name")
        if isinstance(current_category, dict)
        else current_category
    ) or "Unknown Category"

    await callback.message.edit_text(
        text=texts.register_category_items_text.format(
            category_name=category_name_for_text
        ),
        reply_markup=await kb.inline.categories.update_category_items(category_items=category_items)
    )
    await state.update_data(selected_items=selected_items)
    await callback.answer()