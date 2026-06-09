from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.branch_model import Branch
from app.models.library_model import Library
from app.models.school_model import School
from app.services.notification_service import NotificationService


class LibraryService:

    @staticmethod
    async def create_library(
        db: AsyncSession,
        payload,
        created_by: int
    ):

        # =====================================
        # Duplicate Validation
        # =====================================

        existing = await db.execute(
            select(Library).where(
                Library.school_id == payload.school_id,
                Library.branch_id == payload.branch_id,
                Library.library_name == payload.library_name
            )
        )

        if existing.scalar_one_or_none():
            raise ValueError(
                "Library already exists in this branch"
            )

        # =====================================
        # Generate Library Code
        # =====================================

        result = await db.execute(
            select(Library)
        )

        count = len(
            result.scalars().all()
        ) + 1

        library_code = (
            f"LIB-{count:05d}"
        )

        # =====================================
        # Create Library
        # =====================================

        library = Library(
            school_id=payload.school_id,
            branch_id=payload.branch_id,

            library_code=library_code,
            library_name=payload.library_name,
            description=payload.description,

            creator_role=payload.creator_role,

            created_by=created_by
        )

        db.add(library)

        await db.commit()

        await db.refresh(library)
        # =====================================
        # Validate School
        # =====================================

        school = await db.get(
            School,
            payload.school_id
        )

        if not school:
            raise ValueError(
                "Selected school does not exist"
            )

        # =====================================
        # Validate Branch
        # =====================================

        branch = await db.get(
            Branch,
            payload.branch_id
        )

        if not branch:
            raise ValueError(
                "Selected branch does not exist"
            )

        # =====================================
        # Validate Branch Belongs To School
        # =====================================

        if branch.school_id != payload.school_id:
            raise ValueError(
                "Branch does not belong to selected school"
            )
        # =====================================
        # Notification
        # =====================================

        await NotificationService.create_notification(
            db=db,
            title="Library Created",
            message=f"{library.library_name} created successfully",
            notification_type="LIBRARY_CREATED",
            recipient_role="ADMIN"
            # recipient_role=payload.creator_role
        )

        return library

    @staticmethod
    async def get_all_libraries(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Library)
        )

        return result.scalars().all()

    @staticmethod
    async def get_library_by_id(
        db: AsyncSession,
        library_id: int
    ):

        result = await db.execute(
            select(Library).where(
                Library.id == library_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update_library(
        db: AsyncSession,
        library_id: int,
        payload
    ):

        library = await (
            LibraryService.get_library_by_id(
                db,
                library_id
            )
        )

        if not library:
            return None

        if payload.library_name is not None:
            library.library_name = payload.library_name

        if payload.description is not None:
            library.description = payload.description

        if payload.is_active is not None:
            library.is_active = payload.is_active

        await db.commit()

        await db.refresh(library)

        await NotificationService.create_notification(
            db=db,
            title="Library Updated",
            message=f"{library.library_name} updated successfully",
            notification_type="LIBRARY_UPDATED",
            recipient_role="ADMIN"
        )

        return library

    @staticmethod
    async def delete_library(
        db: AsyncSession,
        library_id: int
    ):

        library = await (
            LibraryService.get_library_by_id(
                db,
                library_id
            )
        )

        if not library:
            return False

        library_name = library.library_name

        await db.delete(library)

        await db.commit()

        await NotificationService.create_notification(
            db=db,
            title="Library Deleted",
            message=f"{library_name} deleted successfully",
            notification_type="LIBRARY_DELETED",
            recipient_role="ADMIN"
        )

        return True