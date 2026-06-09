from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.book_category_schema import (
    BookCategoryCreate,
    BookCategoryUpdate,
    BookCategoryResponse
)

from app.services.book_category_service import (
    BookCategoryService
)

router = APIRouter(
    prefix="/book-categories",
    tags=["Book Categories"]
)


# =====================================
# CREATE CATEGORY
# =====================================

@router.post(
    "",
    response_model=BookCategoryResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_category(
    payload: BookCategoryCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookCategoryService
            .create_category(
                db=db,
                payload=payload,
                created_by=1
                # created_by=current_user.id
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
            detail=f"Failed to create category: {str(e)}"
        )


# =====================================
# GET ALL CATEGORIES
# =====================================

@router.get(
    "",
    response_model=List[BookCategoryResponse]
)
async def get_categories(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookCategoryService
            .get_all_categories(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch categories: {str(e)}"
        )


# =====================================
# GET CATEGORY BY ID
# =====================================

@router.get(
    "/{category_id}",
    response_model=BookCategoryResponse
)
async def get_category_by_id(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):

    category = await (
        BookCategoryService
        .get_category_by_id(
            db,
            category_id
        )
    )

    if not category:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


# =====================================
# UPDATE CATEGORY
# =====================================

@router.put(
    "/{category_id}",
    response_model=BookCategoryResponse
)
async def update_category(
    category_id: int,
    payload: BookCategoryUpdate,
    db: AsyncSession = Depends(get_db)
):

    category = await (
        BookCategoryService
        .update_category(
            db=db,
            category_id=category_id,
            payload=payload,
            updated_by=1
            # updated_by=current_user.id
        )
    )

    if not category:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


# =====================================
# DELETE CATEGORY
# =====================================

@router.delete(
    "/{category_id}"
)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted = await (
        BookCategoryService
        .delete_category(
            db,
            category_id
        )
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return {
        "message":
            "Category deleted successfully"
    }