from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from consbot.db.models import User, UserRole
from consbot.db.repositories.base import Repository


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def read_by_id(self, user_id: int) -> User | None:
        return await self._read_by_id(id=user_id)

    async def create(self, user_id: int, role: UserRole = UserRole.USER) -> User:
        stmt = insert(User).values(id=user_id, role=role).returning(User)
        result: ScalarResult[User] = await self._session.scalars(
            select(User).from_statement(stmt)
        )
        await self._session.commit()
        user = result.first()
        if user is None:
            raise Exception
        return user

    async def get_or_create(self, user_id: int, is_admin: bool) -> User:
        user = await self.read_by_id(user_id=user_id)
        if user is not None:
            return user
        role = UserRole.ADMIN if is_admin else UserRole.USER
        return await self.create(user_id=user_id, role=role)
