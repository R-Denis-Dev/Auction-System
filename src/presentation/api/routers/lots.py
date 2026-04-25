from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.application.use_cases.auctions.create_lot import (
    CreateLotInput,
    CreateLotUseCase,
)
from src.application.use_cases.auctions.list_lots import (
    ListActiveLotsUseCase,
)
from src.application.use_cases.auctions.get_lot import (
    GetLotInput,
    GetLotUseCase,
)
from src.application.use_cases.auctions.cancel_lot import (
    CancelLotInput,
    CancelLotUseCase,
)
from src.application.use_cases.auctions.place_bid import (
    PlaceBidInput,
    PlaceBidUseCase,
)
from src.domain.users.entities import User
from src.presentation.api.dependencies.auth import get_current_user
from src.presentation.api.dependencies.auctions import (
    get_create_lot_uc,
    get_list_active_lots_uc,
    get_get_lot_uc,
    get_cancel_lot_uc,
    get_place_bid_uc,
)
from src.presentation.schemas.lots import (
    CreateLotRequest,
    LotResponse,
    LotSummaryResponse,
)
from src.presentation.api.websockets.manager import manager
from src.presentation.schemas.bids import PlaceBidRequest


router = APIRouter(
    prefix="/lots",
    tags=["lots"],
)


@router.post(
    "",
    response_model=LotResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_lot(
    payload: CreateLotRequest,
    current_user: User = Depends(get_current_user),
    use_case: CreateLotUseCase = Depends(get_create_lot_uc),
) -> LotResponse:
    try:
        result = await use_case.execute(
            CreateLotInput(
                owner_id=int(current_user.id.value),
                title=payload.title,
                description=payload.description,
                start_price=payload.start_price,
                bid_step=payload.bid_step,
                starts_at=payload.starts_at,
                ends_at=payload.ends_at,
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return LotResponse(
        id=result.id,
        owner_id=result.owner_id,
        title=result.title,
        description=result.description,
        current_price=result.current_price,
        start_price=payload.start_price,
        bid_step=payload.bid_step,
        status=result.status,
        starts_at=result.starts_at,
        ends_at=result.ends_at,
    )


@router.get(
    "",
    response_model=list[LotSummaryResponse],
    status_code=status.HTTP_200_OK,
)
async def list_active_lots(
    use_case: ListActiveLotsUseCase = Depends(get_list_active_lots_uc),
) -> list[LotSummaryResponse]:
    result = await use_case.execute()
    return [
        LotSummaryResponse(
            id=item.id,
            owner_id=item.owner_id,
            title=item.title,
            current_price=item.current_price,
            status=item.status,
            ends_at=item.ends_at,
        )
        for item in result
    ]


@router.get(
    "/{lot_id}",
    response_model=LotResponse,
    status_code=status.HTTP_200_OK,
)
async def get_lot(
    lot_id: int,
    use_case: GetLotUseCase = Depends(get_get_lot_uc),
) -> LotResponse:
    try:
        result = await use_case.execute(GetLotInput(lot_id=lot_id))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lot not found",
        )

    return LotResponse(
        id=result.id,
        owner_id=result.owner_id,
        title=result.title,
        description=result.description,
        current_price=result.current_price,
        start_price=result.start_price,
        bid_step=result.bid_step,
        status=result.status,
        starts_at=result.starts_at,
        ends_at=result.ends_at,
    )


@router.post(
    "/{lot_id}/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_lot(
    lot_id: int,
    current_user: User = Depends(get_current_user),
    use_case: CancelLotUseCase = Depends(get_cancel_lot_uc),
) -> Response:
    is_admin = current_user.role.value == "admin"

    try:
        await use_case.execute(
            CancelLotInput(
                lot_id=lot_id,
                requester_id=int(current_user.id.value),
                is_admin=is_admin,
            )
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lot not found",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to cancel this lot",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{lot_id}/bids",
    status_code=status.HTTP_201_CREATED,
)
async def place_bid(
    lot_id: int,
    payload: PlaceBidRequest,
    current_user: User = Depends(get_current_user),
    use_case: PlaceBidUseCase = Depends(get_place_bid_uc),
):
    try:
        result = await use_case.execute(
            PlaceBidInput(
                lot_id=lot_id,
                user_id=int(current_user.id.value),
                amount=payload.amount,
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    await manager.broadcast_to_lot(
        lot_id,
        {
            "event": "bid_placed",
            "lot_id": result.lot_id,
            "current_price": result.current_price,
            "status": result.status,
            "bidder_id": int(current_user.id.value),
            "amount": payload.amount,
        },
    )

    return {
        "lot_id": result.lot_id,
        "current_price": result.current_price,
        "status": result.status,
    }