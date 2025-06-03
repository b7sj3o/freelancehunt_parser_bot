from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder

import app.db.crud.user as rq
from app.db.models import CategoryItem

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Створити тему"),
            KeyboardButton(text="Створити підтему"),
        ],
        [
            KeyboardButton(text="На головну"),
        ],
    ],
    resize_keyboard=True,
)