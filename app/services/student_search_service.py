from sqlalchemy import (
    select,
    or_
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student_model import (
    Student
)


class StudentSearchService:

    # =====================================
    # SEARCH STUDENTS
    # =====================================

    @staticmethod
    async def search_students(
        db: AsyncSession,
        keyword: str,
        school_id:int,
        branch_id:int
    ):

        result = await db.execute(
            select(Student).where(
                Student.school_id == school_id,
                Student.branch_id == branch_id,
                Student.is_active == True,


                or_(

                    Student.student_name.ilike(
                        f"%{keyword}%"
                    ),

                    Student.student_code.ilike(
                        f"%{keyword}%"
                    ),

                    Student.email.ilike(
                        f"%{keyword}%"
                    ),

                    Student.class_name.ilike(
                        f"%{keyword}%"
                    )
                )
            )
        )

        return result.scalars().all()