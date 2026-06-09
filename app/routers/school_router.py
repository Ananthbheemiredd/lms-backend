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

from app.schemas.school_schema import (

    SchoolCreate,

    SchoolUpdate,

    SchoolResponse
)

from app.services.school_service import (
    SchoolService
)

router = APIRouter(
    prefix="/schools",
    tags=["Schools"]
)


# =====================================
# CREATE SCHOOL
# =====================================

@router.post(
    "",
    response_model=SchoolResponse
)
async def create_school(
    payload: SchoolCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        school = await (
            SchoolService.create_school(
                db,
                payload
            )
        )

        return school

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =====================================
# GET ALL SCHOOLS
# =====================================

@router.get(
    "",
    response_model=List[SchoolResponse]
)
async def get_all_schools(
    db: AsyncSession = Depends(get_db)
):

    return await (
        SchoolService.get_all_schools(
            db
        )
    )


# =====================================
# GET SCHOOL BY ID
# =====================================

@router.get(
    "/{school_id}",
    response_model=SchoolResponse
)
async def get_school_by_id(
    school_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            SchoolService.get_school_by_id(
                db,
                school_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# =====================================
# UPDATE SCHOOL
# =====================================

@router.put(
    "/{school_id}",
    response_model=SchoolResponse
)
async def update_school(
    school_id: int,
    payload: SchoolUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            SchoolService.update_school(
                db,
                school_id,
                payload
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )