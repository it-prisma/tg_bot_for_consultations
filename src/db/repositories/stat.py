from typing import Literal

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User, UserRole
from src.db.repositories.base import Repository

StatDict = dict[Literal["total", "active", "deactive"], int]


class StatRepository(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def persons(self, role: UserRole) -> StatDict:
        users = (
            await self._session.scalars(select(User).where(User.role == role))
        ).all()
        logger.info(f"{users}")
        active = len(list(filter(lambda x: x.is_active, users)))
        unactive = len(list(filter(lambda x: not x.is_active, users)))

        return {
            "total": active + unactive,
            "active": active,
            "deactivate": unactive,
        }

    async def users(self) -> StatDict:
        return await self.persons(role=UserRole.USER)

    async def admins(self) -> StatDict:
        return await self.persons(role=UserRole.ADMIN)

    async def consultants(self) -> StatDict:
        return await self.persons(role=UserRole.CONSULTANT)
