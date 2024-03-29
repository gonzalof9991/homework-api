from typing import Optional

from pydantic import BaseModel, ConfigDict


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
    repeat: int | None = None  # 0 = no repeat, 1 = repeat every day, 2 = repeat every week, 3 = repeat every month
    repeated_days: int | None = None
    type: int = 0
    minutes_expected: int
    minutes_completed: Optional[int] = None
    minutes_total: Optional[int] = None
    alert_id: int
    expiration_date: str | None = None
    repeated_date: str | None = None
    deleted_at: str | None = None
    updated_at: str | None = None
    created_at: str | None = None


class TaskCreate(TaskBase):
    categories: list[int] = []
    pass


class Task(TaskBase):
    id: int
    history_id: int
    categories: list["CategoryByNameId"] = []

    model_config = ConfigDict(from_attributes=True)


class Category(CategoryBase):
    id: int
    tasks: list["Task"] = []

    model_config = ConfigDict(from_attributes=True)


class CategoryByNameId(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class HistoryBase(BaseModel):
    title: str
    description: str | None = None
    added_minutes: int | None = None


class HistoryCreate(HistoryBase):
    pass


class HistoryUpdate(HistoryBase):
    tasks: list[int] = []
    owner_id: Optional[int] = None


class History(HistoryBase):
    id: int
    tasks: list["Task"] = []
    owner_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


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
    histories: list["History"] = []
    model_config = ConfigDict(from_attributes=True)


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
    model_config = ConfigDict(from_attributes=True)


class TypeAlertBase(BaseModel):
    name: str
    description: str | None = None


class TypeAlertCreate(TypeAlertBase):
    pass


class TypeAlert(TypeAlertBase):
    id: int
    alerts: list["Alert"] = []
    model_config = ConfigDict(from_attributes=True)
