from enum import Enum


class Role(str, Enum):
    GLOBAL_ADMIN = "global_admin"
    DOMAIN_ADMIN = "domain_admin"
    USER = "user"
