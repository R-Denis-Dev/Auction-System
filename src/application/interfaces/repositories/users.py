from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from domain.users.entities import User
from domain.common.value_objects import (
    Email, UserID
)

class IUserRepository(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id:UserID) -> User | None: ...
    @abstractmethod
    async def get_by_email(self, email:Email) -> User | None: ...
    @abstractmethod
    async def create_user(self, user:User) -> User: ...