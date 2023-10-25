from sqlalchemy.ext.asyncio import AsyncSession

from consbot.db.repositories.stat import StatRepository
from consbot.db.repositories.user import UserRepository


class DatabaseHolder:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user = UserRepository(session=session)
        self.stat = StatRepository(session=session)
