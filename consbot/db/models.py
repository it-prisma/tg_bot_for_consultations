from collections.abc import Mapping
from typing import Any

from sqlalchemy import BigInteger, Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from consbot.db.base import Base, TimestampMixin
from consbot.utils.consultants.models import ConsultantRequestStatuses
from consbot.utils.db import make_pg_enum
from consbot.utils.users.models import UserTypes


class Theme(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[int] = mapped_column(
        String(128),
        nullable=False,
        unique=True,
        index=True,
    )


class User(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        unique=True,
    )
    user_type: Mapped[UserTypes] = mapped_column(
        make_pg_enum(
            UserTypes,
            name="user_types",
            schema=None,
        ),
        nullable=False,
        server_default=UserTypes.NOT_REGISTERED.value,
    )
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    properties: Mapped[Mapping[str, Any]] = mapped_column(
        JSONB(),
        nullable=False,
        default="{ }",
    )


class ConsultantRequest(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[ConsultantRequestStatuses] = mapped_column(
        make_pg_enum(
            ConsultantRequestStatuses,
            name="consulant_request_statuses",
            schema=None,
        ),
        nullable=False,
        index=True,
        default=ConsultantRequestStatuses.PENDING.value,
    )
    properties: Mapped[Mapping[str, Any]] = mapped_column(
        JSONB(),
        nullable=False,
        default="{ }",
    )


class ConsultantTheme(Base):
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
    theme_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("theme.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Problem(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    consultant_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(3000), nullable=False)


class ProblemeTheme(Base):
    problem_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("problem.id", ondelete="CASCADE"),
        primary_key=True,
    )
    theme_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("theme.id", ondelete="CASCADE"),
        primary_key=True,
    )
    consultant_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    is_resolved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )


class Message(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    problem_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("problem.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    to_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    properties: Mapped[Mapping[str, Any]] = mapped_column(
        JSONB(),
        nullable=False,
        default="{ }",
    )
