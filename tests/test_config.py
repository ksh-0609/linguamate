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


def test_database_url_is_built_from_parts() -> None:
    settings = Settings(
        postgres_user="user1",
        postgres_password="pass1",
        postgres_host="db.local",
        postgres_port=5433,
        postgres_db="mydb",
        _env_file=None,
    )

    assert settings.database_url == "postgresql+psycopg://user1:pass1@db.local:5433/mydb"


def test_special_characters_in_password_are_escaped() -> None:
    settings = Settings(postgres_password="p@ss:w/rd", _env_file=None)

    assert "p%40ss%3Aw%2Frd" in settings.database_url


def test_safe_database_url_hides_the_password() -> None:
    settings = Settings(postgres_password="topsecret", _env_file=None)

    assert "topsecret" not in settings.safe_database_url
    assert "***" in settings.safe_database_url


def test_default_db_password_is_rejected_in_production() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="production", _env_file=None)