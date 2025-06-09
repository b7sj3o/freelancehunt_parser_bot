from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.session import async_session
from bot.db.models import User, CategoryItem
from bot.utils.db import get_user



async def get_user_by_id(user_id: int) -> User | None:
    async with async_session() as session:
        return await get_user(session, user_id)


async def create_user(user_id: int):
    async with async_session() as session:
        if not await get_user(session, user_id):
            session.add(User(user_id=user_id))
            await session.commit()


async def get_user_category_items(user_id: int, category_id: int) -> list[CategoryItem]:
    async with async_session() as session:
        user = await get_user(session, user_id)

        if not user:
            return []
        
        category_items = await session.scalars(
            select(CategoryItem)
            .where(CategoryItem.category_id == category_id)
            .where(CategoryItem.id.in_([item.id for item in user.category_items]))
            .options(selectinload(CategoryItem.category))
        )

        return category_items.all()



async def set_user_category_items(user_id: int, category_items: list[str]):
    async with async_session() as session:
        user = await get_user(session, user_id)

        if not user:
            return "Користувач не знайдений"

        user.category_items = []

        if category_items:
            items = await session.scalars(
                select(CategoryItem).where(CategoryItem.id.in_(category_items))
            )
            user.category_items.extend(items.all())
            await session.commit()
        
        return "Категорії користувача оновлено"


async def delete_user_category_item(user_id: int, category_item_id: int):
    async with async_session() as session:
        user = await get_user(session, user_id)

        if not user:
            return "Користувач не знайдений"

        item = next((item for item in user.category_items if item.id == category_item_id), None)

        if item is None:
            return "Підтема не знайдена"

        user.category_items.remove(item)
        await session.commit()
        await session.refresh(user)
        return "Підтему видалено"


async def set_user_superuser(user_id: int):
    async with async_session() as session:
        user = await get_user(session, user_id)
        if user:
            user.is_superuser = True 
            await session.commit()


async def is_superuser(user_id: int) -> bool:
    async with async_session() as session:
        user = await get_user(session, user_id)
        return user.is_superuser if user else False


async def set_min_max_cost(user_id: int, min_cost: int, max_cost: int|None):
    async with async_session() as session:
        user = await get_user(session, user_id)
        if not user:
            return "Користувач не знайдений"

        user.filter_min_cost = min_cost
        user.filter_max_cost = max_cost
        await session.commit()
        return "Мінімальна та максимальна ціни оновлені"
    

async def set_max_bets(user_id: int, max_bets: int):
    async with async_session() as session:
        user = await get_user(session, user_id)
        if not user:
            return "Користувач не знайдений"

        user.filter_max_bets = max_bets
        await session.commit()
        return "Максимальна кількість ставок оновлена"
    

async def set_excluded_words(user_id: int, words: list[str]):
    async with async_session() as session:
        user = await get_user(session, user_id)
        if not user:
            return "Користувач не знайдений"

        user.excluded_tags = words
        await session.commit()
        return "Виключені слова оновлено"


