from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, CategoryItem


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.scalar(
        select(User)
        .where(User.user_id == user_id)
        .options(
            selectinload(User.category_items).selectinload(CategoryItem.category)
        )
    )