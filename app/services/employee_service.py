from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.profile_information_model import (
    ProfileInformation
)

from app.schemas.profile_information_schema import (
    ProfileInformationCreate,
    ProfileInformationUpdate
)


class EmployeeService:

    # =====================================
    # CREATE EMPLOYEE
    # =====================================

    @staticmethod
    async def create_employee(
        db: AsyncSession,
        payload: ProfileInformationCreate
    ):

        employee = ProfileInformation(

            school_id=payload.school_id,

            branch_id=payload.branch_id,

            employee_code=payload.employee_code,

            employee_name=payload.employee_name,

            email=payload.email,

            mobile_number=payload.mobile_number,

            department_name=payload.department_name,

            designation=payload.designation
        )

        db.add(employee)

        await db.commit()

        await db.refresh(employee)

        return employee

    # =====================================
    # GET ALL EMPLOYEES
    # =====================================

    @staticmethod
    async def get_all_employees(
        db: AsyncSession
    ):

        result = await db.execute(
            select(ProfileInformation)
        )

        return result.scalars().all()

    # =====================================
    # GET EMPLOYEE BY ID
    # =====================================

    @staticmethod
    async def get_employee_by_id(
        db: AsyncSession,
        employee_id: int
    ):

        result = await db.execute(
            select(ProfileInformation).where(
                ProfileInformation.id
                == employee_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================
    # UPDATE EMPLOYEE
    # =====================================

    @staticmethod
    async def update_employee(
        db: AsyncSession,
        employee_id: int,
        payload: ProfileInformationUpdate
    ):

        employee = await db.get(
            ProfileInformation,
            employee_id
        )

        if not employee:

            return None

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )

        for key, value in update_data.items():

            setattr(
                employee,
                key,
                value
            )

        await db.commit()

        await db.refresh(employee)

        return employee

    # =====================================
    # DELETE EMPLOYEE
    # =====================================

    @staticmethod
    async def delete_employee(
        db: AsyncSession,
        employee_id: int
    ):

        employee = await db.get(
            ProfileInformation,
            employee_id
        )

        if not employee:

            return False

        await db.delete(employee)

        await db.commit()

        return True