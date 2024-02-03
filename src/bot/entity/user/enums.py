from enum import Enum


class Role(str, Enum):
    Quest = "guest"
    Admin = "admin"
