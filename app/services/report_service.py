from datetime import date

from sqlalchemy import (
    select,
    and_,func
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.book_issue_model import (
    BookIssue
)
from app.models.book_model import Book


class ReportService:

    # =====================================
    # ISSUE REPORT
    # =====================================

    @staticmethod
    async def get_issue_report(
        db: AsyncSession,
        from_date: date | None = None,
        to_date: date | None = None,
        student_id: int | None = None,
        employee_id: int | None = None,
        book_id: int | None = None,
        issue_status: str | None = None,
        borrower_type: str | None = None
    ):

        filters = []

        # ---------------------------------
        # DATE FILTERS
        # ---------------------------------

        if from_date:

            filters.append(
                BookIssue.issue_date
                >= from_date
            )

        if to_date:

            filters.append(
                BookIssue.issue_date
                <= to_date
            )

        # ---------------------------------
        # STUDENT FILTER
        # ---------------------------------

        if student_id:

            filters.append(
                BookIssue.student_id
                == student_id
            )

        # ---------------------------------
        # EMPLOYEE FILTER
        # ---------------------------------

        if employee_id:

            filters.append(
                BookIssue.employee_id
                == employee_id
            )

        # ---------------------------------
        # BOOK FILTER
        # ---------------------------------

        if book_id:

            filters.append(
                BookIssue.book_id
                == book_id
            )

        # ---------------------------------
        # ISSUE STATUS FILTER
        # ---------------------------------

        if issue_status:

            filters.append(
                BookIssue.issue_status
                == issue_status
            )

        # ---------------------------------
        # BORROWER TYPE FILTER
        # ---------------------------------

        if borrower_type:

            filters.append(
                BookIssue.borrower_type
                == borrower_type
            )

        # ---------------------------------
        # QUERY
        # ---------------------------------

        result = await db.execute(

            select(BookIssue)

            .where(
                and_(*filters)
            )

            .order_by(
                BookIssue.issue_date.desc()
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_inventory_report(
            db: AsyncSession
    ):

        result = await db.execute(

            select(Book)

            .where(
                Book.is_active == True
            )

            .order_by(
                Book.title
            )
        )

        books = result.scalars().all()

        return [

            {
                "book_id": book.id,

                "title": book.title,

                "author_name": book.author_name,

                "quantity": book.quantity,

                "available_copies": book.available_copies,

                "lost_copies": book.lost_copies,

                "damaged_copies": book.damaged_copies,

                "reserved_copies": book.reserved_copies,

                "low_stock_alert": book.low_stock_alert
            }

            for book in books
        ]
    @staticmethod
    async def get_overdue_report(
            db: AsyncSession
    ):

        today = date.today()

        result = await db.execute(

            select(BookIssue)

            .where(

                and_(

                    BookIssue.issue_status == "ISSUED",

                    BookIssue.due_date < today
                )
            )

            .order_by(
                BookIssue.due_date
            )
        )

        issues = result.scalars().all()

        return [

            {
                "issue_id": issue.id,

                "book_id": issue.book_id,

                "borrower_type": issue.borrower_type,

                "student_id": issue.student_id,

                "employee_id": issue.employee_id,

                "issue_date": issue.issue_date,

                "due_date": issue.due_date,

                "days_overdue":
                    (
                            today -
                            issue.due_date
                    ).days
            }

            for issue in issues
        ]

    @staticmethod
    async def get_return_report(
            db: AsyncSession
    ):

        result = await db.execute(

            select(BookIssue)

            .where(
                BookIssue.issue_status
                == "RETURNED"
            )

            .order_by(
                BookIssue.return_date.desc()
            )
        )

        issues = result.scalars().all()

        return [

            {
                "issue_id": issue.id,

                "book_id": issue.book_id,

                "borrower_type":
                    issue.borrower_type,

                "student_id":
                    issue.student_id,

                "employee_id":
                    issue.employee_id,

                "issue_date":
                    issue.issue_date,

                "due_date":
                    issue.due_date,

                "return_date":
                    issue.return_date,

                "fine_amount":
                    issue.fine_amount
            }

            for issue in issues
        ]

    @staticmethod
    async def get_fine_report(
            db: AsyncSession
    ):

        result = await db.execute(

            select(BookIssue)

            .where(
                BookIssue.fine_amount > 0
            )

            .order_by(
                BookIssue.fine_amount.desc()
            )
        )

        issues = result.scalars().all()

        return [

            {
                "issue_id": issue.id,

                "book_id": issue.book_id,

                "borrower_type":
                    issue.borrower_type,

                "student_id":
                    issue.student_id,

                "employee_id":
                    issue.employee_id,

                "fine_amount":
                    issue.fine_amount,

                "fine_paid":
                    issue.fine_paid,

                "fine_paid_date":
                    issue.fine_paid_date
            }

            for issue in issues
        ]

    @staticmethod
    async def get_dashboard_report(
            db: AsyncSession
    ):

        total_books = await db.scalar(
            select(
                func.count(Book.id)
            )
        )

        total_available_books = await db.scalar(
            select(
                func.sum(
                    Book.available_copies
                )
            )
        )

        total_issued_books = await db.scalar(
            select(
                func.count(BookIssue.id)
            ).where(
                BookIssue.issue_status
                == "ISSUED"
            )
        )

        total_returned_books = await db.scalar(
            select(
                func.count(BookIssue.id)
            ).where(
                BookIssue.issue_status
                == "RETURNED"
            )
        )

        total_overdue_books = await db.scalar(
            select(
                func.count(BookIssue.id)
            ).where(
                and_(
                    BookIssue.issue_status
                    == "ISSUED",

                    BookIssue.due_date
                    < date.today()
                )
            )
        )

        total_pending_fines = await db.scalar(
            select(
                func.sum(
                    BookIssue.fine_amount
                )
            ).where(
                BookIssue.fine_paid.is_(False)
            )
        )

        return {

            "total_books":
                total_books or 0,

            "total_available_books":
                total_available_books or 0,

            "total_issued_books":
                total_issued_books or 0,

            "total_returned_books":
                total_returned_books or 0,

            "total_overdue_books":
                total_overdue_books or 0,

            "total_pending_fines":
                total_pending_fines or 0
        }
