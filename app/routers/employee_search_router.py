from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.profile_information_schema import (
    ProfileInformationResponse
)

from app.services.employee_search_service import (
    EmployeeSearchService
)

router = APIRouter(
    prefix="/employees/search",
    tags=["Employee Search"]
)


# =====================================
# SEARCH EMPLOYEES
# =====================================

@router.get(
    "",
    response_model=List[
        ProfileInformationResponse
    ]
)
async def search_employees(
    keyword: str,
    school_id: int,
    branch_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        employees = await (
            EmployeeSearchService.search_employees(
                db=db,
                keyword=keyword,
                school_id=school_id,
                branch_id=branch_id,
            )
        )

        return employees

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )