from enum import StrEnum, unique


@unique
class UserRole(StrEnum):
    USER = "USER"
    CONSULTANT = "CONSULTANT"
    ADMIN = "ADMIN"


@unique
class RequestStatus(StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"
