from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import Base

Model = TypeVar("Model", bound=Base)


class Repository(ABC, Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    async def _read_by_id(self, id: int) -> Model | None:
        return await self._session.get(self._model, id)
