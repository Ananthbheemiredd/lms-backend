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

from app.schemas.profile_information_schema import (
    ProfileInformationCreate,
    ProfileInformationUpdate,
    ProfileInformationResponse
)

from app.services.employee_service import (
    EmployeeService
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# =====================================
# CREATE EMPLOYEE
# =====================================

@router.post(
    "",
    response_model=ProfileInformationResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_employee(
    payload: ProfileInformationCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        employee = await (
            EmployeeService.create_employee(
                db=db,
                payload=payload
            )
        )

        return employee

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# GET ALL EMPLOYEES
# =====================================

@router.get(
    "",
    response_model=List[
        ProfileInformationResponse
    ]
)
async def get_all_employees(
    db: AsyncSession = Depends(get_db)
):

    try:

        employees = await (
            EmployeeService.get_all_employees(
                db
            )
        )

        return employees

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# GET EMPLOYEE BY ID
# =====================================

@router.get(
    "/{employee_id}",
    response_model=ProfileInformationResponse
)
async def get_employee_by_id(
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        employee = await (
            EmployeeService.get_employee_by_id(
                db,
                employee_id
            )
        )

        if not employee:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return employee

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# UPDATE EMPLOYEE
# =====================================

@router.put(
    "/{employee_id}",
    response_model=ProfileInformationResponse
)
async def update_employee(
    employee_id: int,
    payload: ProfileInformationUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        employee = await (
            EmployeeService.update_employee(
                db=db,
                employee_id=employee_id,
                payload=payload
            )
        )

        if not employee:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return employee

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# DELETE EMPLOYEE
# =====================================

@router.delete(
    "/{employee_id}"
)
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        deleted = await (
            EmployeeService.delete_employee(
                db,
                employee_id
            )
        )

        if not deleted:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return {
            "status": "success",
            "message":
                "Employee deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )