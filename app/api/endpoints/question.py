from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.logger import logger

from app.api.depends import get_from_db_question_by_id, get_jservice_questions
from app.core.db import get_async_session
from app.crud.question import question_crud
from app.models import Question
from app.schemas import QuestionDBShema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    "/", response_model=List[QuestionDBShema], response_model_exclude_none=True
)
async def get_all_questions(
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех уникальных вопросов."""
    try:
        return await question_crud.get_multi(session)
    except SQLAlchemyError:
        error_message = (
            "Внутреняя ошибка сервиса при получении списка вопросов!"
        )
        logger.exception(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )


@router.get(
    "/{id}",
    response_model=QuestionDBShema,
    response_model_exclude_none=True,
)
async def get_info_by_question_id(
    question: Question = Depends(get_from_db_question_by_id),
):
    """Получает информацию по вопросу."""
    return question


@router.post(
    "/",
    response_model=QuestionDBShema | Dict,
    status_code=status.HTTP_201_CREATED,
)
async def create_many_unique_questions(
    questions_num: Annotated[
        int, Query(title="The ID of the item to get", gt=0, le=100)
    ],
    session: AsyncSession = Depends(get_async_session),
):
    """Добавление новых уникальных вопросов."""
    try:
        many_questions = await get_jservice_questions(questions_num)
        if many_questions:
            questions_data = map(
                lambda data: Question(**data), many_questions["results"]
            )
            async with session.begin():
                session.add_all(*questions_data)
        return {}
    except SQLAlchemyError:
        error_message = (
            "Внутреняя ошибка сервиса при добавление новых вопросов!"
        )
        logger.exception(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question: Question = Depends(get_from_db_question_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление информации по вопросу."""
    try:
        await question_crud.remove(session, db_obj=question)
    except SQLAlchemyError:
        error_message = (
            "Внутреняя ошибка сервиса. " "Удаление вопроса не произведено!"
        )
        logger.exception(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )
