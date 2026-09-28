from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from .config import settings

from .database import init_db

from .routes import router

from .api import router as api_router


@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    init_db()

    yield


app = FastAPI(

    title=settings.app_name,

    description=(
        "AI-powered 7-day wellness "
        "plan generator using Gemini."
    ),

    version="1.0.0",

    lifespan=lifespan
)


static_directory = (
    Path(__file__).resolve()
    .parent
    / "static"
)


app.mount(

    "/static",

    StaticFiles(
        directory=static_directory
    ),

    name="static"
)


app.include_router(
    router
)


app.include_router(
    api_router
)