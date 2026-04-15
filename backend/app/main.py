import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging_config import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.routes.auth import router as auth_router
from app.routes.tasks import router as tasks_router
from app.routes.utils import router as utils_router

settings = get_settings()
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("application_started", extra={"env": settings.app_env})


@app.get("/")
def health() -> dict:
    return {"message": "Task API is running"}


app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(tasks_router, prefix=settings.api_v1_prefix)
app.include_router(utils_router, prefix=settings.api_v1_prefix)
