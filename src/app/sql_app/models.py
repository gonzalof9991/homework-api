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
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    histories = relationship("History", back_populates="owner")


class History(Generic):
    __tablename__ = "histories"
    title = Column(String, index=True)
    description = Column(String, index=True)
    tasks = relationship("Task", back_populates="history")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="histories")


association_table = Table(
    "association",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
)


class Task(Generic):
    __tablename__ = "tasks"
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True, default=0)  # 0 = low, 1 = medium, 2 = high
    defeated = Column(Integer, index=True, default=0)  # 0 = not defeated, 1 = defeated
    type = Column(Integer, index=True, default=0)  # 0 = new, 1 = active , 2 = closed
    minutes_expected = Column(Integer, index=True)
    minutes_completed = Column(Integer, index=True, default=0)
    expiration_date = Column(String, index=True)
    history_id = Column(Integer, ForeignKey("histories.id"))
    history = relationship("History", back_populates="tasks")
    categories: Mapped[List["Category"]] = relationship(secondary=association_table, back_populates="tasks")
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    alert = relationship("Alert", back_populates="tasks")


class Category(Generic):
    __tablename__ = "categories"
    name = Column(String, index=True)
    description = Column(String, index=True)
    tasks: Mapped[List["Task"]] = relationship(secondary=association_table, back_populates="categories")


class Alert(Generic):
    __tablename__ = "alerts"
    name = Column(String, index=True)
    description = Column(String, index=True)
    period = Column(Integer, index=True)  # 0 = daily, 1 = weekly, 2 = monthly
    hour = Column(Integer, index=True)  # 0-23
    minute = Column(Integer, index=True)  # 0-59
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="alert")
    type_alert_id = Column(Integer, ForeignKey("type_alerts.id"))
    type_alert = relationship("TypeAlert", back_populates="alerts")


class TypeAlert(Generic):
    __tablename__ = "type_alerts"
    name = Column(String, index=True)
    description = Column(String, index=True)
    alerts: Mapped[List["Alert"]] = relationship("Alert", back_populates="type_alert")
