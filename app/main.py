from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(title=settings.APP_TITLE)

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app.include_router(main_router)
