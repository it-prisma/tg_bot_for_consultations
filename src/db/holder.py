from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.stat import StatRepository
from src.db.repositories.user import UserRepository


class DatabaseHolder:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user = UserRepository(session=session)
        self.stat = StatRepository(session=session)
