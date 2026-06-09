# from itertools import product
#
# from sqlalchemy import (
#     select,
#     func
# )
#
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.models.book_master_model import (
#     BookMaster
# )
# from app.models.book_copy_model import (
#     BookCopy
# )
# from app.models.book_category_model import (
#     BookCategory
# )
#
# from app.services.notification_service import (
#     NotificationService
# )
#
#
# class BookMasterService:
#
#     # =====================================
#     # CREATE BOOK
#     # =====================================
#
#     @staticmethod
#     async def create_book(
#         db: AsyncSession,
#         payload,
#         created_by: int
#     ):
#
#         # -----------------------------
#         # Validate Category
#         # -----------------------------
#
#         category = await db.get(
#             BookCategory,
#             payload.category_id
#         )
#
#         if not category:
#
#             raise ValueError(
#                 "Selected category does not exist"
#             )
#
#         if category.school_id != payload.school_id:
#
#             raise ValueError(
#                 "Category does not belong to selected school"
#             )
#
#         if category.branch_id != payload.branch_id:
#
#             raise ValueError(
#                 "Category does not belong to selected branch"
#             )
#
#         if category.library_id != payload.library_id:
#
#             raise ValueError(
#                 "Category does not belong to selected library"
#             )
#
#         # -----------------------------
#         # Duplicate ISBN Validation
#         # -----------------------------
#
#         if payload.isbn_number:
#
#             existing_isbn = await db.execute(
#                 select(BookMaster).where(
#                     BookMaster.library_id == payload.library_id,
#                     BookMaster.isbn_number == payload.isbn_number
#                 )
#             )
#
#             if existing_isbn.scalar_one_or_none():
#
#                 raise ValueError(
#                     "ISBN already exists in this library"
#                 )
#
#         # -----------------------------
#         # Generate Book Code
#         # -----------------------------
#
#         result = await db.execute(
#             select(
#                 func.max(BookMaster.id)
#             )
#         )
#
#         last_id = result.scalar()
#
#         if last_id is None:
#             next_id = 1
#         else:
#             next_id = last_id + 1
#
#         book_code = (
#             f"BOOK-{next_id:05d}"
#         )
#
#         # -----------------------------
#         # Low Stock Validation
#         # -----------------------------
#
#         low_stock_alert = False
#
#         if (
#             payload.available_copies
#             <=
#             payload.minimum_threshold
#         ):
#
#             low_stock_alert = True
#
#         # -----------------------------
#         # Create Book
#         # -----------------------------
#
#         book = BookMaster(
#             school_id=payload.school_id,
#             branch_id=payload.branch_id,
#             library_id=payload.library_id,
#             category_id=payload.category_id,
#             product_id=payload.product_id,
#
#             book_code=book_code,
#
#             title=payload.title,
#             sub_title=payload.sub_title,
#
#             author_name=payload.author_name,
#             publisher_name=payload.publisher_name,
#
#             isbn_number=payload.isbn_number,
#
#             edition=payload.edition,
#             language=payload.language,
#
#             subject_name=payload.subject_name,
#             book_type=payload.book_type,
#
#             total_copies=payload.total_copies,
#             available_copies=payload.available_copies,
#
#             minimum_threshold=payload.minimum_threshold,
#             low_stock_alert=low_stock_alert,
#
#             lost_copies=payload.lost_copies,
#             damaged_copies=payload.damaged_copies,
#             reserved_copies=payload.reserved_copies,
#
#             keywords=payload.keywords,
#
#             description=payload.description,
#
#             creator_role=payload.creator_role,
#
#             created_by=created_by
#         )
#
#         db.add(book)
#
#         # Generate Book ID
#         await db.flush()
#
#         # =====================================
#         # AUTO CREATE BOOK COPIES
#         # =====================================
#
#         for copy_no in range(1, payload.total_copies + 1):
#             barcode = (
#                 f"BC-{book.id:05d}-{copy_no:03d}"
#             )
#
#             accession_number = (
#                 f"ACC-{book.id:05d}-{copy_no:03d}"
#             )
#
#             copy = BookCopy(
#                 school_id=book.school_id,
#                 branch_id=book.branch_id,
#                 library_id=book.library_id,
#
#                 book_id=book.id,
#
#                 barcode=barcode,
#                 accession_number=accession_number,
#
#                 copy_number=copy_no,
#
#                 book_status="UNALLOCATED",
#
#                 creator_role=payload.creator_role,
#
#                 created_by=created_by,
#
#                 # Location assigned later
#                 floor_id=None,
#                 rack_id=None,
#                 shelf_id=None,
#                 row_id=None
#             )
#
#             db.add(copy)
#
#         # Enterprise inventory sync
#         book.total_copies = payload.total_copies
#         book.available_copies = payload.total_copies
#
#         await db.commit()
#
#         await db.refresh(book)
#
#
#
#         # -----------------------------
#         # Book Created Notification
#         # -----------------------------
#
#         await NotificationService.create_notification(
#             db=db,
#             title="Book Created",
#             message=f"{book.title} created successfully",
#             notification_type="BOOK_CREATED",
#             recipient_role=payload.creator_role
#         )
#
#         # -----------------------------
#         # Low Stock Notification
#         # -----------------------------
#
#         if low_stock_alert:
#             await NotificationService.create_notification(
#                 db=db,
#                 title="Low Stock Alert",
#                 message=(
#                     f"{book.title} stock reached threshold level"
#                 ),
#                 notification_type="LOW_STOCK_ALERT",
#                 recipient_role=book.creator_role
#             )
#         return book
#
#     # =====================================
#     # GET ALL BOOKS
#     # =====================================
#
#     @staticmethod
#     async def get_all_books(
#         db: AsyncSession
#     ):
#
#         result = await db.execute(
#             select(BookMaster)
#         )
#
#         return result.scalars().all()
#
#     # =====================================
#     # GET BOOK BY ID
#     # =====================================
#
#     @staticmethod
#     async def get_book_by_id(
#         db: AsyncSession,
#         book_id: int
#     ):
#
#         result = await db.execute(
#             select(BookMaster).where(
#                 BookMaster.id == book_id
#             )
#         )
#
#         return result.scalar_one_or_none()
#
#     # =====================================
#     # UPDATE BOOK
#     # =====================================
#
#     @staticmethod
#     async def update_book(
#         db: AsyncSession,
#         book_id: int,
#         payload,
#         updated_by: int
#     ):
#
#         book = await (
#             BookMasterService
#             .get_book_by_id(
#                 db,
#                 book_id
#             )
#         )
#
#         if not book:
#             return None
#
#         # -----------------------------
#         # Update Fields
#         # -----------------------------
#
#         if payload.title is not None:
#             book.title = payload.title
#
#         if payload.sub_title is not None:
#             book.sub_title = payload.sub_title
#
#         if payload.author_name is not None:
#             book.author_name = payload.author_name
#
#         if payload.publisher_name is not None:
#             book.publisher_name = payload.publisher_name
#
#         if payload.isbn_number is not None:
#             book.isbn_number = payload.isbn_number
#
#         if payload.edition is not None:
#             book.edition = payload.edition
#
#         if payload.language is not None:
#             book.language = payload.language
#
#         if payload.subject_name is not None:
#             book.subject_name = payload.subject_name
#
#         if payload.book_type is not None:
#             book.book_type = payload.book_type
#
#         if payload.total_copies is not None:
#             book.total_copies = payload.total_copies
#
#         if payload.available_copies is not None:
#             book.available_copies = payload.available_copies
#
#         if payload.minimum_threshold is not None:
#             book.minimum_threshold = payload.minimum_threshold
#
#         if payload.lost_copies is not None:
#             book.lost_copies = payload.lost_copies
#
#         if payload.damaged_copies is not None:
#             book.damaged_copies = payload.damaged_copies
#
#         if payload.reserved_copies is not None:
#             book.reserved_copies = payload.reserved_copies
#
#         if payload.keywords is not None:
#             book.keywords = payload.keywords
#
#         if payload.description is not None:
#             book.description = payload.description
#
#         if payload.is_active is not None:
#             book.is_active = payload.is_active
#
#         # -----------------------------
#         # Low Stock Check
#         # -----------------------------
#
#         if (
#             book.available_copies
#             <=
#             book.minimum_threshold
#         ):
#
#             book.low_stock_alert = True
#
#             await NotificationService.create_notification(
#                 db=db,
#                 title="Low Stock Alert",
#                 message=(
#                     f"{book.title} stock reached threshold level"
#                 ),
#                 notification_type="LOW_STOCK_ALERT",
#                 recipient_role=book.creator_role
#             )
#
#         else:
#
#             book.low_stock_alert = False
#
#         book.updated_by = updated_by
#
#         await db.commit()
#
#         await db.refresh(book)
#
#         # -----------------------------
#         # Update Notification
#         # -----------------------------
#
#         await NotificationService.create_notification(
#             db=db,
#             title="Book Updated",
#             message=f"{book.title} updated successfully",
#             notification_type="BOOK_UPDATED",
#             recipient_role=book.creator_role
#         )
#
#         return book
#
#     # =====================================
#     # DELETE BOOK
#     # =====================================
#
#     @staticmethod
#     async def delete_book(
#         db: AsyncSession,
#         book_id: int
#     ):
#
#         book = await (
#             BookMasterService
#             .get_book_by_id(
#                 db,
#                 book_id
#             )
#         )
#
#         if not book:
#             return False
#
#         book_title = book.title
#         role = book.creator_role
#
#         await db.delete(book)
#
#         await db.commit()
#
#         await NotificationService.create_notification(
#             db=db,
#             title="Book Deleted",
#             message=f"{book_title} deleted successfully",
#             notification_type="BOOK_DELETED",
#             recipient_role=role
#         )
#
#         return True