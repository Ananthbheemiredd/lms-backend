from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.school_model import School
from app.models.branch_model import Branch
from app.models.library_model import Library
from app.models.library_floor_model import LibraryFloor
from app.models.library_rack_model import LibraryRack
from app.models.library_shelf_model import LibraryShelf


class LibraryValidatorService:

    # =====================================
    # SCHOOL
    # =====================================

    @staticmethod
    async def validate_school(
        db: AsyncSession,
        school_id: int
    ):

        school = await db.get(
            School,
            school_id
        )

        if not school:
            raise ValueError(
                "School does not exist"
            )

        return school

    # =====================================
    # BRANCH
    # =====================================

    @staticmethod
    async def validate_branch(
        db: AsyncSession,
        school_id: int,
        branch_id: int
    ):

        result = await db.execute(
            select(Branch).where(
                Branch.id == branch_id,
                Branch.school_id == school_id
            )
        )

        branch = result.scalar_one_or_none()

        if not branch:
            raise ValueError(
                "Branch does not belong to selected school"
            )

        return branch

    # =====================================
    # LIBRARY
    # =====================================

    @staticmethod
    async def validate_library(
        db: AsyncSession,
        school_id: int,
        branch_id: int,
        library_id: int
    ):

        result = await db.execute(
            select(Library).where(
                Library.id == library_id,
                Library.school_id == school_id,
                Library.branch_id == branch_id
            )
        )

        library = result.scalar_one_or_none()

        if not library:
            raise ValueError(
                "Library does not belong to selected school and branch"
            )

        return library

    # =====================================
    # FLOOR
    # =====================================

    @staticmethod
    async def validate_floor(
        db: AsyncSession,
        school_id: int,
        branch_id: int,
        library_id: int,
        floor_id: int
    ):

        result = await db.execute(
            select(LibraryFloor).where(
                LibraryFloor.id == floor_id,
                LibraryFloor.school_id == school_id,
                LibraryFloor.branch_id == branch_id,
                LibraryFloor.library_id == library_id,
                LibraryFloor.is_active == True
            )
        )

        floor = result.scalar_one_or_none()

        if not floor:
            raise ValueError(
                "Floor does not exist"
            )

        return floor

    # =====================================
    # RACK
    # =====================================

    @staticmethod
    async def validate_rack(
        db: AsyncSession,
        school_id: int,
        branch_id: int,
        library_id: int,
        floor_id: int,
        rack_id: int
    ):

        result = await db.execute(
            select(LibraryRack).where(
                LibraryRack.id == rack_id,
                LibraryRack.school_id == school_id,
                LibraryRack.branch_id == branch_id,
                LibraryRack.library_id == library_id,
                LibraryRack.floor_id == floor_id,
                LibraryRack.is_active == True
            )
        )

        rack = result.scalar_one_or_none()

        if not rack:
            raise ValueError(
                "Rack does not exist"
            )

        return rack

    # =====================================
    # SHELF
    # =====================================

    @staticmethod
    async def validate_shelf(
        db: AsyncSession,
        school_id: int,
        branch_id: int,
        library_id: int,
        floor_id: int,
        rack_id: int,
        shelf_id: int
    ):

        result = await db.execute(
            select(LibraryShelf).where(
                LibraryShelf.id == shelf_id,
                LibraryShelf.school_id == school_id,
                LibraryShelf.branch_id == branch_id,
                LibraryShelf.library_id == library_id,
                LibraryShelf.floor_id == floor_id,
                LibraryShelf.rack_id == rack_id,
                LibraryShelf.is_active == True
            )
        )

        shelf = result.scalar_one_or_none()

        if not shelf:
            raise ValueError(
                "Shelf does not exist"
            )

        return shelf

    # =====================================
    # COMPLETE HIERARCHY
    # =====================================

    @staticmethod
    async def validate_hierarchy(
        db: AsyncSession,
        school_id: int,
        branch_id: int,
        library_id: int
    ):

        await LibraryValidatorService.validate_school(
            db,
            school_id
        )

        await LibraryValidatorService.validate_branch(
            db,
            school_id,
            branch_id
        )

        await LibraryValidatorService.validate_library(
            db,
            school_id,
            branch_id,
            library_id
        )

        return True