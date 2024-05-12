from enum import StrEnum, unique


@unique
class ConsultantRequestStatuses(StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"
