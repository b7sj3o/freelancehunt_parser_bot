from typing import List

from sqlalchemy import BigInteger, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from bot.db.session import engine, Base


class UserCategoryItem(Base):
    __tablename__ = "user_category_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_item_id: Mapped[int] = mapped_column(ForeignKey("category_items.id", ondelete="CASCADE"))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)

    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    filter_min_cost: Mapped[int] = mapped_column(nullable=True)
    filter_max_cost: Mapped[int] = mapped_column(nullable=True)
    filter_max_bets: Mapped[int] = mapped_column(nullable=True)
    excluded_tags: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)

    category_items: Mapped[List["CategoryItem"]] = relationship(
        back_populates="users",
        secondary="user_category_items",
    )

    def __str__(self):
        return f"User(id={self.id}, user_id={self.user_id}, is_superuser={self.is_superuser}, is_active={self.is_active})"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    category_items: Mapped[List["CategoryItem"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"Category(id={self.id}, name={self.name})"


class CategoryItem(Base):
    __tablename__ = "category_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="category_items")

    link: Mapped[str] = mapped_column(nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship(
        back_populates="category_items",
        secondary="user_category_items",
    )

    def __str__(self):
        return f"CategoryItem(id={self.id}, name={self.name}, category_id={self.category_id})"


async def create_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
