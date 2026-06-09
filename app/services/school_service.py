from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.school_model import (
    School
)


class SchoolService:

    # =====================================
    # CREATE SCHOOL
    # =====================================

    @staticmethod
    async def create_school(
        db: AsyncSession,
        payload
    ):

        existing_school = await db.execute(

            select(School).where(
                School.school_code
                == payload.school_code
            )
        )

        if existing_school.scalar_one_or_none():

            raise ValueError(
                "School code already exists"
            )

        school = School(

            school_code=payload.school_code,

            school_name=payload.school_name,

            address=payload.address,

            is_active=payload.is_active
        )

        db.add(school)

        await db.commit()

        await db.refresh(school)

        return school

    # =====================================
    # GET ALL SCHOOLS
    # =====================================

    @staticmethod
    async def get_all_schools(
        db: AsyncSession
    ):

        result = await db.execute(

            select(School)

            .order_by(
                School.school_name.asc()
            )
        )

        return result.scalars().all()

    # =====================================
    # GET SCHOOL BY ID
    # =====================================

    @staticmethod
    async def get_school_by_id(
        db: AsyncSession,
        school_id: int
    ):

        school = await db.get(
            School,
            school_id
        )

        if not school:

            raise ValueError(
                "School not found"
            )

        return school

    # =====================================
    # UPDATE SCHOOL
    # =====================================

    @staticmethod
    async def update_school(
        db: AsyncSession,
        school_id: int,
        payload
    ):

        school = await db.get(
            School,
            school_id
        )

        if not school:

            raise ValueError(
                "School not found"
            )

        if payload.school_name is not None:

            school.school_name = (
                payload.school_name
            )

        if payload.address is not None:

            school.address = (
                payload.address
            )

        if payload.is_active is not None:

            school.is_active = (
                payload.is_active
            )

        await db.commit()

        await db.refresh(school)

        return school