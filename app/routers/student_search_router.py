from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.student_schema import (
    StudentResponse
)

from app.services.student_search_service import (
    StudentSearchService
)

router = APIRouter(
    prefix="/students/search",
    tags=["Student Search"]
)


# =====================================
# SEARCH STUDENTS
# =====================================

@router.get(
    "",
    response_model=List[StudentResponse]
)
async def search_students(
    keyword: str,
    school_id: int,
    branch_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        students = await (
            StudentSearchService.search_students(
                db=db,
                keyword=keyword,
                school_id=school_id,
                branch_id=branch_id,
            )
        )

        return students

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )