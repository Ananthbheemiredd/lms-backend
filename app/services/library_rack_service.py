from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.library_rack_model import LibraryRack
from app.services.library_validator_service import LibraryValidatorService
from app.services.notification_service import NotificationService
from app.models.library_floor_model import LibraryFloor

class LibraryRackService:

    @staticmethod
    async def create_rack(
        db: AsyncSession,
        payload,
        created_by: int
    ):

        try:

            # ==========================
            # Duplicate Rack Validation
            # ==========================

            existing_rack = await db.execute(
                select(LibraryRack).where(
                    LibraryRack.floor_id == payload.floor_id,
                    LibraryRack.rack_name == payload.rack_name
                )
            )

            if existing_rack.scalar_one_or_none():

                raise ValueError(
                    "Rack already exists in this floor"
                )

            # ==========================
            # Generate Rack Code
            # ==========================

            result = await db.execute(
                select(LibraryRack)
            )

            rack_count = len(
                result.scalars().all()
            ) + 1

            rack_code = (
                f"RACK-{rack_count:05d}"
            )

            # ==========================
            # Create Rack
            # ==========================

            rack = LibraryRack(
                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id,
                floor_id=payload.floor_id,

                rack_code=rack_code,
                rack_name=payload.rack_name,

                description=payload.description,
                remarks=payload.remarks,

                creator_role=payload.creator_role,

                created_by=created_by
            )

            db.add(rack)

            await db.commit()

            await db.refresh(rack)
            floor = await db.get(
                LibraryFloor,
                payload.floor_id
            )

            if not floor:
                raise ValueError(
                    "Selected floor does not exist"
                )
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
                    "Selected floor does not exist for this school, branch and library"
                )



            # ==========================
            # Notification
            # ==========================

            await NotificationService.create_notification(
                db=db,
                title="Rack Created",
                message=f"{rack.rack_name} created successfully",
                notification_type="RACK_CREATED",
                recipient_role=rack.creator_role
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

            return rack

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_all_racks(
        db: AsyncSession
    ):

        result = await db.execute(
            select(LibraryRack).order_by(
                LibraryRack.id.desc()
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_rack_by_id(
        db: AsyncSession,
        rack_id: int
    ):

        result = await db.execute(
            select(LibraryRack).where(
                LibraryRack.id == rack_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_racks_by_floor(
        db: AsyncSession,
        floor_id: int
    ):

        result = await db.execute(
            select(LibraryRack).where(
                LibraryRack.floor_id == floor_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def update_rack(
        db: AsyncSession,
        rack_id: int,
        payload,
        updated_by: int
    ):

        try:

            rack = await (
                LibraryRackService
                .get_rack_by_id(
                    db,
                    rack_id
                )
            )

            if not rack:
                return None
            # ==========================
            # Floor Validation
            # ==========================

            target_school_id = (
                payload.school_id
                if hasattr(payload, "school_id")
                   and payload.school_id is not None
                else rack.school_id
            )

            target_branch_id = (
                payload.branch_id
                if hasattr(payload, "branch_id")
                   and payload.branch_id is not None
                else rack.branch_id
            )

            target_library_id = (
                payload.library_id
                if hasattr(payload, "library_id")
                   and payload.library_id is not None
                else rack.library_id
            )

            target_floor_id = (
                payload.floor_id
                if hasattr(payload, "floor_id")
                   and payload.floor_id is not None
                else rack.floor_id
            )

            floor_result = await db.execute(
                select(LibraryFloor).where(
                    LibraryFloor.id == target_floor_id,
                    LibraryFloor.school_id == target_school_id,
                    LibraryFloor.branch_id == target_branch_id,
                    LibraryFloor.library_id == target_library_id,
                    LibraryFloor.is_active == True
                )
            )

            floor = floor_result.scalar_one_or_none()

            if not floor:
                raise ValueError(
                    "Selected floor does not exist for this school, branch and library"
                )

            # ==========================
            # Duplicate Name Validation
            # ==========================

            if payload.rack_name:

                existing_rack = await db.execute(
                    select(LibraryRack).where(
                        LibraryRack.floor_id == rack.floor_id,
                        LibraryRack.rack_name == payload.rack_name,
                        LibraryRack.id != rack_id
                    )
                )

                if existing_rack.scalar_one_or_none():

                    raise ValueError(
                        "Rack name already exists"
                    )

                rack.rack_name = payload.rack_name

            if payload.description is not None:
                rack.description = payload.description

            if payload.remarks is not None:
                rack.remarks = payload.remarks

            if payload.is_active is not None:
                rack.is_active = payload.is_active

            rack.updated_by = updated_by

            await db.commit()

            await db.refresh(rack)

            # ==========================
            # Notification
            # ==========================

            await NotificationService.create_notification(
                db=db,
                title="Rack Updated",
                message=f"{rack.rack_name} updated successfully",
                notification_type="RACK_UPDATED",
                recipient_role=rack.creator_role
            )

            return rack

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def delete_rack(
        db: AsyncSession,
        rack_id: int
    ):

        try:

            rack = await (
                LibraryRackService
                .get_rack_by_id(
                    db,
                    rack_id
                )
            )

            if not rack:
                return False

            rack_name = rack.rack_name
            creator_role = rack.creator_role

            await db.delete(rack)

            await db.commit()

            # ==========================
            # Notification
            # ==========================

            await NotificationService.create_notification(
                db=db,
                title="Rack Deleted",
                message=f"{rack_name} deleted successfully",
                notification_type="RACK_DELETED",
                recipient_role=creator_role
            )

            return True

        except Exception:
            await db.rollback()
            raise