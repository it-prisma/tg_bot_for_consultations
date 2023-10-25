from typing import Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def build_db_connection_uri(
    *, host: str, port: int, user: str, password: str, database: str
) -> str:
    url = URL.create(
        drivername="asyncpg",
        username=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )
    return f"postgresql+{url.render_as_string(hide_password=False)}"


def create_engine(connection_uri: str, **engine_kwargs: Any) -> AsyncEngine:
    return create_async_engine(url=connection_uri, **engine_kwargs)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
