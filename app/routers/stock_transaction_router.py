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

from app.schemas.stock_transaction_schema import (
    StockTransactionCreate,
    StockTransactionResponse,
    StockTransactionSummaryResponse
)

from app.services.stock_transaction_service import (
    StockTransactionService
)

router = APIRouter(
    prefix="/stock-transactions",
    tags=["Stock Transactions"]
)


# =====================================
# CREATE
# =====================================

@router.post(
    "",
    response_model=
        StockTransactionResponse
)
async def create_transaction(
    payload: StockTransactionCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            StockTransactionService
            .create_transaction(
                db,
                payload
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# GET ALL
# =====================================

@router.get(
    "",
    response_model=List[
        StockTransactionResponse
    ]
)
async def get_all_transactions(
    db: AsyncSession = Depends(get_db)
):

    return await (
        StockTransactionService
        .get_all_transactions(
            db
        )
    )


# =====================================
# GET BY ID
# =====================================

@router.get(
    "/{transaction_id}",
    response_model=
        StockTransactionResponse
)
async def get_transaction_by_id(
    transaction_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await (
        StockTransactionService
        .get_transaction_by_id(
            db,
            transaction_id
        )
    )


# =====================================
# GET BY BOOK
# =====================================

@router.get(
    "/book/{book_id}",
    response_model=List[
        StockTransactionResponse
    ]
)
async def get_transactions_by_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await (
        StockTransactionService
        .get_transactions_by_book(
            db,
            book_id
        )
    )


# =====================================
# GET BY PRODUCT
# =====================================

@router.get(
    "/product/{product_id}",
    response_model=List[
        StockTransactionResponse
    ]
)
async def get_transactions_by_product(
    product_id: str,
    db: AsyncSession = Depends(get_db)
):

    return await (
        StockTransactionService
        .get_transactions_by_product(
            db,
            product_id
        )
    )


# =====================================
# SUMMARY
# =====================================

@router.get(
    "/summary",
    response_model=
        StockTransactionSummaryResponse
)
async def get_summary(
    db: AsyncSession = Depends(get_db)
):

    return await (
        StockTransactionService
        .get_summary(
            db
        )
    )