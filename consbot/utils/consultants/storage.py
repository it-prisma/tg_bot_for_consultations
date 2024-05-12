from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from consbot.db.models import ConsultantRequest
from consbot.utils.consultants.models import ConsultantRequestStatuses
from consbot.utils.db import AbstractStorage, inject_session


class ConsultantStorage(AbstractStorage):
    @inject_session
    async def has_pending_consultant_request(
        self, session: AsyncSession, user_id: int
    ) -> bool:
        query = select(func.count()).where(
            ConsultantRequest.user_id == user_id,
            ConsultantRequest.status == ConsultantRequestStatuses.PENDING,
        )
        result = await session.scalar(query)
        return True if result and result > 0 else False
