from __future__ import annotations

from fastapi import APIRouter, Depends, status

from src.application.use_cases.users.register_user import (
    RegisterUserInput,
    RegisterUserOutput,
    RegisterUseCase,
)
from src.application.use_cases.users.login_user import (
    LoginUserInput,
    LoginUserOutput,
    LoginUseCase,
)
from src.infrastructure.auth.auth_service import AuthService
from src.infrastructure.auth.password_hasher import PasswordHasher
from src.infrastructure.database.config import get_session
from src.infrastructure.database.uow import SqlAlchemyUnitOfWork
from src.presentation.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service() -> AuthService:
    return AuthService(secret_key="Secret key for secret app with slots")


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


async def get_register_use_case(
    session=Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> RegisterUseCase:
    uow = SqlAlchemyUnitOfWork(session)
    return RegisterUseCase(uow=uow, auth_service=auth_service)


async def get_login_use_case(
    session=Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> LoginUseCase:
    uow = SqlAlchemyUnitOfWork(session)
    return LoginUseCase(uow=uow, auth_service=auth_service)


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: RegisterRequest,
    use_case: RegisterUseCase = Depends(get_register_use_case),
) -> RegisterResponse:
    result: RegisterUserOutput = await use_case.execute(
        RegisterUserInput(email=payload.email, password=payload.password)
    )
    return RegisterResponse(id=result.id, email=result.email, role=result.role)


@router.post("/login", response_model=LoginResponse)
async def login_user(
    payload: LoginRequest,
    use_case: LoginUseCase = Depends(get_login_use_case),
) -> LoginResponse:
    result: LoginUserOutput = await use_case.execute(
        LoginUserInput(email=payload.email, password=payload.password)
    )
    return LoginResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )