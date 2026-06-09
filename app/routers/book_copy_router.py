from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.book_copy_model import BookCopy

from app.schemas.book_copy_schema import (
    BookCopyCreate,
    BookCopyUpdate,
    BookCopyResponse,
    AssignBookCopyLocation
)

from app.services.book_copy_service import (
    BookCopyService
)

router = APIRouter(
    prefix="/book-copies",
    tags=["Book Copies"]
)

# =====================================
# CREATE BOOK COPY
# =====================================

@router.post(
    "",
    response_model=BookCopyResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_book_copy(
    payload: BookCopyCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await BookCopyService.create_book_copy(
            db=db,
            payload=payload,
            created_by=1
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create book copy: {str(e)}"
        )


# =====================================
# GET ALL BOOK COPIES
# =====================================

@router.get(
    "",
    response_model=List[BookCopyResponse]
)
async def get_all_book_copies(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await BookCopyService.get_all_book_copies(db)

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch book copies: {str(e)}"
        )


# =====================================
# ASSIGN LOCATION
# =====================================

@router.post(
    "/assign-location",
    status_code=status.HTTP_200_OK
)
async def assign_location(
    payload: AssignBookCopyLocation,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await BookCopyService.assign_location(
            db,
            payload
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =====================================
# GET UNASSIGNED COPIES
# =====================================

@router.get("/unassigned")
async def get_unassigned_copies(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await BookCopyService.get_unassigned_copies(db)

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =====================================
# GET COPIES BY LOCATION
# =====================================

@router.get("/location")
async def get_copies_by_location(
    floor_id: int,
    rack_id: int,
    shelf_id: int,
    row_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await BookCopyService.get_copies_by_location(
            db,
            floor_id,
            rack_id,
            shelf_id,
            row_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =====================================
# GET BOOK COPY BY ID
# =====================================

@router.get(
    "/{copy_id}",
    response_model=BookCopyResponse
)
async def get_book_copy_by_id(
    copy_id: int,
    db: AsyncSession = Depends(get_db)
):

    copy = await BookCopyService.get_book_copy_by_id(
        db,
        copy_id
    )

    if not copy:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book copy not found"
        )

    return copy


# =====================================
# UPDATE BOOK COPY
# =====================================

@router.put(
    "/{copy_id}",
    response_model=BookCopyResponse
)
async def update_book_copy(
    copy_id: int,
    payload: BookCopyUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        copy = await BookCopyService.update_book_copy(
            db=db,
            copy_id=copy_id,
            payload=payload,
            updated_by=1
        )

        if not copy:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book copy not found"
            )

        return copy

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update book copy: {str(e)}"
        )
# =====================================
# BARCODE SCANNER
# =====================================
@router.get(
    "/barcode/{barcode}"
)
async def get_book_by_barcode(
    barcode: str,
    db: AsyncSession = Depends(get_db)
):

    copy = await (
        BookCopyService
        .get_book_copy_by_barcode(
            db,
            barcode
        )
    )

    if not copy:
        raise HTTPException(
            status_code=404,
            detail="Barcode not found"
        )

    return copy
@router.get(
    "/{copy_id}/barcode"
)
async def get_barcode(
    copy_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BookCopyService
            .get_barcode(
                db,
                copy_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.get(
    "/{copy_id}/download-barcode"
)
async def download_barcode(
    copy_id: int,
    db: AsyncSession = Depends(get_db)
):

    copy = await (
        BookCopyService
        .get_book_copy_by_id(
            db,
            copy_id
        )
    )

    if not copy:

        raise HTTPException(
            status_code=404,
            detail="Book copy not found"
        )

    file_path = (
        "." +
        copy.barcode_image_url
    )

    return FileResponse(
        path=file_path,
        filename=f"{copy.barcode}.svg",
        media_type="image/svg+xml"
    )

# =====================================
# DELETE BOOK COPY
# =====================================

@router.delete("/{copy_id}")
async def delete_book_copy(
    copy_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted = await BookCopyService.delete_book_copy(
        db,
        copy_id
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book copy not found"
        )

    return {
        "message": "Book copy deleted successfully"
    }