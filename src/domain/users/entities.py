from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from domain.common.value_objects import (
    Email,
    HashedPassword,
    UserID
)


class UserRole(str, Enum):
    USER="user"
    ADMIN="admin"


@dataclass(slots=True)
class User:
    id:UserID
    email:Email
    password:HashedPassword
    role:UserRole
    is_blocked:bool
    created_at:datetime

    def block(self) -> None:
        self.is_blocked = True

    def unblock(self) -> None:
        self.is_blocked = False