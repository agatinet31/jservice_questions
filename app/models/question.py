from app.core.db import Base
from sqlalchemy import Column, DateTime, Integer, String


class Question(Base):
    """Модель вопроса."""

    answer = Column(String(250), nullable=False)
    question = Column(String(250), unique=True, nullable=False)
    value = Column(Integer)
    airdate = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    category_id = Column(Integer)

    def __repr__(self):
        """Возвращает информацию по вопросу."""
        return f"<ID {self.id}> " f"{self.question} => " f"{self.answer}"
