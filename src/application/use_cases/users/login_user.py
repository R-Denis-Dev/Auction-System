from __future__ import annotations

from dataclasses import dataclass

from application.interfaces.auth import IAuthService
from application.interfaces.unit_of_work import IUnitOFWork
from domain.common.exceptions import AuthError
from domain.common.value_objects import Email
from domain.users.entities import User


@dataclass
class LoginUserInput:
    email:str
    password:str

@dataclass
class LoginUserOutput:
    access_token:str
    refresh_token:str
    user_id:int
    email:int
    role:str


class LoginUseCase:
    def __init__(self, uow:IUnitOFWork, auth_service:IAuthService) -> None:
        self._uow = uow
        self._auth = auth_service

    async def execute(self, data:LoginUserInput) -> LoginUserOutput:
        email_vo = Email(data.email)

        async with self._uow:
            user = await self._uow.users.get_by_email(email_vo)

        if user is None:
            raise AuthError("Invalid credentials")
        if not self._auth.verify_password(data.password, user.password.value):
            raise AuthError("Invalid credentials")
        if user.is_blocked:
            raise AuthError("User is blocked")
        
        access = self._auth.create_access_token(user)
        refresh = self._auth.create_refresh_token(user)

        return LoginUserOutput(
            access_token=access,
            refresh_token=refresh,
            user_id=int(user.id.value),
            email=str(user.email),
            role=user.role.value
        )
    