from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),  # type: ignore
        onupdate=datetime.now,
    )
