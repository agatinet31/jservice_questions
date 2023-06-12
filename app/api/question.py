from fastapi import Depends, HTTPException, status
from fastapi.logger import logger

from app.core.db import get_async_session
from app.crud import question_crud
from app.exceptions import (
    QuestionIncorrectStructureError,
    QuestionRequestError,
)
from app.models import Question
from app.schemas import ManyQuestionParseShema
from app.services.parse_jservice import parse_jservice_random_questions
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


async def get_from_db_question_by_id(
    question_id: int, session: AsyncSession = Depends(get_async_session)
) -> Question:
    """Возвращает информацию по вопросу для валидного идентификатора."""
    try:
        return await question_crud.get(session, question_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вопрос с идентификатором {question_id} не найден в БД!",
        )
    except SQLAlchemyError:
        error_message = "Внутреняя ошибка сервиса при получении информации по товару из БД!"
        logger.exception(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )


async def get_unique_jservice_questions(
    questions_num: int, session: AsyncSession = Depends(get_async_session)
) -> ManyQuestionParseShema:
    """
    Возвращает распарсиные данные
    для questions_num вопросов с хостинга https://jservice.io/.
    """
    try:
        return await parse_jservice_random_questions(questions_num)
    except (QuestionRequestError, QuestionIncorrectStructureError):
        error_message = "Внутреняя ошибка сервиса при парсинге вопросов!"
        logger.exception(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )
