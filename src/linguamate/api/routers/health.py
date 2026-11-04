"""Health-check route used by monitoring, Docker and load balancers."""

from typing import Annotated

from fastapi import APIRouter, Depends

from linguamate import __version__
from linguamate.core.config import Settings, get_settings
from linguamate.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Service health check")
def health_check(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    """Return a small status document proving the API process is alive."""
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=__version__,
        environment=settings.environment,
    )