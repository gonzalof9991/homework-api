from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    priority: int = 0  # 0 = low, 1 = medium, 2 = high
    defeated: int = 0  # 0 = not defeated, 1 = defeated
    minutes_expected: int
    minutes_completed: Optional[int] = None


class TaskCreate(TaskBase):
    categories: list[int] = []
    pass


class Task(TaskBase):
    id: int
    owner_id: int
    categories: list[CategoryBase] = []

    class Config:
        from_attributes = True


class Category(CategoryBase):
    id: int
    tasks: list["Task"] = []

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tasks: list[Task] = []

    class Config:
        from_attributes = True
