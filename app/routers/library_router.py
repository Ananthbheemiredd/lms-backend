from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.library_schema import (
    LibraryCreate,
    LibraryUpdate,
    LibraryResponse
)

from app.services.library_service import (
    LibraryService
)

router = APIRouter(
    prefix="/libraries",
    tags=["Libraries"]
)


@router.post(
    "",
    response_model=LibraryResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_library(
    payload: LibraryCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryService.create_library(
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


@router.get(
    "",
    response_model=List[LibraryResponse]
)
async def get_libraries(
    db: AsyncSession = Depends(get_db)
):

    return await (
        LibraryService.get_all_libraries(
            db
        )
    )


@router.get(
    "/{library_id}",
    response_model=LibraryResponse
)
async def get_library_by_id(
    library_id: int,
    db: AsyncSession = Depends(get_db)
):

    library = await (
        LibraryService.get_library_by_id(
            db,
            library_id
        )
    )

    if not library:

        raise HTTPException(
            status_code=404,
            detail="Library not found"
        )

    return library


@router.put(
    "/{library_id}",
    response_model=LibraryResponse
)
async def update_library(
    library_id: int,
    payload: LibraryUpdate,
    db: AsyncSession = Depends(get_db)
):

    library = await (
        LibraryService.update_library(
            db,
            library_id,
            payload
        )
    )

    if not library:

        raise HTTPException(
            status_code=404,
            detail="Library not found"
        )

    return library


@router.delete(
    "/{library_id}"
)
async def delete_library(
    library_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted = await (
        LibraryService.delete_library(
            db,
            library_id
        )
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Library not found"
        )

    return {
        "message":
            "Library deleted successfully"
    }