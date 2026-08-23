from pydantic import BaseModel, Field
from typing import Optional, Literal


class MessageIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class ClassificationOut(BaseModel):
    category: Literal["sales", "support", "billing", "complaint", "general"]
    priority: Literal["low", "medium", "high"]
    summary: str = Field(..., min_length=1)
    suggested_action: str = Field(..., min_length=1)


class ExtractionOut(BaseModel):
    requester_name: Optional[str] = None
    request_type: Literal["new_task", "update", "question"]
    urgency: Literal["low", "medium", "high"]
    task_title_guess: Optional[str] = None