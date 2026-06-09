from idlelib.query import Query
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.database.session import (
    get_db
)

from app.schemas.book_stock_request_schema import (

    BookStockRequestCreate,

    BookStockRequestApprove,

    BookStockRequestReject,

    BookStockRequestComplete,

    BookStockRequestResponse
)

from app.services.book_stock_request_service import (
    BookStockRequestService
)

router = APIRouter(
    prefix="/stock-requests",
    tags=["Book Stock Requests"]
)


# =====================================
# CREATE STOCK REQUEST
# =====================================

@router.post(
    "",
    response_model=BookStockRequestResponse
)
async def create_stock_request(
    payload: BookStockRequestCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        request = await (
            BookStockRequestService
            .create_stock_request(
                db=db,
                payload=payload
            )
        )

        return request

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# GET ALL STOCK REQUESTS
# =====================================

@router.get(
    "",
    response_model=List[BookStockRequestResponse]
)
async def get_all_requests(
    db: AsyncSession = Depends(get_db)
):

    try:

        requests = await (
            BookStockRequestService
            .get_all_requests(
                db
            )
        )

        return requests

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# APPROVE STOCK REQUEST
# =====================================

@router.put(
    "/{request_id}/approve",
    response_model=BookStockRequestResponse
)
async def approve_request(
    request_id: int,
    payload: BookStockRequestApprove,
    db: AsyncSession = Depends(get_db)
):

    try:

        request = await (
            BookStockRequestService
            .approve_request(
                db=db,
                request_id=request_id,
                payload=payload
            )
        )

        return request

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# REJECT STOCK REQUEST
# =====================================

@router.put(
    "/{request_id}/reject",
    response_model=BookStockRequestResponse
)
async def reject_request(
    request_id: int,
    payload: BookStockRequestReject,
    db: AsyncSession = Depends(get_db)
):

    try:

        request = await (
            BookStockRequestService
            .reject_request(
                db=db,
                request_id=request_id,
                payload=payload
            )
        )

        return request

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# COMPLETE STOCK REQUEST
# =====================================

@router.put(
    "/{request_id}/complete",
    response_model=BookStockRequestResponse
)
async def complete_request(
    request_id: int,
    payload: BookStockRequestComplete,
    db: AsyncSession = Depends(get_db)
):

    try:

        request = await (
            BookStockRequestService
            .complete_request(
                db=db,
                request_id=request_id,
                payload=payload
            )
        )

        return request

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@router.get(
    "/{request_id}",
    response_model=BookStockRequestResponse
)
async def get_request_by_id(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookStockRequestService
            .get_request_by_id(
                db,
                request_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[
        BookStockRequestResponse
    ]
)
async def get_all_requests(

    status: str | None = Query(None),

    db: AsyncSession = Depends(get_db)
):

    return await (
        BookStockRequestService
        .get_all_requests(
            db,
            status
        )
    )
@router.delete(
    "/{request_id}"
)
async def delete_request(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):

    await (
        BookStockRequestService
        .delete_request(
            db,
            request_id
        )
    )

    return {
        "message":
            "Stock request deleted successfully"
    }