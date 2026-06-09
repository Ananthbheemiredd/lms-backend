from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.library_floor_model import LibraryFloor
from app.models.library_rack_model import LibraryRack
from app.models.library_shelf_model import LibraryShelf
from app.services.library_validator_service import LibraryValidatorService

from app.services.notification_service import NotificationService


class LibraryShelfService:

    # =====================================
    # CREATE SHELF
    # =====================================

    @staticmethod
    async def create_shelf(
        db: AsyncSession,
        payload,
        created_by: int
    ):

        try:

            # ==========================
            # Floor Validation
            # ==========================

            floor_result = await db.execute(
                select(LibraryFloor).where(
                    LibraryFloor.id == payload.floor_id,
                    LibraryFloor.school_id == payload.school_id,
                    LibraryFloor.branch_id == payload.branch_id,
                    LibraryFloor.library_id == payload.library_id,
                    LibraryFloor.is_active == True
                )
            )

            floor = floor_result.scalar_one_or_none()

            if not floor:
                raise ValueError(
                    "Selected floor does not exist"
                )

            # ==========================
            # Rack Validation
            # ==========================

            rack_result = await db.execute(
                select(LibraryRack).where(
                    LibraryRack.id == payload.rack_id,
                    LibraryRack.floor_id == payload.floor_id,
                    LibraryRack.school_id == payload.school_id,
                    LibraryRack.branch_id == payload.branch_id,
                    LibraryRack.library_id == payload.library_id,
                    LibraryRack.is_active == True
                )
            )

            rack = rack_result.scalar_one_or_none()

            if not rack:
                raise ValueError(
                    "Selected rack does not exist"
                )

            # ==========================
            # Duplicate Shelf Validation
            # ==========================

            shelf_result = await db.execute(
                select(LibraryShelf).where(
                    LibraryShelf.rack_id == payload.rack_id,
                    LibraryShelf.shelf_name == payload.shelf_name
                )
            )

            if shelf_result.scalar_one_or_none():
                raise ValueError(
                    "Shelf already exists in this rack"
                )

            # ==========================
            # Generate Shelf Code
            # ==========================

            result = await db.execute(
                select(LibraryShelf)
            )

            shelf_count = len(
                result.scalars().all()
            ) + 1

            shelf_code = (
                f"SHLF-{shelf_count:05d}"
            )

            # ==========================
            # Create Shelf
            # ==========================

            shelf = LibraryShelf(
                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id,
                floor_id=payload.floor_id,
                rack_id=payload.rack_id,

                shelf_code=shelf_code,
                shelf_name=payload.shelf_name,

                description=payload.description,
                remarks=payload.remarks,

                creator_role=payload.creator_role,

                created_by=created_by
            )

            db.add(shelf)

            await db.commit()

            await db.refresh(shelf)

            # ==========================
            # Notification
            # ==========================

            await NotificationService.create_notification(
                db=db,
                title="Shelf Created",
                message=f"{shelf.shelf_name} created successfully",
                notification_type="SHELF_CREATED",
                recipient_role=shelf.creator_role
            )

            return shelf

        except Exception:
            await db.rollback()
            raise

    # =====================================
    # GET ALL SHELVES
    # =====================================

    @staticmethod
    async def get_all_shelves(
        db: AsyncSession
    ):

        result = await db.execute(
            select(LibraryShelf).order_by(
                LibraryShelf.id.desc()
            )
        )

        return result.scalars().all()

    # =====================================
    # GET SHELF BY ID
    # =====================================

    @staticmethod
    async def get_shelf_by_id(
        db: AsyncSession,
        shelf_id: int
    ):

        result = await db.execute(
            select(LibraryShelf).where(
                LibraryShelf.id == shelf_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================
    # GET SHELVES BY RACK
    # =====================================

    @staticmethod
    async def get_shelves_by_rack(
        db: AsyncSession,
        rack_id: int
    ):

        result = await db.execute(
            select(LibraryShelf).where(
                LibraryShelf.rack_id == rack_id
            )
        )

        return result.scalars().all()

    # =====================================
    # UPDATE SHELF
    # =====================================

    @staticmethod
    async def update_shelf(
        db: AsyncSession,
        shelf_id: int,
        payload,
        updated_by: int
    ):

        try:

            shelf = await (
                LibraryShelfService
                .get_shelf_by_id(
                    db,
                    shelf_id
                )
            )

            if not shelf:
                return None

            if payload.shelf_name:

                existing_shelf = await db.execute(
                    select(LibraryShelf).where(
                        LibraryShelf.rack_id == shelf.rack_id,
                        LibraryShelf.shelf_name == payload.shelf_name,
                        LibraryShelf.id != shelf_id
                    )
                )

                if existing_shelf.scalar_one_or_none():

                    raise ValueError(
                        "Shelf name already exists"
                    )

                shelf.shelf_name = payload.shelf_name

            if payload.description is not None:
                shelf.description = payload.description

            if payload.remarks is not None:
                shelf.remarks = payload.remarks

            if payload.is_active is not None:
                shelf.is_active = payload.is_active

            shelf.updated_by = updated_by

            await db.commit()

            await db.refresh(shelf)

            await NotificationService.create_notification(
                db=db,
                title="Shelf Updated",
                message=f"{shelf.shelf_name} updated successfully",
                notification_type="SHELF_UPDATED",
                recipient_role=shelf.creator_role
            )

            await LibraryValidatorService.validate_hierarchy(
                db=db,
                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id
            )

            await LibraryValidatorService.validate_floor(
                db=db,
                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id,
                floor_id=payload.floor_id
            )

            await LibraryValidatorService.validate_rack(
                db=db,
                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id,
                floor_id=payload.floor_id,
                rack_id=payload.rack_id
            )

            return shelf

        except Exception:
            await db.rollback()
            raise

    # =====================================
    # DELETE SHELF
    # =====================================

    @staticmethod
    async def delete_shelf(
        db: AsyncSession,
        shelf_id: int
    ):

        try:

            shelf = await (
                LibraryShelfService
                .get_shelf_by_id(
                    db,
                    shelf_id
                )
            )

            if not shelf:
                return False

            shelf_name = shelf.shelf_name
            creator_role = shelf.creator_role

            await db.delete(shelf)

            await db.commit()

            await NotificationService.create_notification(
                db=db,
                title="Shelf Deleted",
                message=f"{shelf_name} deleted successfully",
                notification_type="SHELF_DELETED",
                recipient_role=creator_role
            )

            return True

        except Exception:
            await db.rollback()
            raise