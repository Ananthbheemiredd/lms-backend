from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.library_floor_schema import (
    FloorCreate,
    FloorUpdate,
    FloorResponse
)

from app.services.library_floor_service import (
    LibraryFloorService
)

router = APIRouter(
    prefix="/floors",
    tags=["Library Floors"]
)


# =====================================
# Health Check
# =====================================

@router.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def floor_health():

    return {
        "module": "Floor Management",
        "status": "running"
    }


# =====================================
# Create Floor
# =====================================

@router.post(
    "",
    response_model=FloorResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_floor(
    payload: FloorCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryFloorService
            .create_floor(
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
            detail=f"Failed to create floor: {str(e)}"
        )


# =====================================
# Get All Floors
# =====================================

@router.get(
    "",
    response_model=List[FloorResponse],
    status_code=status.HTTP_200_OK
)
async def get_floors(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryFloorService
            .get_all_floors(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch floors: {str(e)}"
        )


# =====================================
# Get Floor By ID
# =====================================

@router.get(
    "/{floor_id}",
    response_model=FloorResponse,
    status_code=status.HTTP_200_OK
)
async def get_floor_by_id(
    floor_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        floor = await (
            LibraryFloorService
            .get_floor_by_id(
                db,
                floor_id
            )
        )

        if not floor:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Floor not found"
            )

        return floor

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch floor: {str(e)}"
        )


# =====================================
# Get Floors By Library
# =====================================

@router.get(
    "/library/{library_id}",
    response_model=List[FloorResponse],
    status_code=status.HTTP_200_OK
)
async def get_floors_by_library(
    library_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryFloorService
            .get_floors_by_library(
                db,
                library_id
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch library floors: {str(e)}"
        )


# =====================================
# Update Floor
# =====================================

@router.put(
    "/{floor_id}",
    response_model=FloorResponse,
    status_code=status.HTTP_200_OK
)
async def update_floor(
    floor_id: int,
    payload: FloorUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        floor = await (
            LibraryFloorService
            .update_floor(
                db=db,
                floor_id=floor_id,
                payload=payload,
                updated_by=1
                # updated_by=current_user.id
            )
        )

        if not floor:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Floor not found"
            )

        return floor

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
            detail=f"Failed to update floor: {str(e)}"
        )


# =====================================
# Delete Floor
# =====================================

@router.delete(
    "/{floor_id}",
    status_code=status.HTTP_200_OK
)
async def delete_floor(
    floor_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        deleted = await (
            LibraryFloorService
            .delete_floor(
                db,
                floor_id
            )
        )

        if not deleted:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Floor not found"
            )

        return {
            "success": True,
            "message": "Floor deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete floor: {str(e)}"
        )