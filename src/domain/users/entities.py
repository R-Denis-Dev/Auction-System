from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from common.value_objects import (
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
