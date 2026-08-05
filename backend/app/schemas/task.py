from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    is_complete: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    owner_id: int
    is_complete: bool

    class Config:
        from_attributes = True