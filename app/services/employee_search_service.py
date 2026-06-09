from sqlalchemy import (
    select,
    or_
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile_information_model import (
    ProfileInformation
)


class EmployeeSearchService:

    # =====================================
    # SEARCH EMPLOYEES
    # =====================================

    @staticmethod
    async def search_employees(
        db: AsyncSession,
        keyword: str,
        school_id: int,
        branch_id: int,
    ):

        result = await db.execute(
            select(ProfileInformation).where(
                ProfileInformation.school_id
                == school_id,

                ProfileInformation.branch_id
                == branch_id,

                ProfileInformation.is_active
                == True,
                or_(

                    ProfileInformation.employee_name.ilike(
                        f"%{keyword}%"
                    ),

                    ProfileInformation.employee_code.ilike(
                        f"%{keyword}%"
                    ),

                    ProfileInformation.email.ilike(
                        f"%{keyword}%"
                    ),

                    ProfileInformation.department_name.ilike(
                        f"%{keyword}%"
                    ),

                    ProfileInformation.designation.ilike(
                        f"%{keyword}%"
                    )
                )
            )
        )

        return result.scalars().all()