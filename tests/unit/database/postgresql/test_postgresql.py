import pytest

from app.services.example_service import (
    PostgreSQL,
    PostgreSQLParams,
)


class TestPostgreSQL:
    """Проверка формирования данных перед вставкой в БД"""

    postgresql: PostgreSQL

    @pytest.mark.parametrize(
        "params_dict,expected_url",
        [
            ({}, "implementation+asyncpg://admin:password@anyhost:5342/my_database"),
            ({"username": "a$@!2b"}, "implementation+asyncpg://a%24%40%212b:password@anyhost:5342/my_database"),
            ({"password": "a$@!2b"}, "implementation+asyncpg://admin:a%24%40%212b@anyhost:5342/my_database"),
            ({"port": None}, "implementation+asyncpg://admin:password@anyhost/my_database"),
        ],
    )
    def test_make_url(self, params_dict: dict, expected_url: str) -> None:
        """Проверка формирования строки подключения к БД PostgreSQL"""
        default_params: dict = {
            "host": "anyhost",
            "port": 5342,
            "username": "admin",
            "password": "password",
        }
        params: dict = default_params | params_dict
        connection_params: PgConnectionParams = PostgreSQLParams(**params)  # type: ignore
        maked_url: str = PostgreSQL._make_url(connection_params=connection_params)  # pylint: disable=protected-access
        assert expected_url == maked_url
