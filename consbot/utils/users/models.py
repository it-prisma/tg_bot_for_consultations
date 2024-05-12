from collections.abc import Mapping
from datetime import datetime
from enum import StrEnum, unique
from typing import Any

from pydantic import BaseModel, ConfigDict


@unique
class UserTypes(StrEnum):
    ADMINISTRATOR = "ADMINISTRATOR"
    CONSULTANT = "CONSULTANT"
    REGULAR = "REGULAR"
    NOT_REGISTERED = "NOT_REGISTERED"


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    user_type: UserTypes
    properties: Mapping[str, Any]
    is_banned: bool
    created_at: datetime
    updated_at: datetime

    @property
    def is_admin(self) -> bool:
        return self.user_type == UserTypes.ADMINISTRATOR

    @property
    def is_consultant(self) -> bool:
        return self.user_type == UserTypes.CONSULTANT

    @property
    def is_regular(self) -> bool:
        return self.user_type == UserTypes.REGULAR

    @property
    def is_anonymous(self) -> bool:
        return self.user_type == UserTypes.NOT_REGISTERED
