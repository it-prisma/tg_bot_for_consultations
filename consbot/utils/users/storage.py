from collections.abc import Mapping
from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from consbot.db.models import User as UserDb
from consbot.utils.db import AbstractStorage, inject_session
from consbot.utils.users.models import User, UserTypes


class UserStorage(AbstractStorage):
    session_factory: async_sessionmaker[AsyncSession]

    @inject_session
    async def read_by_telegram_id(
        self,
        session: AsyncSession,
        telegram_id: int,
    ) -> User | None:
        query = select(UserDb).where(UserDb.telegram_id == telegram_id)
        obj = (await session.scalars(query)).first()
        return User.model_validate(obj) if obj else None

    @inject_session
    async def create_user(
        self,
        session: AsyncSession,
        telegram_id: int,
        user_type: UserTypes,
        properties: Mapping[str, Any],
    ) -> User:
        query = (
            insert(UserDb)
            .values(
                telegram_id=telegram_id,
                user_type=user_type,
                properties=properties,
            )
            .returning(UserDb)
        )
        obj = (await session.scalars(query)).one()
        return User.model_validate(obj)
