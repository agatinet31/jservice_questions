import asyncio
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger

from app.api.question import (
    get_from_db_question_by_id,
    get_unique_jservice_questions,
)
from app.core.db import get_async_session
from app.crud.question import question_crud
from app.models import Question
from app.schemas import ManyQuestionParseShema, QuestionDBShema
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
    "/{question_id}",
    response_model=QuestionDBShema,
    response_model_exclude_none=True,
)
async def get_info_by_product_id(
    question: Question = Depends(get_from_db_question_by_id),
):
    """Получает информацию по товару."""
    return question


@router.post(
    "/",
    response_model=QuestionDBShema,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_many_unique_questions(
    many_unique_questions: ManyQuestionParseShema = Depends(
        get_unique_jservice_questions
    ),
    session: AsyncSession = Depends(get_async_session),
):
    """Добавление номенклатуры товара."""
    try:
        async_calls = [get_wb_product_info_by_id(id) for id in product_ids]
        parse_products: List[QuestionParseShema] = await asyncio.gather(
            *async_calls
        )
        if parse_products:
            success_product = map(
                lambda product: Question(**product), parse_products
            )
            async with session.begin():
                session.add_all(*success_product)

        return await product_crud.create(session, obj_in=parse_wb_product)
    except SQLAlchemyError:
        error_message = (
            "Внутреняя ошибка сервиса при добавление нового "
            f"товара: ID = {parse_wb_product.id}, "
            f"наименование = `{parse_wb_product.name}`!"
        )
        logger.exception(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
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
