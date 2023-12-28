from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Generic(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    created_at = Column(String, index=True, default="now()")
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


class Task(Generic):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
    categories = relationship("Category", back_populates="task")


class Category(Generic):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="categories")
