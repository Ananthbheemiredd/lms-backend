from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.library_floor_model import LibraryFloor
from app.models.library_model import Library
from app.services.notification_service import NotificationService

from app.services.library_validator_service import (
    LibraryValidatorService
)
class LibraryFloorService:

    @staticmethod
    async def create_floor(
        db: AsyncSession,
        payload,
        created_by: int
    ):

        try:

            existing_floor = await db.execute(
                select(LibraryFloor).where(
                    LibraryFloor.school_id == payload.school_id,
                    LibraryFloor.branch_id == payload.branch_id,
                    LibraryFloor.library_id == payload.library_id,
                    LibraryFloor.floor_name == payload.floor_name
                )
            )

            if existing_floor.scalar_one_or_none():
                raise ValueError(
                    "Floor already exists in this library"
                )

            result = await db.execute(
                select(LibraryFloor)
            )

            floor_count = len(
                result.scalars().all()
            ) + 1

            floor_code = f"FLR-{floor_count:05d}"

            floor = LibraryFloor(
                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id,
                floor_code=floor_code,
                floor_name=payload.floor_name,
                description=payload.description,
                creator_role=payload.creator_role,
                created_by=created_by
            )

            db.add(floor)

            await db.commit()

            await db.refresh(floor)


            # =====================================
            # Validate Library
            # =====================================

            library = await db.get(
                Library,
                payload.library_id
            )

            if not library:
                raise ValueError(
                    "Selected library does not exist"
                )

            # =====================================
            # Validate Library Belongs To School
            # =====================================

            if library.school_id != payload.school_id:
                raise ValueError(
                    "Library does not belong to selected school"
                )

            # =====================================
            # Validate Library Belongs To Branch
            # =====================================

            if library.branch_id != payload.branch_id:
                raise ValueError(
                    "Library does not belong to selected branch"
                )

            await NotificationService.create_notification(
                db=db,
                title="Floor Created",
                message=f"{floor.floor_name} created successfully",
                notification_type="FLOOR_CREATED",
                recipient_role=floor.creator_role
            )

            await LibraryValidatorService.validate_hierarchy(
                db=db,
                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id
            )



            return floor

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_all_floors(
        db: AsyncSession
    ):

        result = await db.execute(
            select(LibraryFloor).order_by(
                LibraryFloor.id.desc()
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_floor_by_id(
        db: AsyncSession,
        floor_id: int
    ):

        result = await db.execute(
            select(LibraryFloor).where(
                LibraryFloor.id == floor_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update_floor(
        db: AsyncSession,
        floor_id: int,
        payload,
        updated_by: int
    ):

        try:

            floor = await LibraryFloorService.get_floor_by_id(
                db,
                floor_id
            )

            if not floor:
                return None

            if payload.floor_name:

                existing_floor = await db.execute(
                    select(LibraryFloor).where(
                        LibraryFloor.school_id == floor.school_id,
                        LibraryFloor.branch_id == floor.branch_id,
                        LibraryFloor.library_id == floor.library_id,
                        LibraryFloor.floor_name == payload.floor_name,
                        LibraryFloor.id != floor_id
                    )
                )

                if existing_floor.scalar_one_or_none():
                    raise ValueError(
                        "Floor name already exists"
                    )

                floor.floor_name = payload.floor_name

            if payload.description is not None:
                floor.description = payload.description

            if payload.is_active is not None:
                floor.is_active = payload.is_active

            floor.updated_by = updated_by

            await db.commit()

            await db.refresh(floor)

            await NotificationService.create_notification(
                db=db,
                title="Floor Updated",
                message=f"{floor.floor_name} updated successfully",
                notification_type="FLOOR_UPDATED",
                recipient_role=floor.creator_role
            )

            return floor

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def delete_floor(
        db: AsyncSession,
        floor_id: int
    ):

        try:

            floor = await LibraryFloorService.get_floor_by_id(
                db,
                floor_id
            )

            if not floor:
                return False

            floor_name = floor.floor_name
            creator_role = floor.creator_role

            await db.delete(floor)

            await db.commit()

            await NotificationService.create_notification(
                db=db,
                title="Floor Deleted",
                message=f"{floor_name} deleted successfully",
                notification_type="FLOOR_DELETED",
                recipient_role=creator_role
            )

            return True

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_floors_by_library(
        db: AsyncSession,
        library_id: int
    ):

        result = await db.execute(
            select(LibraryFloor).where(
                LibraryFloor.library_id == library_id
            )
        )

        return result.scalars().all()