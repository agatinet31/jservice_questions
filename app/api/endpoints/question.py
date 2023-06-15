from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.logger import logger
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depends import get_from_db_question_by_id, get_jservice_questions
from app.core.config import settings
from app.core.db import get_async_session
from app.crud.question import question_crud
from app.exceptions import QuestionMaxCountRequestError
from app.models import Question
from app.schemas import QuestionDBShema

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
        request_count = 0
        last_two_obj = []
        while (
            questions_num > 0
            and request_count < settings.MAX_LIMIT_COUNT_FOR_REQUEST
        ):
            many_questions = await get_jservice_questions(questions_num)
            questions_data = map(
                lambda data: data.dict(), many_questions.results
            )
            insert_stmt = insert(Question).values(list(questions_data))
            do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
                index_elements=["question"]
            ).returning(Question)
            async with session.begin():
                success_insert = (await session.scalars(do_nothing_stmt)).all()
                questions_num -= len(success_insert)
                try:
                    last_two_obj = success_insert[-2:]
                except IndexError:
                    return last_two_obj.append(success_insert)
            request_count += 1
        if questions_num > 0:
            raise QuestionMaxCountRequestError
        return last_two_obj[-2] if len(last_two_obj) > 1 else {}
    except (SQLAlchemyError, QuestionMaxCountRequestError):
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
