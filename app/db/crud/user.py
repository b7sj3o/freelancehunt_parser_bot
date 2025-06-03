from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import async_session
from app.db.models import User, Category, CategoryItem
import random
import string

# -------------- UTILS ----------------
async def get_user(session: AsyncSession, chat_id: int) -> User | None:
    return await session.scalar(select(User)
                                .where(User.chat_id == chat_id)
                                .options(selectinload(User.category_items))
                                )


# -------------- CRUD -----------------
async def get_user_by_id(chat_id: int) -> User | None:
    async with async_session() as session:
        return await session.scalar(select(User)
                                    .where(User.chat_id == chat_id)
                                    .options(selectinload(User.category_items))
                                    )


async def create_user(chat_id: int):
    async with async_session() as session:
        if not await get_user(session, chat_id):
            session.add(User(chat_id=chat_id))
            await session.commit()


async def set_user_category_items(chat_id: int, category_items: list[str]):
    async with async_session() as session:
        user = await get_user(session, chat_id)

        if not user:
            return "Користувач не знайдений"

        user.category_items = []

        if category_items:
            items = await session.scalars(
                select(CategoryItem).where(CategoryItem.name.in_(category_items))
            )
            user.category_items.extend(items.all())
            await session.commit()
        
        return "Категорії користувача оновлено"


async def is_superuser(chat_id: int) -> bool:
    async with async_session() as session:
        user = await get_user(session, chat_id)
        return user.is_superuser if user else False
    

async def set_user_admin(chat_id: int):
    async with async_session() as session:
        user = await get_user(session, chat_id)
        if user:
            user.is_superuser = True 
            await session.commit()


def admin_required(func):
    async def wrapper(chat_id: int, *args, **kwargs):
        if await is_superuser(chat_id):
            return await func(chat_id, *args, **kwargs)
        return "У вас немає прав"
    return wrapper


@admin_required
async def create_category(chat_id: int, name: str):
    async with async_session() as session:
        category = await session.scalar(select(Category).where(Category.name == name))

        if not category:
            category = Category(name=name)
            session.add(category)
            await session.commit()
            return "Категорія створена"
        else:
            return "Категорія вже існує"

@admin_required
async def create_category_item(chat_id: int, category_name: str, item_name: str):
    async with async_session() as session:
        category = await session.scalar(select(Category).where(Category.name == category_name))

        if not category:
            return "Категорія не знайдена"

        item = await session.scalar(select(CategoryItem).where(
            CategoryItem.name == item_name, CategoryItem.category_id == category.id
        ))

        if not item:
            item = CategoryItem(name=item_name, category=category)
            session.add(item)
            await session.commit()
            return "Підкатегорію створено"
        else:
            return "Підкатегорія вже існує"
        

async def get_categories():
    async with async_session() as session:
        return (await session.scalars(select(Category))).all()
    

async def get_category_by_name(name: str) -> Category | None:
    async with async_session() as session:
        return await session.scalar(select(Category).where(Category.name == name))
    

async def get_category_items(category_name: str = None, category_id: int = None):
    async with async_session() as session:
        category = None
        if category_id:
            category = await session.scalar(select(Category).where(Category.id == category_id))
        elif category_name:
            category = await session.scalar(select(Category).where(Category.name == category_name))
        
        if category is None:
            return []

        return (await session.scalars(select(CategoryItem).where(CategoryItem.category_id == category.id))).all()
    

@admin_required
async def create_random_category_items(chat_id: int, category_name: str, count: int = 5, length: int = 8):
    """
    Create random category items for a given category
    
    Args:
        chat_id: The ID of the user (not used in this function, but kept for consistency)
        category_name: The category name to add items to
        count: Number of random items to create (default: 5)
        length: Length of random item names (default: 8)
    
    Returns:
        str: Status message
    """
    async with async_session() as session:
        category = await session.scalar(select(Category).where(Category.name == category_name))
        
        if not category:
            return "Категорія не знайдена"
        
        created_count = 0
        for _ in range(count):
            # Generate random item name
            random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            
            # Check if item already exists
            existing_item = await session.scalar(select(CategoryItem).where(
                CategoryItem.name == random_name, 
                CategoryItem.category_id == category.id
            ))
            
            if not existing_item:
                item = CategoryItem(name=random_name, category=category)
                session.add(item)
                created_count += 1
        
        if created_count > 0:
            await session.commit()
            return f"Створено {created_count} випадкових підкатегорій"
        else:
            return "Не вдалося створити жодної підкатегорії"
            

