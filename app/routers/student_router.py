from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.database.session import (
    get_db
)

from app.schemas.student_schema import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

from app.services.student_service import (
    StudentService
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# =====================================
# CREATE STUDENT
# =====================================

@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_student(
    payload: StudentCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        student = await (
            StudentService.create_student(
                db=db,
                payload=payload
            )
        )

        return student

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# GET ALL STUDENTS
# =====================================

@router.get(
    "",
    response_model=List[StudentResponse]
)
async def get_all_students(
    db: AsyncSession = Depends(get_db)
):

    try:

        students = await (
            StudentService.get_all_students(
                db
            )
        )

        return students

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# GET STUDENT BY ID
# =====================================

@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
async def get_student_by_id(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        student = await (
            StudentService.get_student_by_id(
                db,
                student_id
            )
        )

        if not student:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return student

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# UPDATE STUDENT
# =====================================

@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
async def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        student = await (
            StudentService.update_student(
                db=db,
                student_id=student_id,
                payload=payload
            )
        )

        if not student:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return student

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# DELETE STUDENT
# =====================================

@router.delete(
    "/{student_id}"
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        deleted = await (
            StudentService.delete_student(
                db,
                student_id
            )
        )

        if not deleted:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "status": "success",
            "message": "Student deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )