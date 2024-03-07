from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from consbot.db.repositories.stat import StatRepository
from consbot.db.repositories.user import UserRepository


class UnitOfWork:
    _session_factory: async_sessionmaker[AsyncSession]
    _session: AsyncSession

    users: UserRepository
    stats: StatRepository

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        self.users = UserRepository(session=self._session)
        self.stats = StatRepository(session=self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._session.rollback()

    async def roolback(self) -> None:
        await self._session.rollback()

    async def commit(self) -> None:
        await self._session.commit()
