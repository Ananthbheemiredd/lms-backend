from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.branch_model import (
    Branch
)

from app.models.school_model import (
    School
)


class BranchService:

    # =====================================
    # CREATE BRANCH
    # =====================================

    @staticmethod
    async def create_branch(
        db: AsyncSession,
        payload
    ):

        school = await db.get(
            School,
            payload.school_id
        )

        if not school:

            raise ValueError(
                "School not found"
            )

        existing_branch = await db.execute(

            select(Branch).where(
                Branch.branch_code
                == payload.branch_code
            )
        )

        if existing_branch.scalar_one_or_none():

            raise ValueError(
                "Branch code already exists"
            )

        branch = Branch(

            school_id=payload.school_id,

            branch_code=payload.branch_code,

            branch_name=payload.branch_name,

            address=payload.address,

            is_active=payload.is_active
        )

        db.add(branch)

        await db.commit()

        await db.refresh(branch)

        return branch

    # =====================================
    # GET ALL BRANCHES
    # =====================================

    @staticmethod
    async def get_all_branches(
        db: AsyncSession
    ):

        result = await db.execute(

            select(Branch)

            .order_by(
                Branch.branch_name.asc()
            )
        )

        return result.scalars().all()

    # =====================================
    # GET BRANCHES BY SCHOOL
    # =====================================

    @staticmethod
    async def get_branches_by_school(
        db: AsyncSession,
        school_id: int
    ):

        result = await db.execute(

            select(Branch).where(
                Branch.school_id
                == school_id
            )
        )

        return result.scalars().all()

    # =====================================
    # UPDATE BRANCH
    # =====================================

    @staticmethod
    async def update_branch(
        db: AsyncSession,
        branch_id: int,
        payload
    ):

        branch = await db.get(
            Branch,
            branch_id
        )

        if not branch:

            raise ValueError(
                "Branch not found"
            )

        if payload.branch_name is not None:

            branch.branch_name = (
                payload.branch_name
            )

        if payload.address is not None:

            branch.address = (
                payload.address
            )

        if payload.is_active is not None:

            branch.is_active = (
                payload.is_active
            )

        await db.commit()

        await db.refresh(branch)

        return branch