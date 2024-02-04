from enum import Enum


class Role(str, Enum):
    GUEST = "guest"
    ADMIN = "admin"
