"""Tests for the settings loader."""

import pytest
from pydantic import ValidationError

from linguamate.core.config import Settings


def test_log_level_is_normalised_to_uppercase() -> None:
    settings = Settings(log_level="debug", _env_file=None)

    assert settings.log_level == "DEBUG"


def test_invalid_log_level_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(log_level="verbose", _env_file=None)