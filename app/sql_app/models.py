from msilib import Table
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


class Generic(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)
    deleted_at = Column(String, index=True)


class User(Generic):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tasks = relationship("Task", back_populates="owner")


association_table = Table(
    "association",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
)


class Task(Generic):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True, default=0)  # 0 = low, 1 = medium, 2 = high
    defeated = Column(Integer, index=True, default=0)  # 0 = not defeated, 1 = defeated
    minutes_expected = Column(Integer, index=True)
    minutes_completed = Column(Integer, index=True, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
    categories: Mapped[List["Category"]] = relationship(secondary=association_table, back_populates="tasks")


class Category(Generic):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    tasks: Mapped[List["Task"]] = relationship(secondary=association_table, back_populates="categories")
