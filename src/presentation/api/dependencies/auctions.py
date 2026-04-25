from __future__ import annotations

from fastapi import Depends

from src.infrastructure.database.config import get_session
from src.infrastructure.database.uow import SqlAlchemyUnitOfWork
from src.application.use_cases.auctions.create_lot import CreateLotUseCase
from src.application.use_cases.auctions.list_lots import ListActiveLotsUseCase
from src.application.use_cases.auctions.get_lot import GetLotUseCase
from src.application.use_cases.auctions.cancel_lot import CancelLotUseCase
from src.application.use_cases.auctions.place_bid import PlaceBidUseCase


async def get_uow(session=Depends(get_session)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)


async def get_create_lot_uc(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> CreateLotUseCase:
    return CreateLotUseCase(uow)


async def get_list_active_lots_uc(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> ListActiveLotsUseCase:
    return ListActiveLotsUseCase(uow)


async def get_get_lot_uc(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetLotUseCase:
    return GetLotUseCase(uow)


async def get_cancel_lot_uc(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> CancelLotUseCase:
    return CancelLotUseCase(uow)


async def get_place_bid_uc(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> PlaceBidUseCase:
    return PlaceBidUseCase(uow) 