from typing import List

from sqlalchemy import BigInteger, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from app.core.config import config


engine = create_async_engine(config.DATABSE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UserCategoryItem(Base):
    __tablename__ = "user_category_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_item_id: Mapped[int] = mapped_column(ForeignKey("category_items.id", ondelete="CASCADE"))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    filter_min_cost: Mapped[int] = mapped_column(default=0, nullable=False)
    filter_max_cost: Mapped[int] = mapped_column(default=0, nullable=False)
    filter_max_bets: Mapped[int] = mapped_column(default=0, nullable=False)
    excluded_words: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)

    category_items: Mapped[List["CategoryItem"]] = relationship(
        back_populates="users",
        secondary="user_category_items",
    )

    def __repr__(self):
        return f"<User id={self.id} chat_id={self.chat_id} is_superuser={self.is_superuser}, is_active={self.is_active}>"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    category_items: Mapped[List["CategoryItem"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"


class CategoryItem(Base):
    __tablename__ = "category_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="category_items")

    users: Mapped[List["User"]] = relationship(
        back_populates="category_items",
        secondary="user_category_items",
    )

    def __repr__(self):
        return f"<CategoryItem id={self.id} name={self.name} category_id={self.category_id}>"


async def create_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
