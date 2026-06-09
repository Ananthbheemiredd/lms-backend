from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.student_model import (
    Student
)

from app.schemas.student_schema import (
    StudentCreate,
    StudentUpdate
)


class StudentService:

    # =====================================
    # CREATE STUDENT
    # =====================================

    @staticmethod
    async def create_student(
        db: AsyncSession,
        payload: StudentCreate
    ):

        student = Student(
            school_id=payload.school_id,
            branch_id=payload.branch_id,

            student_code=payload.student_code,

            student_name=payload.student_name,

            email=payload.email,

            mobile_number=payload.mobile_number,

            class_name=payload.class_name,

            section_name=payload.section_name
        )

        db.add(student)

        await db.commit()

        await db.refresh(student)

        return student

    # =====================================
    # GET ALL STUDENTS
    # =====================================

    @staticmethod
    async def get_all_students(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Student)
        )

        return result.scalars().all()

    # =====================================
    # GET STUDENT BY ID
    # =====================================

    @staticmethod
    async def get_student_by_id(
        db: AsyncSession,
        student_id: int
    ):

        result = await db.execute(
            select(Student).where(
                Student.id == student_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================
    # UPDATE STUDENT
    # =====================================

    @staticmethod
    async def update_student(
        db: AsyncSession,
        student_id: int,
        payload: StudentUpdate
    ):

        student = await db.get(
            Student,
            student_id
        )

        if not student:

            return None

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )

        for key, value in update_data.items():

            setattr(
                student,
                key,
                value
            )

        await db.commit()

        await db.refresh(student)

        return student

    # =====================================
    # DELETE STUDENT
    # =====================================

    @staticmethod
    async def delete_student(
        db: AsyncSession,
        student_id: int
    ):

        student = await db.get(
            Student,
            student_id
        )

        if not student:

            return False

        await db.delete(student)

        await db.commit()

        return True