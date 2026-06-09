from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.book_search_schema import (
    BookSearchResponse
)

from app.services.book_search_service import (
    BookSearchService
)

router = APIRouter(
    prefix="/book-search",
    tags=["Book Search"]
)


# =====================================
# SEARCH BOOKS
# =====================================

@router.get(
    "",
    response_model=List[BookSearchResponse],
    status_code=status.HTTP_200_OK
)
async def search_books(
    keyword: str = Query(
        ...,
        min_length=1
    ),

    school_id: int = Query(
        ...,
        gt=0
    ),

    branch_id: int = Query(
        ...,
        gt=0
    ),

    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),

    offset: int = Query(
        default=0,
        ge=0
    ),

    db: AsyncSession = Depends(get_db)
):

    try:

        keyword = keyword.strip()

        if not keyword:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Keyword is required"
            )

        books = await (
            BookSearchService.search_books(
                db=db,
                keyword=keyword,
                school_id=school_id,
                branch_id=branch_id,
                limit=limit,
                offset=offset
            )
        )

        return books

    except HTTPException:
        raise

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )