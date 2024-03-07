from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ChoiceType

from consbot.db.base import Base
from consbot.db.mixins import TimestampMixin
from consbot.enums import RequestStatus, UserRole


class User(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    role: Mapped[UserRole] = mapped_column(
        ChoiceType(UserRole, impl=String(16)), default=UserRole.USER, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ConsultantRequest(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=False, index=True
    )
    status: Mapped[RequestStatus] = mapped_column(
        ChoiceType(RequestStatus, impl=String(16)),
        nullable=False,
        index=True,
        default=RequestStatus.PENDING,
    )


class Theme(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )


class UserTheme(Base):
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=False, index=True, primary_key=True
    )
    theme_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("theme.id"), index=True, nullable=False, primary_key=True
    )


class Problem(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(3000), nullable=False)
    consultant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=True, index=True
    )


class ProblemTheme(Base):
    problem_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("problem.id"),
        index=True,
        nullable=False,
        primary_key=True,
    )
    consultant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=True, index=True, primary_key=True
    )
    theme_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("theme.id"), index=True, nullable=False
    )
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Message(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    problem_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("problem.id"), nullable=False, index=True
    )
    from_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=False, index=True
    )
    to_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(String(4000), nullable=False, default="")
    is_delivered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class Review(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    problem_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("problem.id"), nullable=False, index=True
    )
    from_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=False, index=True
    )
    about_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=False, index=True
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    comment: Mapped[str] = mapped_column(String(3000), nullable=False, default="")
