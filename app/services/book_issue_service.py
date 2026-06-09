from datetime import (
    date,
    timedelta
)

from sqlalchemy import (
    select,
    and_
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_issue_model import (
    BookIssue
)
from app.services.email_service import (
EmailService
)
from app.models.book_copy_model import (
    BookCopy
)
from app.models.book_model import (
Book
)
# from app.models.book_master_model import (
#     Book
# )

from app.models.student_model import (
    Student
)

from app.models.profile_information_model import (
    ProfileInformation
)

from app.models.library_borrow_rule_model import (
    LibraryBorrowRule
)

from app.services.notification_service import (
    NotificationService
)


class BookIssueService:

    # =====================================
    # ISSUE BOOK
    # =====================================

    @staticmethod
    async def issue_book(
            db: AsyncSession,
            payload,
            issued_by: int
    ):

        try:

            # ---------------------------------
            # Validate Borrower
            # ---------------------------------

            borrower = None

            if payload.borrower_type == "STUDENT":

                if not payload.student_id:
                    raise ValueError(
                        "student_id is required"
                    )

                borrower = await db.get(
                    Student,
                    payload.student_id
                )

            elif payload.borrower_type == "EMPLOYEE":

                if not payload.employee_id:
                    raise ValueError(
                        "employee_id is required"
                    )

                borrower = await db.get(
                    ProfileInformation,
                    payload.employee_id
                )

            else:
                raise ValueError(
                    "Invalid borrower type"
                )

            if not borrower:
                raise ValueError(
                    "Borrower not found"
                )

            # ---------------------------------
            # Borrower Details
            # ---------------------------------

            if payload.borrower_type == "STUDENT":

                borrower_name = borrower.student_name
                borrower_email = borrower.email

            else:

                borrower_name = borrower.employee_name
                borrower_email = borrower.email

            # ---------------------------------
            # Borrower Active Check
            # ---------------------------------

            if not borrower.is_active:
                raise ValueError(
                    "Borrower is inactive"
                )

            # ---------------------------------
            # Library Block Check
            # ---------------------------------

            if borrower.is_library_blocked:
                raise ValueError(
                    "User is blocked from library"
                )

            # ---------------------------------
            # Pending Fine Check
            # ---------------------------------

            if borrower.pending_fine_amount > 0:
                raise ValueError(
                    "Pending fine exists. Please clear dues first."
                )

            # ---------------------------------
            # Borrow Rule Validation
            # ---------------------------------

            rule_result = await db.execute(
                select(LibraryBorrowRule).where(
                    and_(
                        LibraryBorrowRule.school_id
                        == payload.school_id,

                        LibraryBorrowRule.branch_id
                        == payload.branch_id,

                        LibraryBorrowRule.library_id
                        == payload.library_id,

                        LibraryBorrowRule.borrower_type
                        == payload.borrower_type,

                        LibraryBorrowRule.is_active
                        == True
                    )
                )
            )

            borrow_rule = (
                rule_result.scalar_one_or_none()
            )

            if not borrow_rule:
                raise ValueError(
                    "Borrow rule not configured"
                )

            # ---------------------------------
            # Borrow Limit Check
            # ---------------------------------

            if (
                    borrower.current_borrowed_books
                    >= borrow_rule.max_books_allowed
            ):
                raise ValueError(
                    "Borrow limit exceeded"
                )

            # ---------------------------------
            # Overdue Book Check
            # ---------------------------------

            overdue_query = await db.execute(
                select(BookIssue).where(
                    and_(
                        BookIssue.issue_status == "ISSUED",
                        BookIssue.due_date < date.today(),

                        (
                                BookIssue.student_id
                                == payload.student_id
                        )
                        if payload.borrower_type
                           == "STUDENT"
                        else
                        (
                                BookIssue.employee_id
                                == payload.employee_id
                        )
                    )
                )
            )

            overdue_book = (
                overdue_query.scalar_one_or_none()
            )

            if overdue_book:
                raise ValueError(
                    "Overdue book exists. Return overdue books first."
                )

            # # ---------------------------------
            # # Validate Book
            # # ---------------------------------
            #
            # book = await db.get(
            #     Book,
            #     payload.book_id
            # )
            #
            # if not book:
            #     raise ValueError(
            #         "Book not found"
            #     )
            #
            # if not book.is_active:
            #     raise ValueError(
            #         "Book is inactive"
            #     )
            # ---------------------------------
            # Validate Book Copy
            # ---------------------------------

            book_copy = await db.get(
                BookCopy,
                payload.book_copy_id
            )

            if not book_copy:
                raise ValueError(
                    "Book copy not found"
                )

            if not book_copy.is_active:
                raise ValueError(
                    "Book copy is inactive"
                )

            # ---------------------------------
            # Fetch Parent Book
            # ---------------------------------

            book = await db.get(
                Book,
                book_copy.book_id
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
            # Validate Book Ownership
            # ---------------------------------

            if (
                    book.school_id != payload.school_id
                    or
                    book.branch_id != payload.branch_id
                    or
                    book.library_id != payload.library_id
            ):
                raise ValueError(
                    "Book does not belong to this library"
                )
            #
            # # ---------------------------------
            # # Find Available Copy
            # # ---------------------------------
            #
            # copy_result = await db.execute(
            #     select(BookCopy).where(
            #         and_(
            #             BookCopy.book_id
            #             == payload.book_id,
            #
            #             BookCopy.book_status
            #             == "AVAILABLE",
            #
            #             BookCopy.is_active
            #             == True
            #         )
            #     )
            # )
            #
            # book_copy = (
            #     copy_result.scalar_one_or_none()
            # )

            if not book_copy:
                raise ValueError(
                    "No available copies found"
                )

            # ---------------------------------
            # Validate Copy Ownership
            # ---------------------------------

            if (
                    book_copy.school_id != payload.school_id
                    or
                    book_copy.branch_id != payload.branch_id
                    or
                    book_copy.library_id != payload.library_id
            ):
                raise ValueError(
                    "Book copy does not belong to this library"
                )

            # ---------------------------------
            # Validate Copy Location
            # ---------------------------------

            if book_copy.book_status == "UNALLOCATED":
                raise ValueError(
                    "Book copy location not assigned"
                )

            # ---------------------------------
            # Inventory Validation
            # ---------------------------------

            if book.available_copies <= 0:
                raise ValueError(
                    "No available copies remaining"
                )

            if book_copy.book_status != "AVAILABLE":
                raise ValueError(
                    "Book copy is already issued"
                )

            # ---------------------------------
            # Calculate Dates
            # ---------------------------------

            issue_date = date.today()

            due_date = (
                    issue_date
                    + timedelta(
                days=borrow_rule.max_issue_days
            )
            )

            # ---------------------------------
            # Create Issue Record
            # ---------------------------------

            issue = BookIssue(
                school_id=payload.school_id,
                branch_id=payload.branch_id,
                library_id=payload.library_id,

                borrower_type=payload.borrower_type,

                student_id=payload.student_id,
                employee_id=payload.employee_id,

                book_id=book.id,
                book_copy_id=book_copy.id,

                issue_date=issue_date,
                due_date=due_date,

                issue_status="ISSUED",

                remarks=payload.remarks,

                creator_role=payload.creator_role,

                issued_by=issued_by
            )

            db.add(issue)

            # ---------------------------------
            # Update Inventory
            # ---------------------------------

            book.available_copies -= 1

            book_copy.book_status = "ISSUED"

            # ---------------------------------
            # Update Borrower Summary
            # ---------------------------------

            borrower.current_borrowed_books += 1

            borrower.last_issue_date = issue_date

            current_books = (
                    borrower.allocated_book_codes
                    or ""
            )

            if current_books:

                borrower.allocated_book_codes = (
                        current_books
                        + ", "
                        + book_copy.barcode
                )

            else:

                borrower.allocated_book_codes = (
                    book_copy.barcode
                )

            # ---------------------------------
            # Save
            # ---------------------------------

            await db.commit()

            await db.refresh(issue)

            # ---------------------------------
            # Notifications
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Book Issued",
                message=f"{book.title} issued successfully",
                notification_type="BOOK_ISSUE",
                recipient_role="ADMIN"
            )

            await NotificationService.create_notification(
                db=db,
                title="Book Issued",
                message=f"{book.title} issued successfully",
                notification_type="BOOK_ISSUE",
                recipient_role="LIBRARIAN"
            )

            await NotificationService.create_notification(
                db=db,
                title="Book Issued",
                message=f"{book.title} issued successfully",
                notification_type="BOOK_ISSUE",
                recipient_role=payload.borrower_type
            )

            # ---------------------------------
            # Email
            # ---------------------------------

            await EmailService.send_email(
                to_email=borrower_email,
                subject="Book Issued Successfully",
                body=f"""
                <h3>Library Management System</h3>

                <p>Dear {borrower_name},</p>

                <p>Your book has been issued successfully.</p>

                <p>
                    <b>Book:</b> {book.title}<br>
                    <b>Issue Date:</b> {issue.issue_date}<br>
                    <b>Due Date:</b> {issue.due_date}
                </p>

                <p>Please return the book before the due date.</p>

                <br>

                <p>
                    Regards,<br>
                    Library Team
                </p>
                """
            )

            return issue

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def return_book(
            db: AsyncSession,
            issue_id: int,
            payload,
            returned_by: int
    ):

        try:

            # ---------------------------------
            # Fetch Issue
            # ---------------------------------

            issue = await db.get(
                BookIssue,
                issue_id
            )

            if not issue:
                raise ValueError(
                    "Issue record not found"
                )

            if issue.issue_status == "RETURNED":
                raise ValueError(
                    "Book already returned"
                )

            # ---------------------------------
            # Fetch Book
            # ---------------------------------

            book = await db.get(
                Book,
                issue.book_id
            )

            if not book:
                raise ValueError(
                    "Book not found"
                )

            # ---------------------------------
            # Fetch Book Copy
            # ---------------------------------

            book_copy = await db.get(
                BookCopy,
                issue.book_copy_id
            )

            if not book_copy:
                raise ValueError(
                    "Book copy not found"
                )

            if book_copy.book_status != "ISSUED":
                raise ValueError(
                    "Book copy is not currently issued"
                )

            # ---------------------------------
            # Fetch Borrower
            # ---------------------------------

            if issue.borrower_type == "STUDENT":

                borrower = await db.get(
                    Student,
                    issue.student_id
                )

                if not borrower:
                    raise ValueError(
                        "Student not found"
                    )

                borrower_name = (
                    borrower.student_name
                )

            else:

                borrower = await db.get(
                    ProfileInformation,
                    issue.employee_id
                )

                if not borrower:
                    raise ValueError(
                        "Employee not found"
                    )

                borrower_name = (
                    borrower.employee_name
                )

            # ---------------------------------
            # Return Details
            # ---------------------------------

            # return_date = date.today()

            return_date = payload.return_date
            issue.return_date = return_date
            issue.issue_status = "RETURNED"
            issue.returned_by = returned_by
            issue.return_remarks = (
                payload.remarks
            )

            # ---------------------------------
            # Fine Calculation
            # ---------------------------------

            fine = 0

            if return_date > issue.due_date:
                overdue_days = (
                        return_date -
                        issue.due_date
                ).days

                fine = overdue_days * 10

            issue.fine_amount = fine

            if fine > 0:
                issue.fine_paid = False

                borrower.pending_fine_amount += fine

            # ---------------------------------
            # Update Inventory
            # ---------------------------------

            book.available_copies += 1

            book.low_stock_alert = (
                    book.available_copies
                    <=
                    book.minimum_threshold
            )

            # ---------------------------------
            # Update Copy Status
            # ---------------------------------

            book_copy.book_status = (
                "AVAILABLE"
            )

            # ---------------------------------
            # Update Borrower Summary
            # ---------------------------------

            if borrower.current_borrowed_books > 0:
                borrower.current_borrowed_books -= 1

            borrower.last_return_date = (
                return_date
            )

            # ---------------------------------
            # Remove Barcode
            # ---------------------------------

            current_books = (
                    borrower.allocated_book_codes
                    or ""
            )

            updated_books = (
                current_books.replace(
                    book_copy.barcode,
                    ""
                )
            )

            borrower.allocated_book_codes = (
                updated_books.strip(", ")
            )

            # ---------------------------------
            # Save
            # ---------------------------------

            await db.commit()

            await db.refresh(issue)

            # ---------------------------------
            # Notifications
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Book Returned",
                message=(
                    f"{book.title} returned successfully"
                ),
                notification_type="BOOK_RETURN",
                recipient_role="ADMIN"
            )

            await NotificationService.create_notification(
                db=db,
                title="Book Returned",
                message=(
                    f"{book.title} returned successfully"
                ),
                notification_type="BOOK_RETURN",
                recipient_role="LIBRARIAN"
            )

            await NotificationService.create_notification(
                db=db,
                title="Book Returned",
                message=(
                    f"{book.title} returned successfully"
                ),
                notification_type="BOOK_RETURN",
                recipient_role=issue.borrower_type
            )

            # ---------------------------------
            # Email
            # ---------------------------------

            await EmailService.send_email(
                to_email=borrower.email,
                subject="Book Returned Successfully",
                body=f"""
                <h3>Library Management System</h3>

                <p>Dear {borrower_name},</p>

                <p>Your book has been returned successfully.</p>

                <p>
                    <b>Book:</b> {book.title}<br>
                    <b>Return Date:</b> {return_date}<br>
                    <b>Fine Amount:</b> ₹{fine}
                </p>

                <p>
                    Regards,<br>
                    Library Team
                </p>
                """
            )

            return issue

        except Exception:

            await db.rollback()
            raise

    @staticmethod
    async def delete_issue(
            db: AsyncSession,
            issue_id: int
    ):

        issue = await db.get(
            BookIssue,
            issue_id
        )

        if not issue:
            return False

        if issue.issue_status == "ISSUED":

            book = await db.get(
                Book,
                issue.book_id
            )

            book_copy = await db.get(
                BookCopy,
                issue.book_copy_id
            )

            borrower = None

            if issue.borrower_type == "STUDENT":

                borrower = await db.get(
                    Student,
                    issue.student_id
                )

            else:

                borrower = await db.get(
                    ProfileInformation,
                    issue.employee_id
                )

            book.available_copies += 1

            book_copy.book_status = (
                "AVAILABLE"
            )

            borrower.current_borrowed_books -= 1

            current_books = (
                    borrower.allocated_book_codes
                    or ""
            )

            updated_books = (
                current_books.replace(
                    book_copy.barcode,
                    ""
                )
            )

            borrower.allocated_book_codes = (
                updated_books.strip(", ")
            )

        await db.delete(issue)

        await db.commit()

        await NotificationService.create_notification(
            db=db,
            title="Issue Deleted",
            message=(
                "Book issue deleted successfully"
            ),
            notification_type="DELETE_ISSUE",
            recipient_role="ADMIN"
        )

        await NotificationService.create_notification(
            db=db,
            title="Issue Deleted",
            message=(
                "Book issue deleted successfully"
            ),
            notification_type="DELETE_ISSUE",
            recipient_role="LIBRARIAN"
        )

        return True


    # =====================================
    # GET ALL ISSUES
    # =====================================

    @staticmethod
    async def get_all_issues(
        db: AsyncSession
    ):

        result = await db.execute(
            select(BookIssue)
        )

        return result.scalars().all()
    # =====================================
    # GET ACTIVE ISSUES
    # =====================================

    @staticmethod
    async def get_active_issues(
        db: AsyncSession
    ):

        result = await db.execute(
            select(BookIssue).where(
                BookIssue.issue_status
                == "ISSUED"
            )
        )

        return result.scalars().all()
    # =====================================
    # GET ISSUE BY ID
    # =====================================

    @staticmethod
    async def get_issue_by_id(
        db: AsyncSession,
        issue_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                BookIssue.id == issue_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================
    # GET STUDENT ISSUES
    # =====================================

    @staticmethod
    async def get_student_issues(
        db: AsyncSession,
        student_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                BookIssue.student_id
                == student_id
            )
        )

        return result.scalars().all()

    # =====================================
    # GET EMPLOYEE ISSUES
    # =====================================

    @staticmethod
    async def get_employee_issues(
        db: AsyncSession,
        employee_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                BookIssue.employee_id
                == employee_id
            )
        )

        return result.scalars().all()

    # =====================================
    # GET OVERDUE BOOKS
    # =====================================

    @staticmethod
    async def get_overdue_books(
        db: AsyncSession
    ):

        result = await db.execute(
            select(BookIssue).where(
                and_(
                    BookIssue.issue_status
                    == "ISSUED",

                    BookIssue.due_date
                    < date.today()
                )
            )
        )

        return result.scalars().all()

    # =====================================
    # GET PENDING FINES
    # =====================================

    @staticmethod
    async def get_pending_fines(
        db: AsyncSession
    ):

        result = await db.execute(
            select(BookIssue).where(
                and_(
                    BookIssue.fine_amount > 0,

                    BookIssue.fine_paid
                    == False
                )
            )
        )

        return result.scalars().all()
    # =====================================
    # STUDENT OVERDUE BOOKS
    # =====================================

    @staticmethod
    async def get_student_overdue_books(
        db: AsyncSession,
        student_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                and_(
                    BookIssue.student_id
                    == student_id,

                    BookIssue.issue_status
                    == "ISSUED",

                    BookIssue.due_date
                    < date.today()
                )
            )
        )

        return result.scalars().all()

    # =====================================
    # STUDENT PENDING FINES
    # =====================================

    @staticmethod
    async def get_student_pending_fines(
        db: AsyncSession,
        student_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                and_(
                    BookIssue.student_id
                    == student_id,

                    BookIssue.fine_amount > 0,

                    BookIssue.fine_paid
                    == False
                )
            )
        )

        return result.scalars().all()

    # =====================================
    # STUDENT ACTIVE BOOKS
    # =====================================

    @staticmethod
    async def get_student_active_books(
        db: AsyncSession,
        student_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                and_(
                    BookIssue.student_id
                    == student_id,

                    BookIssue.issue_status
                    == "ISSUED"
                )
            )
        )

        return result.scalars().all()

    # =====================================
    # EMPLOYEE OVERDUE BOOKS
    # =====================================

    @staticmethod
    async def get_employee_overdue_books(
        db: AsyncSession,
        employee_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                and_(
                    BookIssue.employee_id
                    == employee_id,

                    BookIssue.issue_status
                    == "ISSUED",

                    BookIssue.due_date
                    < date.today()
                )
            )
        )

        return result.scalars().all()

    # =====================================
    # EMPLOYEE PENDING FINES
    # =====================================

    @staticmethod
    async def get_employee_pending_fines(
        db: AsyncSession,
        employee_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                and_(
                    BookIssue.employee_id
                    == employee_id,

                    BookIssue.fine_amount > 0,

                    BookIssue.fine_paid
                    == False
                )
            )
        )

        return result.scalars().all()

    # =====================================
    # EMPLOYEE ACTIVE BOOKS
    # =====================================

    @staticmethod
    async def get_employee_active_books(
        db: AsyncSession,
        employee_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                and_(
                    BookIssue.employee_id
                    == employee_id,

                    BookIssue.issue_status
                    == "ISSUED"
                )
            )
        )

        return result.scalars().all()

    # =====================================
    # PAY FINE
    # =====================================

    @staticmethod
    async def pay_fine(
            db: AsyncSession,
            issue_id: int
    ):

        try:

            # ---------------------------------
            # Fetch Issue
            # ---------------------------------

            issue = await db.get(
                BookIssue,
                issue_id
            )

            if not issue:
                raise ValueError(
                    "Issue not found"
                )

            # ---------------------------------
            # Fine Validation
            # ---------------------------------

            if issue.fine_amount <= 0:
                raise ValueError(
                    "No fine available"
                )

            if issue.fine_paid:
                raise ValueError(
                    "Fine already paid"
                )

            # ---------------------------------
            # Fetch Borrower
            # ---------------------------------

            borrower = None

            if issue.borrower_type == "STUDENT":

                borrower = await db.get(
                    Student,
                    issue.student_id
                )

                borrower_name = (
                    borrower.student_name
                )

            else:

                borrower = await db.get(
                    ProfileInformation,
                    issue.employee_id
                )

                borrower_name = (
                    borrower.employee_name
                )

            if not borrower:
                raise ValueError(
                    "Borrower not found"
                )

            # ---------------------------------
            # Update Issue
            # ---------------------------------

            issue.fine_paid = True

            issue.fine_paid_date = (
                date.today()
            )

            # If you add this field later
            # issue.fine_collected_by = paid_by

            # ---------------------------------
            # Update Borrower Fine
            # ---------------------------------

            borrower.pending_fine_amount -= (
                issue.fine_amount
            )

            if borrower.pending_fine_amount < 0:
                borrower.pending_fine_amount = 0

            # ---------------------------------
            # Unblock User
            # ---------------------------------

            if borrower.pending_fine_amount == 0:
                borrower.is_library_blocked = False

            # ---------------------------------
            # Save
            # ---------------------------------

            await db.commit()

            await db.refresh(issue)

            # ---------------------------------
            # Notifications
            # ---------------------------------

            await NotificationService.create_notification(
                db=db,
                title="Fine Paid",
                message=(
                    f"Fine paid successfully "
                    f"for issue #{issue.id}"
                ),
                notification_type="FINE_PAYMENT",
                recipient_role="ADMIN"
            )

            await NotificationService.create_notification(
                db=db,
                title="Fine Paid",
                message=(
                    f"Fine paid successfully "
                    f"for issue #{issue.id}"
                ),
                notification_type="FINE_PAYMENT",
                recipient_role="LIBRARIAN"
            )

            await NotificationService.create_notification(
                db=db,
                title="Fine Paid",
                message=(
                    f"Fine payment received "
                    f"for issue #{issue.id}"
                ),
                notification_type="FINE_PAYMENT",
                recipient_role=issue.borrower_type
            )

            # ---------------------------------
            # Email
            # ---------------------------------

            await EmailService.send_email(
                to_email=borrower.email,
                subject="Fine Payment Successful",
                body=f"""
                <h3>Library Management System</h3>

                <p>Dear {borrower_name},</p>

                <p>
                    Your library fine payment has been
                    received successfully.
                </p>

                <p>
                    <b>Issue ID:</b> {issue.id}<br>
                    <b>Fine Amount:</b> ₹{issue.fine_amount}<br>
                    <b>Paid Date:</b> {issue.fine_paid_date}
                </p>

                <p>
                    Thank you.
                </p>

                <br>

                <p>
                    Regards,<br>
                    Library Team
                </p>
                """
            )

            return issue

        except Exception:

            await db.rollback()
            raise
    # =====================================
    # STUDENT BORROW HISTORY
    # =====================================

    @staticmethod
    async def get_student_history(
        db: AsyncSession,
        student_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                BookIssue.student_id
                == student_id
            ).order_by(
                BookIssue.issue_date.desc()
            )
        )

        return result.scalars().all()

    # =====================================
    # EMPLOYEE BORROW HISTORY
    # =====================================

    @staticmethod
    async def get_employee_history(
        db: AsyncSession,
        employee_id: int
    ):

        result = await db.execute(
            select(BookIssue).where(
                BookIssue.employee_id
                == employee_id
            ).order_by(
                BookIssue.issue_date.desc()
            )
        )

        return result.scalars().all()