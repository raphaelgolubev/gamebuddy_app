from enum import Enum


class Role(Enum):
    GUEST = "GUEST"
    USER = "USER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"
