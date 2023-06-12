from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as BaseSchema
from sqlalchemy import Column, select
from sqlalchemy.ext.asyncio import AsyncScalarResult, AsyncSession

from app.core.base import Base

Model = TypeVar('Model', bound=Base)
CreateSchema = TypeVar('CreateSchema', bound=BaseSchema)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseSchema)


class CRUDBase(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[Model]):
        """Базовый класс для методов CRUD (Create, Read, Update, Delete)."""
        self.model = model

    async def get_by_attribute(
            self,
            session: AsyncSession,
            attribute: Union[str, Column],
            value: Any
    ) -> AsyncScalarResult:
        if isinstance(attribute, str):
            attribute = getattr(self.model, attribute)
        statement = select(self.model).where(attribute == value)
        return await session.scalars(statement)

    async def get(
        self,
        session: AsyncSession,
        id: Any
    ) -> Optional[Model]:
        return (await self.get_by_attribute(session, self.model.id, id)).one()

    async def get_multi(
        self,
        session: AsyncSession,
        *,
        skip: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Model]:
        statement = select(self.model)
        if skip is not None:
            statement = statement.offset(skip)
        if limit is not None:
            statement = statement.limit(limit)
        return (await session.scalars(statement)).all()

    async def save(
        self,
        session: AsyncSession,
        obj: Model
    ) -> Model:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def create(
        self,
        session: AsyncSession,
        *,
        obj_in: Union[CreateSchema, Dict[str, Any]]
    ) -> Model:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        return await self.save(session, db_obj)

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: Model,
        obj_in: Union[UpdateSchema, Dict[str, Any]]
    ) -> Model:
        obj_data = jsonable_encoder(db_obj)
        update_data = (
            obj_in
            if isinstance(obj_in, dict)
            else obj_in.dict(exclude_unset=True)
        )
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return await self.save(session, db_obj)

    async def remove(
        self,
        session: AsyncSession,
        *,
        db_obj: Model
    ) -> Model:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
