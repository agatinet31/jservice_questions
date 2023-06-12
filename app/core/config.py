import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """Класс конфигурации сервиса."""
    APP_TITLE: str = 'Парсинг товаров wildberries'
    DESCRIPTION: str = (
        'Сервис парсит информацию по вопросам '
        'с сайта https://jservice.io и сохраняет их в БД'
    )
    JSERVICE_URL: str = 'https://jservice.io/api/random'
    CORS_ORIGINS: List[AnyHttpUrl] = []
    SECRET: str = secrets.token_urlsafe(32)
    datatime_format: str = '%Y-%m-%dT%H:%M:%SZ'
    POSTGRES_SERVER: str = 'db'
    POSTGRES_PORT: str = '5432'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = 'js'
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any: # noqa
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]: # noqa
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = '.env'


settings = Settings()
