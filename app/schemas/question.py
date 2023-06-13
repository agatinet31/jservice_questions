from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class QuestionBase(BaseModel):
    """Класс схемы вопроса."""

    id: int
    answer: str
    question: str
    value: Optional[int] = None
    airdate: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    category_id: Optional[int] = None


class ManyQuestionParseShema(BaseModel):
    """Класс схемы с распарсенной информацией по списку вопросов."""

    results: List[QuestionBase]


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    pass


class QuestionDBShema(QuestionBase):
    """Класс схемы для выдачи информации по вопросу из БД."""

    class Config:
        orm_mode = True
