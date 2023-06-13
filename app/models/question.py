from sqlalchemy import TIMESTAMP, Column, Integer, Text

from app.core.db import Base


class Question(Base):
    """Модель вопроса."""

    answer = Column(Text, nullable=False)
    question = Column(Text, unique=True, nullable=False)
    value = Column(Integer)
    airdate = Column(type_=TIMESTAMP(timezone=True))
    created_at = Column(type_=TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(type_=TIMESTAMP(timezone=True))
    category_id = Column(Integer)

    def __repr__(self):
        """Возвращает информацию по вопросу."""
        return f"<ID {self.id}> " f"{self.question} => " f"{self.answer}"
