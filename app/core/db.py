from typing import AsyncGenerator

from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import as_declarative, declared_attr, sessionmaker

from app.core.config import settings

meta = MetaData(
    naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s'
    }
)

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session


@as_declarative(metadata=meta)
class Base:
    """Базовый класс модели сервиса."""
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str: # noqa
        """Возвращает имя таблицы, основанное на имени класса."""
        return cls.__name__.lower()
