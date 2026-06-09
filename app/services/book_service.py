from dataclasses import Field
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_copy_model import BookCopy
from app.models.book_model import Book
from app.models.book_category_model import BookCategory

from app.schemas.book_schema import (
    BookCreate,
    BookUpdate
)

from app.services.notification_service import NotificationService


class BookService:

    # =====================================
    # Generate Product ID
    # =====================================

    @staticmethod
    async def generate_product_id(
            db: AsyncSession
    ) -> str:

        result = await db.execute(
            select(Book.id).order_by(
                Book.id.desc()
            )
        )

        last_book_id = result.scalars().first()

        if last_book_id:
            next_id = last_book_id + 1
        else:
            next_id = 1

        return f"PROD-{next_id:05d}"

    # =====================================
    # Generate Book Code
    # =====================================

    @staticmethod
    async def generate_book_code(
            db: AsyncSession
    ) -> str:

        result = await db.execute(
            select(Book.id).order_by(
                Book.id.desc()
            )
        )

        last_book_id = result.scalars().first()

        if last_book_id:
            next_id = last_book_id + 1
        else:
            next_id = 1

        return f"BOOK-{next_id:05d}"

    # =====================================
    # Create Book
    # =====================================

    @staticmethod
    async def create_book(
            db: AsyncSession,
            payload: BookCreate,
            user_id: int | None = None
    ):

        try:

            # ---------------------------------
            # Validate Category
            # ---------------------------------

            category = await db.get(
                BookCategory,
                payload.category_id
            )

            if not category:
                raise ValueError(
                    "Book category not found"
                )

            if not category.is_active:
                raise ValueError(
                    "Book category is inactive"
                )

            # ---------------------------------
            # Validate Category Ownership
            # ---------------------------------

            if (
                    category.school_id != payload.school_id
                    or
                    category.branch_id != payload.branch_id
                    or
                    category.library_id != payload.library_id
            ):
                raise ValueError(
                    "Category does not belong "
                    "to selected library"
                )

            # ---------------------------------
            # Validate ISBN
            # ---------------------------------

            isbn = payload.isbn_number.strip()

            existing = await db.execute(
                select(Book).where(
                    Book.isbn_number == isbn
                )
            )

            if existing.scalars().first():
                raise ValueError(
                    "ISBN already exists"
                )

            # ---------------------------------
            # Generate IDs
            # ---------------------------------

            product_id = await BookService.generate_product_id(
                db
            )

            book_code = await BookService.generate_book_code(
                db
            )

            # ---------------------------------
            # Create Book
            # ---------------------------------

            book = Book(

                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id,

                category_id=payload.category_id,

                product_id=product_id,
                book_code=book_code,

                isbn_number=isbn,

                title=payload.title,
                sub_title=payload.sub_title,

                author_name=payload.author_name,
                publisher_name=payload.publisher_name,

                edition=payload.edition,
                language=payload.language,
                subject_name=payload.subject_name,

                book_type=payload.book_type,

                cover_image_url=payload.cover_image_url,

                # Copies created later
                quantity=0,
                available_copies=0,

                minimum_threshold=payload.minimum_threshold,

                lost_copies=0,
                damaged_copies=0,
                reserved_copies=0,

                low_stock_alert=False,

                keywords=payload.keywords,
                description=payload.description,

                is_active=True,

                creator_role=payload.creator_role,

                created_by=user_id
            )

            db.add(book)

            await db.commit()

            await db.refresh(book)

            # ---------------------------------
            # Notifications
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="New Book Added",
                message=(
                    f"{book.title} created successfully"
                ),
                notification_type="BOOK",
                recipient_role="ADMIN"
            )

            await NotificationService.create_notification(
                db=db,
                title="New Book Added",
                message=(
                    f"{book.title} created successfully"
                ),
                notification_type="BOOK",
                recipient_role="LIBRARIAN"
            )

            return book

        except Exception:

            await db.rollback()
            raise

    # =====================================
    # Get Book By ID
    # =====================================

    @staticmethod
    async def get_book_by_id(
            db: AsyncSession,
            book_id: int
    ):

        try:

            result = await db.execute(
                select(Book).where(
                    Book.id == book_id,
                    Book.is_active == True
                )
            )

            book = result.scalar_one_or_none()

            if not book:
                raise ValueError(
                    "Book not found"
                )

            return book

        except Exception:

            await db.rollback()
            raise

    # =====================================
    # Get All Books
    # =====================================

    @staticmethod
    async def get_all_books(
            db: AsyncSession
    ):

        result = await db.execute(
            select(Book)
            .where(Book.is_active == True)
            .order_by(Book.title.asc())
        )

        return result.scalars().all()

    # =====================================
    # Update Book
    # =====================================
    @staticmethod
    async def update_book(
            db: AsyncSession,
            book_id: int,
            payload: BookUpdate,
            user_id: int | None = None
    ):

        try:

            # ---------------------------------
            # Fetch Book
            # ---------------------------------

            book = await db.get(
                Book,
                book_id
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
            # Validate ISBN
            # ---------------------------------

            if (
                    payload.isbn_number
                    and
                    payload.isbn_number
                    != book.isbn_number
            ):

                isbn = payload.isbn_number.strip()

                existing = await db.execute(
                    select(Book).where(
                        Book.isbn_number == isbn,
                        Book.id != book_id
                    )
                )

                if existing.scalar_one_or_none():
                    raise ValueError(
                        "ISBN already exists"
                    )

                book.isbn_number = isbn


            # ---------------------------------
            # Update Fields
            # ---------------------------------

            update_data = payload.model_dump(
                exclude_unset=True
            )

            restricted_fields = {
                "quantity",
                "available_copies",
                "lost_copies",
                "damaged_copies",
                "reserved_copies",
                "product_id",
                "book_code"
            }

            for field, value in update_data.items():

                if field in restricted_fields:
                    continue

                setattr(
                    book,
                    field,
                    value
                )

            # ---------------------------------
            # Audit
            # ---------------------------------

            book.updated_by = user_id

            # ---------------------------------
            # Save
            # ---------------------------------

            await db.commit()

            await db.refresh(book)

            # ---------------------------------
            # Notification
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Book Updated",
                message=(
                    f"{book.title} updated successfully"
                ),
                notification_type="BOOK_UPDATED",
                recipient_role="ADMIN"
            )

            await NotificationService.create_notification(
                db=db,
                title="Book Updated",
                message=(
                    f"{book.title} updated successfully"
                ),
                notification_type="BOOK_UPDATED",
                recipient_role="LIBRARIAN"
            )

            return book

        except Exception:

            await db.rollback()
            raise

    # =====================================
    # Delete Book
    # =====================================

    @staticmethod
    async def delete_book(
            db: AsyncSession,
            book_id: int,
            user_id: int | None = None
    ):

        try:

            # ---------------------------------
            # Fetch Book
            # ---------------------------------

            book = await db.get(
                Book,
                book_id
            )

            if not book:
                raise ValueError(
                    "Book not found"
                )

            if not book.is_active:
                raise ValueError(
                    "Book already deleted"
                )

            # ---------------------------------
            # Check Active Copies
            # ---------------------------------

            copies_result = await db.execute(
                select(BookCopy).where(
                    BookCopy.book_id == book_id,
                    BookCopy.is_active == True
                )
            )

            copies = copies_result.scalars().all()

            if copies:
                raise ValueError(
                    "Cannot delete book. "
                    "Active book copies exist."
                )

            # ---------------------------------
            # Soft Delete
            # ---------------------------------

            book.is_active = False

            book.updated_by = user_id

            # ---------------------------------
            # Save
            # ---------------------------------

            await db.commit()

            await db.refresh(book)

            # ---------------------------------
            # Notifications
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Book Deleted",
                message=(
                    f"{book.title} deleted successfully"
                ),
                notification_type="BOOK_DELETED",
                recipient_role="ADMIN"
            )

            await NotificationService.create_notification(
                db=db,
                title="Book Deleted",
                message=(
                    f"{book.title} deleted successfully"
                ),
                notification_type="BOOK_DELETED",
                recipient_role="LIBRARIAN"
            )

            return {
                "success": True,
                "message": (
                    f"{book.title} deleted successfully"
                )
            }

        except Exception:

            await db.rollback()
            raise

    # =====================================
    # Search Books
    # =====================================

    # @staticmethod
    # async def search_books(
    #         db: AsyncSession,
    #         keyword: str
    # ):
    #
    #     try:
    #
    #         keyword = keyword.strip()
    #
    #         if not keyword:
    #             raise ValueError(
    #                 "Search keyword is required"
    #             )
    #
    #         result = await db.execute(
    #             select(Book).where(
    #
    #                 Book.is_active == True,
    #
    #                 (
    #                     Book.title.ilike(
    #                         f"%{keyword}%"
    #                     )
    #                 )
    #                 |
    #                 (
    #                     Book.author_name.ilike(
    #                         f"%{keyword}%"
    #                     )
    #                 )
    #                 |
    #                 (
    #                     Book.isbn_number.ilike(
    #                         f"%{keyword}%"
    #                     )
    #                 )
    #                 |
    #                 (
    #                     Book.book_code.ilike(
    #                         f"%{keyword}%"
    #                     )
    #                 )
    #                 |
    #                 (
    #                     Book.subject_name.ilike(
    #                         f"%{keyword}%"
    #                     )
    #                 )
    #                 |
    #                 (
    #                     Book.publisher_name.ilike(
    #                         f"%{keyword}%"
    #                     )
    #                 )
    #
    #             ).order_by(
    #                 Book.title.asc()
    #             )
    #         )
    #
    #         books = result.scalars().all()
    #
    #         return books
    #
    #     except Exception:
    #
    #         await db.rollback()
    #         raise

    # =====================================
    # Inventory Summary
    # =====================================

    @staticmethod
    async def get_inventory_summary(
            db: AsyncSession,
            book_id: int
    ):

        try:

            # ---------------------------------
            # Fetch Book
            # ---------------------------------

            book = await db.get(
                Book,
                book_id
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
            # Calculate Issued Copies
            # ---------------------------------

            issued_copies = (
                    book.quantity
                    -
                    book.available_copies
                    -
                    book.lost_copies
                    -
                    book.damaged_copies
                    -
                    book.reserved_copies
            )

            if issued_copies < 0:
                issued_copies = 0

            # ---------------------------------
            # Response
            # ---------------------------------

            return {

                "book_id": book.id,

                "book_code": book.book_code,

                "title": book.title,

                "isbn_number": book.isbn_number,

                "author_name": book.author_name,

                "total_copies": book.quantity,

                "available_copies": book.available_copies,

                "issued_copies": issued_copies,

                "lost_copies": book.lost_copies,

                "damaged_copies": book.damaged_copies,

                "reserved_copies": book.reserved_copies,

                "minimum_threshold":
                    book.minimum_threshold,

                "low_stock_alert":
                    book.low_stock_alert
            }

        except Exception:

            await db.rollback()
            raise

    # =====================================
    # Low Stock Books
    # =====================================

    @staticmethod
    async def get_low_stock_books(
            db: AsyncSession
    ):

        try:

            result = await db.execute(
                select(Book).where(
                    Book.is_active == True,
                    Book.available_copies
                    <=
                    Book.minimum_threshold
                ).order_by(
                    Book.available_copies.asc()
                )
            )

            books = result.scalars().all()

            response = []

            for book in books:
                response.append({

                    "book_id": book.id,

                    "book_code": book.book_code,

                    "title": book.title,

                    "isbn_number": book.isbn_number,

                    "author_name": book.author_name,

                    "total_copies": book.quantity,

                    "available_copies":
                        book.available_copies,

                    "minimum_threshold":
                        book.minimum_threshold,

                    "low_stock_alert": True
                })

            return response

        except Exception:

            await db.rollback()
            raise