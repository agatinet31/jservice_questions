from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class QuestionBase(BaseModel):
    """Класс схемы вопроса."""
    id: int
    answer: str
    question: str
    value: int
    airdate: datetime
    created_at: datetime
    updated_at: datetime
    category_id: int


class ManyQuestionParseShema(QuestionBase):
    """Класс схемы с распарсенной информацией по списку вопросов."""
    pass


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    pass


class QuestionDBShema(QuestionBase):
    """Класс схемы для выдачи информации по вопросу из БД."""

    class Config:
        orm_mode = True
