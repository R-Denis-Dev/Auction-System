from __future__ import annotations

from fastapi import FastAPI

from src.presentation.api.routers.auth import router as auth_router



def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)