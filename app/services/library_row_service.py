from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.library_row_model import LibraryRow
from app.models.library_shelf_model import LibraryShelf

from app.services.notification_service import (
    NotificationService
)


class LibraryRowService:

    # =====================================
    # CREATE ROW
    # =====================================

    @staticmethod
    async def create_row(
        db: AsyncSession,
        payload,
        created_by: int
    ):

        # -----------------------------
        # Validate Shelf
        # -----------------------------

        shelf = await db.get(
            LibraryShelf,
            payload.shelf_id
        )

        if not shelf:
            raise ValueError(
                "Selected shelf does not exist"
            )

        if shelf.school_id != payload.school_id:
            raise ValueError(
                "Shelf does not belong to selected school"
            )

        if shelf.branch_id != payload.branch_id:
            raise ValueError(
                "Shelf does not belong to selected branch"
            )

        if shelf.library_id != payload.library_id:
            raise ValueError(
                "Shelf does not belong to selected library"
            )

        if shelf.floor_id != payload.floor_id:
            raise ValueError(
                "Shelf does not belong to selected floor"
            )

        if shelf.rack_id != payload.rack_id:
            raise ValueError(
                "Shelf does not belong to selected rack"
            )

        # -----------------------------
        # Duplicate Validation
        # -----------------------------

        existing = await db.execute(
            select(LibraryRow).where(
                LibraryRow.shelf_id == payload.shelf_id,
                LibraryRow.row_name == payload.row_name
            )
        )

        if existing.scalar_one_or_none():

            raise ValueError(
                "Row already exists in this shelf"
            )

        # -----------------------------
        # Generate Row Code
        # -----------------------------

        result = await db.execute(
            select(LibraryRow)
        )

        count = len(
            result.scalars().all()
        ) + 1

        row_code = (
            f"ROW-{count:05d}"
        )

        # -----------------------------
        # Create Row
        # -----------------------------

        row = LibraryRow(
            school_id=payload.school_id,
            branch_id=payload.branch_id,
            library_id=payload.library_id,

            floor_id=payload.floor_id,
            rack_id=payload.rack_id,
            shelf_id=payload.shelf_id,

            row_code=row_code,
            row_name=payload.row_name,

            capacity=payload.capacity,
            description=payload.description,

            creator_role=payload.creator_role,

            created_by=created_by
        )

        db.add(row)

        await db.commit()

        await db.refresh(row)

        # -----------------------------
        # Notification
        # -----------------------------

        await NotificationService.create_notification(
            db=db,
            title="Row Created",
            message=f"{row.row_name} created successfully",
            notification_type="ROW_CREATED",
            recipient_role=payload.creator_role
        )

        return row

    # =====================================
    # GET ALL ROWS
    # =====================================

    @staticmethod
    async def get_all_rows(
        db: AsyncSession
    ):

        result = await db.execute(
            select(LibraryRow)
        )

        return result.scalars().all()

    # =====================================
    # GET ROW BY ID
    # =====================================

    @staticmethod
    async def get_row_by_id(
        db: AsyncSession,
        row_id: int
    ):

        result = await db.execute(
            select(LibraryRow).where(
                LibraryRow.id == row_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================
    # GET ROWS BY SHELF
    # =====================================

    @staticmethod
    async def get_rows_by_shelf(
        db: AsyncSession,
        shelf_id: int
    ):

        result = await db.execute(
            select(LibraryRow).where(
                LibraryRow.shelf_id == shelf_id
            )
        )

        return result.scalars().all()

    # =====================================
    # UPDATE ROW
    # =====================================

    @staticmethod
    async def update_row(
        db: AsyncSession,
        row_id: int,
        payload,
        updated_by: int
    ):

        row = await (
            LibraryRowService
            .get_row_by_id(
                db,
                row_id
            )
        )

        if not row:
            return None

        if payload.row_name is not None:
            row.row_name = payload.row_name

        if payload.capacity is not None:
            row.capacity = payload.capacity

        if payload.description is not None:
            row.description = payload.description

        if payload.is_active is not None:
            row.is_active = payload.is_active

        row.updated_by = updated_by

        await db.commit()

        await db.refresh(row)

        await NotificationService.create_notification(
            db=db,
            title="Row Updated",
            message=f"{row.row_name} updated successfully",
            notification_type="ROW_UPDATED",
            recipient_role=row.creator_role
        )

        return row

    # =====================================
    # DELETE ROW
    # =====================================

    @staticmethod
    async def delete_row(
        db: AsyncSession,
        row_id: int
    ):

        row = await (
            LibraryRowService
            .get_row_by_id(
                db,
                row_id
            )
        )

        if not row:
            return False

        row_name = row.row_name
        role = row.creator_role

        await db.delete(row)

        await db.commit()

        await NotificationService.create_notification(
            db=db,
            title="Row Deleted",
            message=f"{row_name} deleted successfully",
            notification_type="ROW_DELETED",
            recipient_role=role
        )

        return True