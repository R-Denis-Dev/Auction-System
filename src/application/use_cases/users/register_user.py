from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from src.application.interfaces.auth import IAuthService
from src.application.interfaces.unit_of_work import IUnitOFWork
from src.domain.common.exceptions import ValidationError
from src.domain.common.value_objects import (
    UserId, HashedPassword, Email
)
from src.domain.users.entities import (
    User, UserRole
)


@dataclass
class RegisterUserInput:
    email:str
    password:str

@dataclass
class RegisterUserOutput:
    id:int
    email:str
    role:str


class RegisterUseCase:
    def __init__(self, uow:IUnitOFWork, auth_service:IAuthService) -> None:
        self._uow = uow
        self._auth = auth_service

    async def execute(self, data:RegisterUserInput) -> RegisterUserOutput:
        email_vo = Email(data.email)

        async with self._uow:
            existing = await self._uow.users.get_by_email(email_vo)
            if existing is not None:
                raise ValidationError("User with this email already exists")
            
            hashed = self._auth.hash_password(data.password)
            user = User(
                id=UserId,
                email=email_vo,
                password=HashedPassword(hashed),
                role=UserRole.USER,
                is_blocked=False,
                created_at=datetime.now(timezone.utc)
            )
            created = await self._uow.users.add(user)

        return RegisterUserOutput(
            id=int(created.id.value),
            email=str(created.email),
            role=created.role.value
        )
