from sqlalchemy import (
    select,
    func
)
# print("BOOK COPY SERVICE LOADED")
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_copy_model import (
    BookCopy
)
from app.models.book_model import Book

from app.models.library_floor_model import (
    LibraryFloor
)

from app.models.library_rack_model import (
    LibraryRack
)

from app.models.library_shelf_model import (
    LibraryShelf
)
from app.models.library_row_model import LibraryRow

from app.models.library_row_model import (
    LibraryRow
)
from app.schemas.book_copy_schema import AssignBookCopyLocation

from app.services.notification_service import (
    NotificationService
)
from app.utils.barcode_utils import BarcodeUtils


class BookCopyService:

    # =====================================
    # CREATE BOOK COPY
    # =====================================

    @staticmethod
    async def create_book_copy(
            db: AsyncSession,
            payload,
            created_by: int
    ):

        try:

            # -----------------------------
            # Validate Book
            # -----------------------------

            book = await db.get(
                Book,
                payload.book_id
            )

            if not book:
                raise ValueError(
                    "Selected book does not exist"
                )

            # -----------------------------
            # Validate Book Ownership
            # -----------------------------

            if (
                    book.school_id != payload.school_id
                    or
                    book.branch_id != payload.branch_id
                    or
                    book.library_id != payload.library_id
            ):
                raise ValueError(
                    "Book does not belong "
                    "to selected library"
                )

            # -----------------------------
            # Generate Copy Number
            # -----------------------------

            result = await db.execute(
                select(
                    func.max(BookCopy.copy_number)
                ).where(
                    BookCopy.book_id
                    == payload.book_id
                )
            )

            last_copy = result.scalar()

            copy_number = (
                1
                if last_copy is None
                else last_copy + 1
            )

            # -----------------------------
            # Generate Barcode
            # -----------------------------

            barcode = (
                f"BC-{payload.book_id:05d}-"
                f"{copy_number:03d}"
            )
            print(
                "CALLING BARCODE GENERATOR",
                flush=True
            )
            # print(
            #     "BARCODE URL =",
            #     barcode_image_url
            # )
            # print(
            #     "BARCODE URL =",
            #     barcode_image_url,
            #     flush=True
            # )

            barcode_image_url = (
                BarcodeUtils.generate_barcode(
                    barcode
                )
            )

            print("BARCODE URL =", barcode_image_url)
            # qr_code_url = (
            #     BarcodeUtils.generate_qrcode(
            #         barcode
            #     )
            # )

            # -----------------------------
            # Generate Accession Number
            # -----------------------------

            accession_number = (
                f"ACC-{payload.book_id:05d}-"
                f"{copy_number:03d}"
            )

            # -----------------------------
            # Create Book Copy
            # -----------------------------

            book_copy = BookCopy(

                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id,

                book_id=payload.book_id,
                barcode_image_url=barcode_image_url,

                # qr_code_url=qr_code_url,

                floor_id=None,
                rack_id=None,
                shelf_id=None,
                row_id=None,

                barcode=barcode,
                accession_number=accession_number,

                copy_number=copy_number,

                book_status="UNALLOCATED",

                acquisition_type=payload.acquisition_type,
                acquisition_price=payload.acquisition_price,
                acquisition_date=payload.acquisition_date,
                source_name=payload.source_name,

                is_reference_only=payload.is_reference_only,

                remarks=payload.remarks,


                created_by=created_by
            )

            db.add(book_copy)

            # -----------------------------
            # Update Inventory
            # -----------------------------

            book.quantity += 1
            book.available_copies += 1

            # -----------------------------
            # Low Stock Alert
            # -----------------------------

            book.low_stock_alert = (
                    book.available_copies
                    <=
                    book.minimum_threshold
            )

            await db.commit()

            await db.refresh(book_copy)

            # -----------------------------
            # Notification
            # -----------------------------

            await NotificationService.create_notification(
                db=db,
                title="Book Copy Created",
                message=(
                    f"Copy {barcode} "
                    f"added for {book.title}"
                ),
                notification_type="BOOK_COPY_CREATED",
                recipient_role="LIBRARIAN,ADMIN"
            )

            return book_copy

        except Exception:

            await db.rollback()
            raise

    @staticmethod
    async def get_all_book_copies(
            db: AsyncSession
    ):

        result = await db.execute(
            select(BookCopy).where(
                BookCopy.is_active == True
            )
        )

        return result.scalars().all()

    # =====================================
    # GET BOOK COPY BY ID
    # =====================================

    @staticmethod
    async def get_book_copy_by_id(
            db: AsyncSession,
            copy_id: int
    ):

        try:

            result = await db.execute(
                select(BookCopy).where(
                    BookCopy.id == copy_id,
                    BookCopy.is_active == True
                )
            )

            return result.scalar_one_or_none()

        except Exception:

            await db.rollback()
            raise

    # =====================================
    # UPDATE BOOK COPY
    # =====================================

    @staticmethod
    async def update_book_copy(
        db: AsyncSession,
        copy_id: int,
        payload,
        updated_by: int
    ):

        copy = await (
            BookCopyService
            .get_book_copy_by_id(
                db,
                copy_id
            )
        )

        if not copy:
            return None

        # -----------------------------
        # Update Location
        # -----------------------------

        if payload.floor_id is not None:
            copy.floor_id = payload.floor_id

        if payload.rack_id is not None:
            copy.rack_id = payload.rack_id

        if payload.shelf_id is not None:
            copy.shelf_id = payload.shelf_id

        if payload.row_id is not None:
            copy.row_id = payload.row_id

        # -----------------------------
        # Update Status
        # -----------------------------

        if payload.book_status is not None:
            copy.book_status = payload.book_status

        # -----------------------------
        # Update Acquisition
        # -----------------------------

        if payload.acquisition_type is not None:
            copy.acquisition_type = (
                payload.acquisition_type
            )

        if payload.acquisition_price is not None:
            copy.acquisition_price = (
                payload.acquisition_price
            )

        if payload.acquisition_date is not None:
            copy.acquisition_date = (
                payload.acquisition_date
            )

        if payload.source_name is not None:
            copy.source_name = (
                payload.source_name
            )

        # -----------------------------
        # Update Other Fields
        # -----------------------------

        if payload.is_reference_only is not None:
            copy.is_reference_only = (
                payload.is_reference_only
            )

        if payload.remarks is not None:
            copy.remarks = payload.remarks

        if payload.is_active is not None:
            copy.is_active = payload.is_active

        copy.updated_by = updated_by

        await db.commit()

        await db.refresh(copy)

        # -----------------------------
        # Notification
        # -----------------------------

        await NotificationService.create_notification(
            db=db,
            title="Book Copy Updated",
            message=(
                f"{copy.barcode} updated successfully"
            ),
            notification_type="BOOK_COPY_UPDATED",
            recipient_role="LIBRARIAN,ADMIN"
        )

        return copy

    # =====================================
    # DELETE BOOK COPY
    # =====================================

    @staticmethod
    async def delete_book_copy(
            db: AsyncSession,
            copy_id: int
    ):

        try:

            # ---------------------------------
            # Fetch Book Copy
            # ---------------------------------

            copy = await db.get(
                BookCopy,
                copy_id
            )

            if not copy:
                raise ValueError(
                    "Book copy not found"
                )

            # ---------------------------------
            # Already Deleted Check
            # ---------------------------------

            if not copy.is_active:
                raise ValueError(
                    "Book copy already deleted"
                )

            # ---------------------------------
            # Issued Book Check
            # ---------------------------------

            if copy.book_status == "ISSUED":
                raise ValueError(
                    "Issued book copy cannot be deleted"
                )

            # ---------------------------------
            # Fetch Book
            # ---------------------------------

            book = await db.get(
                Book,
                copy.book_id
            )

            if not book:
                raise ValueError(
                    "Book not found"
                )

            # ---------------------------------
            # Update Inventory
            # ---------------------------------

            if book.quantity > 0:
                book.quantity -= 1

            if (
                    copy.book_status == "AVAILABLE"
                    and
                    book.available_copies > 0
            ):
                book.available_copies -= 1

            # ---------------------------------
            # Low Stock Alert
            # ---------------------------------

            book.low_stock_alert = (
                    book.available_copies
                    <=
                    book.minimum_threshold
            )

            # ---------------------------------
            # Soft Delete Copy
            # ---------------------------------

            copy.is_active = False

            # Optional
            copy.updated_by = None

            barcode = copy.barcode

            # ---------------------------------
            # Save
            # ---------------------------------

            await db.commit()

            # ---------------------------------
            # Notification
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Book Copy Deleted",
                message=(
                    f"Book copy {barcode} "
                    f"deleted successfully"
                ),
                notification_type="BOOK_COPY_DELETED",
                recipient_role="LIBRARIAN,ADMIN"
            )

            return {
                "success": True,
                "message": (
                    f"Book copy {barcode} "
                    f"deleted successfully"
                )
            }

        except Exception:

            await db.rollback()
            raise

    @staticmethod
    async def assign_location(
            db: AsyncSession,
            payload: AssignBookCopyLocation
    ):

        try:

            # ---------------------------------
            # Validate Row
            # ---------------------------------

            row = await db.get(
                LibraryRow,
                payload.row_id
            )

            if not row:
                raise ValueError(
                    "Row not found"
                )

            # ---------------------------------
            # Validate Hierarchy
            # ---------------------------------

            if row.floor_id != payload.floor_id:
                raise ValueError(
                    "Selected row does not belong to floor"
                )

            if row.rack_id != payload.rack_id:
                raise ValueError(
                    "Selected row does not belong to rack"
                )

            if row.shelf_id != payload.shelf_id:
                raise ValueError(
                    "Selected row does not belong to shelf"
                )

            # ---------------------------------
            # Fetch Copies
            # ---------------------------------

            result = await db.execute(
                select(BookCopy).where(
                    BookCopy.id.in_(
                        payload.book_copy_ids
                    ),
                    BookCopy.is_active == True
                )
            )

            copies = result.scalars().all()

            if not copies:
                raise ValueError(
                    "No book copies found"
                )

            if len(copies) != len(payload.book_copy_ids):
                raise ValueError(
                    "One or more book copies not found"
                )

            # ---------------------------------
            # Validate Copies
            # ---------------------------------

            for copy in copies:

                if (
                        copy.school_id != row.school_id
                        or
                        copy.branch_id != row.branch_id
                        or
                        copy.library_id != row.library_id
                ):
                    raise ValueError(
                        f"Book copy {copy.barcode} "
                        f"does not belong to selected library"
                    )

                if copy.book_status in [
                    "ISSUED",
                    "LOST",
                    "DAMAGED"
                ]:
                    raise ValueError(
                        f"Book copy {copy.barcode} "
                        f"cannot be allocated because "
                        f"status is {copy.book_status}"
                    )

                if copy.row_id is not None:
                    raise ValueError(
                        f"Book copy {copy.barcode} "
                        f"is already allocated"
                    )

            # ---------------------------------
            # Capacity Validation
            # ---------------------------------

            result = await db.execute(
                select(
                    func.count(BookCopy.id)
                ).where(
                    BookCopy.row_id == payload.row_id,
                    BookCopy.is_active == True
                )
            )

            occupied = result.scalar() or 0

            required = len(copies)

            available_slots = (
                    row.capacity - occupied
            )

            if required > available_slots:
                raise ValueError(
                    f"Row capacity exceeded. "
                    f"Available slots: {available_slots}"
                )

            # ---------------------------------
            # Allocate Copies
            # ---------------------------------

            for copy in copies:
                copy.floor_id = payload.floor_id
                copy.rack_id = payload.rack_id
                copy.shelf_id = payload.shelf_id
                copy.row_id = payload.row_id

                copy.book_status = "AVAILABLE"

            await db.commit()

            return {
                "success": True,
                "message": (
                    f"{required} book copies "
                    f"allocated successfully"
                )
            }

        except Exception:

            await db.rollback()
            raise

    @staticmethod
    async def get_unassigned_copies(
            db: AsyncSession
    ):

        result = await db.execute(
            select(BookCopy)
            .where(
                BookCopy.row_id.is_(None),
                BookCopy.is_active == True
            )
            .order_by(
                BookCopy.id.asc()
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_copies_by_location(
            db: AsyncSession,
            floor_id: int,
            rack_id: int,
            shelf_id: int,
            row_id: int
    ):

        result = await db.execute(
            select(BookCopy)
            .where(
                BookCopy.floor_id == floor_id,
                BookCopy.rack_id == rack_id,
                BookCopy.shelf_id == shelf_id,
                BookCopy.row_id == row_id,
                BookCopy.is_active == True
            )
            .order_by(
                BookCopy.copy_number.asc()
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_book_copy_by_barcode(
            db: AsyncSession,
            barcode: str
    ):

        result = await db.execute(
            select(
                BookCopy,
                Book,
                LibraryFloor,
                LibraryRack,
                LibraryShelf,
                LibraryRow
            )
            .outerjoin(
                Book,
                Book.id == BookCopy.book_id
            )
            .outerjoin(
                LibraryFloor,
                LibraryFloor.id == BookCopy.floor_id
            )
            .outerjoin(
                LibraryRack,
                LibraryRack.id == BookCopy.rack_id
            )
            .outerjoin(
                LibraryShelf,
                LibraryShelf.id == BookCopy.shelf_id
            )
            .outerjoin(
                LibraryRow,
                LibraryRow.id == BookCopy.row_id
            )
            .where(
                BookCopy.barcode == barcode,
                BookCopy.is_active == True
            )
        )

        data = result.first()

        if not data:
            return None

        (
            copy,
            book,
            floor,
            rack,
            shelf,
            row
        ) = data

        return {
            "barcode": copy.barcode,
            "accession_number": copy.accession_number,

            "book_id": book.id,
            "copy_id": copy.id,

            "title": book.title,
            "author_name": book.author_name,
            "isbn_number": book.isbn_number,

            "publisher_name": book.publisher_name,
            "subject_name": book.subject_name,
            "language": book.language,

            "copy_number": copy.copy_number,
            "book_status": copy.book_status,

            "floor_name":
                floor.floor_name if floor else None,

            "rack_name":
                rack.rack_name if rack else None,

            "shelf_name":
                shelf.shelf_name if shelf else None,

            "row_name":
                row.row_name if row else None,

            "barcode_image_url":
                copy.barcode_image_url
        }

    @staticmethod
    async def get_barcode(
            db: AsyncSession,
            copy_id: int
    ):

        copy = await db.get(
            BookCopy,
            copy_id
        )

        if not copy:
            raise ValueError(
                "Book copy not found"
            )

        return {
            "barcode": copy.barcode,
            "barcode_image_url":
                copy.barcode_image_url
        }