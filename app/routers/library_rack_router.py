from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.library_rack_schema import (
    RackCreate,
    RackUpdate,
    RackResponse
)

from app.services.library_rack_service import (
    LibraryRackService
)

router = APIRouter(
    prefix="/racks",
    tags=["Library Racks"]
)


# =====================================
# Health Check
# =====================================

@router.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def rack_health():

    return {
        "module": "Rack Management",
        "status": "running"
    }


# =====================================
# Create Rack
# =====================================

@router.post(
    "",
    response_model=RackResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_rack(
    payload: RackCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryRackService
            .create_rack(
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
            detail=f"Failed to create rack: {str(e)}"
        )


# =====================================
# Get All Racks
# =====================================

@router.get(
    "",
    response_model=List[RackResponse]
)
async def get_racks(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryRackService
            .get_all_racks(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch racks: {str(e)}"
        )


# =====================================
# Get Rack By ID
# =====================================

@router.get(
    "/{rack_id}",
    response_model=RackResponse
)
async def get_rack_by_id(
    rack_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        rack = await (
            LibraryRackService
            .get_rack_by_id(
                db,
                rack_id
            )
        )

        if not rack:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rack not found"
            )

        return rack

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch rack: {str(e)}"
        )


# =====================================
# Get Racks By Floor
# =====================================

@router.get(
    "/floor/{floor_id}",
    response_model=List[RackResponse]
)
async def get_racks_by_floor(
    floor_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryRackService
            .get_racks_by_floor(
                db,
                floor_id
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch floor racks: {str(e)}"
        )


# =====================================
# Update Rack
# =====================================

@router.put(
    "/{rack_id}",
    response_model=RackResponse
)
async def update_rack(
    rack_id: int,
    payload: RackUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        rack = await (
            LibraryRackService
            .update_rack(
                db=db,
                rack_id=rack_id,
                payload=payload,
                updated_by=1
                # updated_by=current_user.id
            )
        )

        if not rack:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rack not found"
            )

        return rack

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
            detail=f"Failed to update rack: {str(e)}"
        )


# =====================================
# Delete Rack
# =====================================

@router.delete(
    "/{rack_id}",
    status_code=status.HTTP_200_OK
)
async def delete_rack(
    rack_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        deleted = await (
            LibraryRackService
            .delete_rack(
                db,
                rack_id
            )
        )

        if not deleted:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rack not found"
            )

        return {
            "success": True,
            "message": "Rack deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete rack: {str(e)}"
        )