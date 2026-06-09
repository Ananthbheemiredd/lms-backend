from sqlalchemy import (
    select,
    func
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.book_model import (
    Book
)

from app.models.book_stock_request_model import (
    BookStockRequest
)



from app.models.book_copy_model import (
    BookCopy
)
from app.schemas.stock_transaction_schema import StockTransactionCreate

from app.services.notification_service import (
    NotificationService
)
from app.services.stock_transaction_service import StockTransactionService


class BookStockRequestService:

    # =====================================
    # CREATE STOCK REQUEST
    # =====================================

    @staticmethod
    async def create_stock_request(
        db: AsyncSession,
        payload
    ):

        # ---------------------------------
        # CHECK BOOK
        # ---------------------------------

        book = await db.get(
            Book,
            payload.book_id
        )

        if not book:

            raise ValueError(
                "Book not found"
            )

        # ---------------------------------
        # CREATE REQUEST
        # ---------------------------------

        request = BookStockRequest(

            product_id=payload.product_id,

            book_id=payload.book_id,

            requested_quantity=(
                payload.requested_quantity
            ),

            requested_by=payload.requested_by,

            remarks=payload.remarks
        )

        db.add(request)

        await db.commit()

        await db.refresh(request)

        # ---------------------------------
        # SEND NOTIFICATION
        # ---------------------------------

        await NotificationService.create_notification(
            db=db,
            title="Stock Request Created",
            message=(
                f"Stock request created for "
                f"{book.title}"
            ),
            notification_type="STOCK_REQUEST",
            creator_role="LIBRARIAN"
        )

        return request

    # =====================================
    # GET ALL REQUESTS
    # =====================================

    @staticmethod
    async def get_all_requests(
            db: AsyncSession,
            status: str | None = None
    ):

        query = select(
            BookStockRequest
        )

        if status:
            query = query.where(
                BookStockRequest.request_status
                == status
            )

        result = await db.execute(
            query.order_by(
                BookStockRequest.created_at.desc()
            )
        )

        return result.scalars().all()

    # =====================================
    # APPROVE REQUEST
    # =====================================

    @staticmethod
    async def approve_request(
            db: AsyncSession,
            request_id: int,
            payload
    ):

        try:

            # ---------------------------------
            # Fetch Request
            # ---------------------------------

            request = await db.get(
                BookStockRequest,
                request_id
            )

            if not request:
                raise ValueError(
                    "Stock request not found"
                )

            # ---------------------------------
            # Status Validation
            # ---------------------------------

            if request.request_status != "PENDING":
                raise ValueError(
                    "Request already processed"
                )

            # ---------------------------------
            # Book Validation
            # ---------------------------------

            book = await db.get(
                Book,
                request.book_id
            )

            if not book:
                raise ValueError(
                    "Book not found"
                )

            if not book.is_active:
                raise ValueError(
                    "Book is inactive"
                )

            # ---------------------------------
            # Quantity Validation
            # ---------------------------------

            if payload.approved_quantity <= 0:
                raise ValueError(
                    "Approved quantity must be greater than zero"
                )

            if (
                    payload.approved_quantity
                    >
                    request.requested_quantity
            ):
                raise ValueError(
                    "Approved quantity cannot exceed requested quantity"
                )

            # ---------------------------------
            # Approve Request
            # ---------------------------------

            request.request_status = "APPROVED"

            request.approved_quantity = (
                payload.approved_quantity
            )

            request.approved_by = (
                payload.approved_by
            )

            request.remarks = (
                payload.remarks
            )

            await db.commit()

            await db.refresh(request)

            # ---------------------------------
            # Notification - Admin
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Stock Request Approved",
                message=(
                    f"Stock request #{request.id} "
                    f"approved for "
                    f"{payload.approved_quantity} copies"
                ),
                notification_type="STOCK_APPROVAL",
                recipient_role="ADMIN"
            )

            # ---------------------------------
            # Notification - Librarian
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Stock Request Approved",
                message=(
                    f"Stock request #{request.id} "
                    f"approved for "
                    f"{payload.approved_quantity} copies"
                ),
                notification_type="STOCK_APPROVAL",
                recipient_role="LIBRARIAN"
            )

            return request

        except Exception:

            await db.rollback()
            raise

    # =====================================
    # REJECT REQUEST
    # =====================================

    @staticmethod
    async def reject_request(
            db: AsyncSession,
            request_id: int,
            payload
    ):

        try:

            # ---------------------------------
            # Fetch Request
            # ---------------------------------

            request = await db.get(
                BookStockRequest,
                request_id
            )

            if not request:
                raise ValueError(
                    "Stock request not found"
                )

            # ---------------------------------
            # Status Validation
            # ---------------------------------

            if request.request_status != "PENDING":
                raise ValueError(
                    "Request already processed"
                )

            # ---------------------------------
            # Fetch Book
            # ---------------------------------

            book = await db.get(
                Book,
                request.book_id
            )

            if not book:
                raise ValueError(
                    "Book not found"
                )

            # ---------------------------------
            # Remarks Validation
            # ---------------------------------

            if (
                    not payload.rejection_reason
                    or
                    not payload.rejection_reason.strip()
            ):
                raise ValueError(
                    "Rejection remarks are required"
                )

            # ---------------------------------
            # Reject Request
            # ---------------------------------

            request.request_status = "REJECTED"

            request.approved_by = (
                payload.approved_by
            )

            request.approved_quantity = 0

            request.rejection_reason = (
                payload.rejection_reason
            )

            request.remarks = (
                payload.rejection_reason
            )

            await db.commit()

            await db.refresh(request)

            # ---------------------------------
            # Notification - Admin
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Stock Request Rejected",
                message=(
                    f"Stock request #{request.id} "
                    f"has been rejected"
                ),
                notification_type="STOCK_REJECTION",
                recipient_role="ADMIN"
            )

            # ---------------------------------
            # Notification - Librarian
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Stock Request Rejected",
                message=(
                    f"Stock request #{request.id} "
                    f"has been rejected"
                ),
                notification_type="STOCK_REJECTION",
                recipient_role="LIBRARIAN"
            )

            return request

        except Exception:

            await db.rollback()
            raise

    @staticmethod
    async def get_request_by_id(
            db: AsyncSession,
            request_id: int
    ):

        request = await db.get(
            BookStockRequest,
            request_id
        )

        if not request:
            raise ValueError(
                "Stock request not found"
            )

        return request
    # =====================================
    # COMPLETE REQUEST
    # =====================================

    @staticmethod
    async def complete_request(
            db: AsyncSession,
            request_id: int,
            payload
    ):

        try:

            # ---------------------------------
            # Fetch Request
            # ---------------------------------

            request = await db.get(
                BookStockRequest,
                request_id
            )

            if not request:
                raise ValueError(
                    "Stock request not found"
                )

            if request.request_status != "APPROVED":
                raise ValueError(
                    "Only approved requests can be completed"
                )

            # ---------------------------------
            # Fetch Book
            # ---------------------------------

            book = await db.get(
                Book,
                request.book_id
            )

            if not book:
                raise ValueError(
                    "Book not found"
                )

            if not book.is_active:
                raise ValueError(
                    "Book is inactive"
                )

            # ---------------------------------
            # Quantity Validation
            # ---------------------------------

            if (
                    not request.approved_quantity
                    or
                    request.approved_quantity <= 0
            ):
                raise ValueError(
                    "Approved quantity is invalid"
                )

            # ---------------------------------
            # Current Copy Count
            # ---------------------------------

            result = await db.execute(
                select(
                    func.max(BookCopy.copy_number)
                ).where(
                    BookCopy.book_id == book.id
                )
            )

            last_copy_number = (
                    result.scalar() or 0
            )

            # ---------------------------------
            # Update Inventory
            # ---------------------------------

            book.quantity += (
                request.approved_quantity
            )

            book.available_copies += (
                request.approved_quantity
            )

            # ---------------------------------
            # Create Book Copies
            # ---------------------------------

            for i in range(
                    request.approved_quantity
            ):
                copy_number = (
                        last_copy_number
                        + i + 1
                )

                copy = BookCopy(

                    school_id=book.school_id,
                    branch_id=book.branch_id,
                    library_id=book.library_id,

                    book_id=book.id,

                    barcode=(
                        f"BC-{book.id:05d}-"
                        f"{copy_number:03d}"
                    ),

                    accession_number=(
                        f"ACC-{book.id:05d}-"
                        f"{copy_number:03d}"
                    ),

                    copy_number=copy_number,

                    floor_id=None,
                    rack_id=None,
                    shelf_id=None,
                    row_id=None,

                    book_status="UNALLOCATED",

                    is_active=True,

                    created_by=payload.approved_by
                )

                db.add(copy)

            # ---------------------------------
            # Update Request
            # ---------------------------------

            request.request_status = (
                "COMPLETED"
            )

            request.approved_by = payload.approved_by

            request.remarks = (
                payload.remarks
            )

            # ---------------------------------
            # Save
            # ---------------------------------

            await db.commit()

            await db.refresh(request)

            # ---------------------------------
            # Notifications
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Stock Request Completed",
                message=(
                    f"{request.approved_quantity} "
                    f"copies added for "
                    f"{book.title}"
                ),
                notification_type="STOCK_COMPLETED",
                recipient_role="ADMIN"
            )

            await NotificationService.create_notification(
                db=db,
                title="Stock Request Completed",
                message=(
                    f"{request.approved_quantity} "
                    f"copies added for "
                    f"{book.title}"
                ),
                notification_type="STOCK_COMPLETED",
                recipient_role="LIBRARIAN"
            )

            await StockTransactionService.create_transaction(
                db=db,
                payload=StockTransactionCreate(
                    product_id=request.product_id,
                    book_id=request.book_id,
                    transaction_type="STOCK_IN",
                    quantity=request.approved_quantity,
                    reference_id=request.id,
                    created_by=payload.approved_by
                )
            )
            return request

        except Exception:

            await db.rollback()
            raise

    @staticmethod
    async def delete_request(
            db: AsyncSession,
            request_id: int
    ):

        request = await db.get(
            BookStockRequest,
            request_id
        )

        if not request:
            raise ValueError(
                "Stock request not found"
            )

        await db.delete(request)

        await db.commit()

        return True