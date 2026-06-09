from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.library_row_schema import (
    RowCreate,
    RowUpdate,
    RowResponse
)

from app.services.library_row_service import (
    LibraryRowService
)

router = APIRouter(
    prefix="/rows",
    tags=["Library Rows"]
)


# =====================================
# CREATE ROW
# =====================================

@router.post(
    "",
    response_model=RowResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_row(
    payload: RowCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryRowService
            .create_row(
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
            detail=f"Failed to create row: {str(e)}"
        )


# =====================================
# GET ALL ROWS
# =====================================

@router.get(
    "",
    response_model=List[RowResponse]
)
async def get_rows(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryRowService
            .get_all_rows(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch rows: {str(e)}"
        )


# =====================================
# GET ROW BY ID
# =====================================

@router.get(
    "/{row_id}",
    response_model=RowResponse
)
async def get_row_by_id(
    row_id: int,
    db: AsyncSession = Depends(get_db)
):

    row = await (
        LibraryRowService
        .get_row_by_id(
            db,
            row_id
        )
    )

    if not row:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Row not found"
        )

    return row


# =====================================
# GET ROWS BY SHELF
# =====================================

@router.get(
    "/shelf/{shelf_id}",
    response_model=List[RowResponse]
)
async def get_rows_by_shelf(
    shelf_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryRowService
            .get_rows_by_shelf(
                db,
                shelf_id
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch shelf rows: {str(e)}"
        )


# =====================================
# UPDATE ROW
# =====================================

@router.put(
    "/{row_id}",
    response_model=RowResponse
)
async def update_row(
    row_id: int,
    payload: RowUpdate,
    db: AsyncSession = Depends(get_db)
):

    row = await (
        LibraryRowService
        .update_row(
            db=db,
            row_id=row_id,
            payload=payload,
            updated_by=1
            # updated_by=current_user.id
        )
    )

    if not row:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Row not found"
        )

    return row


# =====================================
# DELETE ROW
# =====================================

@router.delete(
    "/{row_id}"
)
async def delete_row(
    row_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted = await (
        LibraryRowService
        .delete_row(
            db,
            row_id
        )
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Row not found"
        )

    return {
        "message":
            "Row deleted successfully"
    }