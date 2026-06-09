from http.client import HTTPException
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.book_schema import (
    BookCreate,
    BookResponse, BookUpdate
)

from app.services.book_service import BookService


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# =====================================
# Create Book
# =====================================

@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_book(
    payload: BookCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookService.create_book(
                db=db,
                payload=payload,
                user_id=1
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create book: {str(e)}"
        )
@router.get(
    "",
    response_model=List[BookResponse]
)
async def get_all_books(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookService.get_all_books(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch books: {str(e)}"
        )
@router.get(
    "/{book_id}",
    response_model=BookResponse
)
async def get_book_by_id(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookService.get_book_by_id(
                db,
                book_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
@router.put(
    "/{book_id}",
    response_model=BookResponse
)
async def update_book(
    book_id: int,
    payload: BookUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookService.update_book(
                db=db,
                book_id=book_id,
                payload=payload,
                user_id=1
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update book: {str(e)}"
        )
@router.delete(
    "/{book_id}"
)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookService.delete_book(
                db=db,
                book_id=book_id,
                user_id=1
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete book: {str(e)}"
        )

@router.get(
    "/{book_id}/inventory-summary"
)
async def get_inventory_summary(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookService.get_inventory_summary(
                db,
                book_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/low-stock"
)
async def get_low_stock_books(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookService.get_low_stock_books(
                db
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )