from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.database.session import (
    get_db
)

from app.schemas.book_stock_schema import (
    BookStockCreate,
    BookStockUpdate,
    BookStockResponse,
    BookStockSummaryResponse
)

from app.services.book_stock_service import (
    BookStockService
)

router = APIRouter(
    prefix="/book-stocks",
    tags=["Book Stocks"]
)


# =====================================
# CREATE STOCK
# =====================================

@router.post(
    "",
    response_model=BookStockResponse
)
async def create_stock(
    payload: BookStockCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookStockService
            .create_stock(
                db=db,
                payload=payload,
                created_by=1
            )
        )

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
# GET ALL STOCKS
# =====================================

@router.get(
    "",
    response_model=List[
        BookStockResponse
    ]
)
async def get_all_stocks(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookStockService
            .get_all_stocks(
                db
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# GET STOCK BY ID
# =====================================

@router.get(
    "/{stock_id}",
    response_model=BookStockResponse
)
async def get_stock_by_id(
    stock_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        stock = await (
            BookStockService
            .get_stock_by_id(
                db,
                stock_id
            )
        )

        if not stock:

            raise HTTPException(
                status_code=404,
                detail="Stock not found"
            )

        return stock

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# UPDATE STOCK
# =====================================

@router.put(
    "/{stock_id}",
    response_model=BookStockResponse
)
async def update_stock(
    stock_id: int,
    payload: BookStockUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookStockService
            .update_stock(
                db=db,
                stock_id=stock_id,
                payload=payload,
                updated_by=1
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# DELETE STOCK
# =====================================

@router.delete(
    "/{stock_id}"
)
async def delete_stock(
    stock_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        await (
            BookStockService
            .delete_stock(
                db,
                stock_id
            )
        )

        return {
            "message":
                "Stock deleted successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# STOCK SUMMARY
# =====================================

@router.get(
    "/summary",
    response_model=
        BookStockSummaryResponse
)
async def get_stock_summary(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookStockService
            .get_stock_summary(
                db
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )