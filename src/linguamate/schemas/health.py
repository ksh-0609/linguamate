"""Pydantic models for the health-check endpoint."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response body of GET /health."""

    status: str = Field(..., examples=["ok"])
    app_name: str = Field(..., examples=["LinguaMate"])
    version: str = Field(..., examples=["0.1.0"])
    environment: str = Field(..., examples=["development"])