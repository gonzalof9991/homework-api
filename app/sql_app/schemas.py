from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    task_id: int

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    owner_id: int
    categories: list[Category] = []

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
