"""FastAPI application entry point."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from linguamate import __version__
from linguamate.api.routers import health
from linguamate.core.config import get_settings
from linguamate.core.logging_config import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Run code at startup (before yield) and shutdown (after yield)."""
    settings = get_settings()
    setup_logging(settings.log_level)
    logger.info(
        "Starting %s v%s (%s)", settings.app_name, __version__, settings.environment
    )
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Application factory: builds a fresh FastAPI app (also used by tests)."""
    settings = get_settings()
    app = FastAPI(
        title=f"{settings.app_name} API",
        version=__version__,
        description="Backend API of the LinguaMate agentic AI language tutor.",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    return app


app = create_app()