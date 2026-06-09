from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.library_shelf_schema import (
    ShelfCreate,
    ShelfUpdate,
    ShelfResponse
)

from app.services.library_shelf_service import (
    LibraryShelfService
)

router = APIRouter(
    prefix="/shelves",
    tags=["Library Shelves"]
)


# =====================================
# HEALTH CHECK
# =====================================

@router.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def shelf_health():

    return {
        "module": "Shelf Management",
        "status": "running"
    }


# =====================================
# CREATE SHELF
# =====================================

@router.post(
    "",
    response_model=ShelfResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_shelf(
    payload: ShelfCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryShelfService
            .create_shelf(
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
            detail=f"Failed to create shelf: {str(e)}"
        )


# =====================================
# GET ALL SHELVES
# =====================================

@router.get(
    "",
    response_model=List[ShelfResponse]
)
async def get_shelves(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryShelfService
            .get_all_shelves(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch shelves: {str(e)}"
        )


# =====================================
# GET SHELF BY ID
# =====================================

@router.get(
    "/{shelf_id}",
    response_model=ShelfResponse
)
async def get_shelf_by_id(
    shelf_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        shelf = await (
            LibraryShelfService
            .get_shelf_by_id(
                db,
                shelf_id
            )
        )

        if not shelf:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shelf not found"
            )

        return shelf

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch shelf: {str(e)}"
        )


# =====================================
# GET SHELVES BY RACK
# =====================================

@router.get(
    "/rack/{rack_id}",
    response_model=List[ShelfResponse]
)
async def get_shelves_by_rack(
    rack_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryShelfService
            .get_shelves_by_rack(
                db,
                rack_id
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch rack shelves: {str(e)}"
        )


# =====================================
# UPDATE SHELF
# =====================================

@router.put(
    "/{shelf_id}",
    response_model=ShelfResponse
)
async def update_shelf(
    shelf_id: int,
    payload: ShelfUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        shelf = await (
            LibraryShelfService
            .update_shelf(
                db=db,
                shelf_id=shelf_id,
                payload=payload,
                updated_by=1
                # updated_by=current_user.id
            )
        )

        if not shelf:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shelf not found"
            )

        return shelf

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
            detail=f"Failed to update shelf: {str(e)}"
        )


# =====================================
# DELETE SHELF
# =====================================

@router.delete(
    "/{shelf_id}",
    status_code=status.HTTP_200_OK
)
async def delete_shelf(
    shelf_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        deleted = await (
            LibraryShelfService
            .delete_shelf(
                db,
                shelf_id
            )
        )

        if not deleted:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shelf not found"
            )

        return {
            "success": True,
            "message": "Shelf deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete shelf: {str(e)}"
        )