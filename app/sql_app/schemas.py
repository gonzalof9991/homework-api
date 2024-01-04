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
    alert_id: int
    expiration_date: str | None = None


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


# Alert and TypeAlert


class AlertBase(BaseModel):
    name: str
    description: str | None = None
    period: int
    hour: int
    minute: int
    type_alert_id: Optional[int] = None


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: int
    tasks: list["Task"] = []

    class Config:
        from_attributes = True


class TypeAlertBase(BaseModel):
    name: str
    description: str | None = None


class TypeAlertCreate(TypeAlertBase):
    pass


class TypeAlert(TypeAlertBase):
    id: int
    alerts: list["Alert"] = []

    class Config:
        from_attributes = True
