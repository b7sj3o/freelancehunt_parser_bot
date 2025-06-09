from sqlalchemy import select

from bot.db.session import async_session
from bot.db.models import Category, CategoryItem


async def create_category(user_id: int, name: str):
    async with async_session() as session:
        category = await session.scalar(select(Category).where(Category.name == name))

        if not category:
            category = Category(name=name)
            session.add(category)
            await session.commit()
            return "Категорія створена"
        else:
            return "Категорія вже існує"


async def create_category_item(user_id: int, category_name: str, item_name: str):
    async with async_session() as session:
        category = await session.scalar(
            select(Category).where(Category.name == category_name)
        )

        if not category:
            return "Категорія не знайдена"

        item = await session.scalar(
            select(CategoryItem).where(
                CategoryItem.name == item_name, CategoryItem.category_id == category.id
            )
        )

        if not item:
            item = CategoryItem(name=item_name, category=category)
            session.add(item)
            await session.commit()
            return "Підкатегорію створено"
        else:
            return "Підкатегорія вже існує"


async def get_categories(with_children: bool = False) -> list[Category]:
    """
    Fetch all categories from the database.
    If `with_children` is True, it will fetch only categories that have children.
    """
    async with async_session() as session:
        if with_children:
            return (
                await session.scalars(
                    select(Category).where(Category.category_items.any())
                )
            ).all()
        return (await session.scalars(select(Category))).all()


async def get_category(**filters) -> Category | None:
    async with async_session() as session:
        return await session.scalar(select(Category).filter_by(**filters))


async def get_category_items(category_name: str = None, category_id: int = None):
    async with async_session() as session:
        category = None
        if category_id:
            category = await session.scalar(
                select(Category).where(Category.id == category_id)
            )
        elif category_name:
            category = await session.scalar(
                select(Category).where(Category.name == category_name)
            )

        if category is None:
            return []

        return (
            await session.scalars(
                select(CategoryItem).where(CategoryItem.category_id == category.id)
            )
        ).all()


