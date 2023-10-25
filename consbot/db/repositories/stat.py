import logging
from typing import Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from consbot.db.models import User, UserRole
from consbot.db.repositories.base import Repository

StatDict = dict[Literal["total", "active", "deactive"], int]

log = logging.getLogger(__name__)


class StatRepository(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def persons(self, role: UserRole) -> StatDict:
        users = (
            await self._session.scalars(select(User).where(User.role == role))
        ).all()
        active = len(list(filter(lambda x: x.is_active, users)))
        unactive = len(list(filter(lambda x: not x.is_active, users)))
        log.info("Stat repo total=%d", active + unactive)
        return {
            "total": active + unactive,
            "active": active,
            "deactive": unactive,
        }

    async def users(self) -> StatDict:
        return await self.persons(role=UserRole.USER)

    async def admins(self) -> StatDict:
        return await self.persons(role=UserRole.ADMIN)

    async def consultants(self) -> StatDict:
        return await self.persons(role=UserRole.CONSULTANT)
