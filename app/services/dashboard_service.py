from datetime import date

from sqlalchemy import (
    select,
    func,
    and_
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_master_model import (
    BookMaster
)

from app.models.book_issue_model import (
    BookIssue
)

from app.models.student_model import (
    Student
)

from app.models.profile_information_model import (
    ProfileInformation
)


class DashboardService:

    # =====================================
    # DASHBOARD SUMMARY
    # =====================================

    @staticmethod
    async def get_dashboard_summary(
        db: AsyncSession
    ):

        # ---------------------------------
        # Total Books
        # ---------------------------------

        total_books_query = await db.execute(
            select(
                func.count(BookMaster.id)
            )
        )

        total_books = (
            total_books_query.scalar()
        )

        # ---------------------------------
        # Issued Books
        # ---------------------------------

        issued_books_query = await db.execute(
            select(
                func.count(BookIssue.id)
            ).where(
                BookIssue.issue_status
                == "ISSUED"
            )
        )

        issued_books = (
            issued_books_query.scalar()
        )

        # ---------------------------------
        # Overdue Books
        # ---------------------------------

        overdue_books_query = await db.execute(
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

        overdue_books = (
            overdue_books_query.scalar()
        )

        # ---------------------------------
        # Pending Fine Amount
        # ---------------------------------

        fine_query = await db.execute(
            select(
                func.sum(
                    BookIssue.fine_amount
                )
            ).where(
                BookIssue.fine_paid
                == False
            )
        )

        pending_fines = (
            fine_query.scalar() or 0
        )

        # ---------------------------------
        # Active Students
        # ---------------------------------

        student_query = await db.execute(
            select(
                func.count(Student.id)
            ).where(
                Student.is_active == True
            )
        )

        total_students = (
            student_query.scalar()
        )

        # ---------------------------------
        # Active Employees
        # ---------------------------------

        employee_query = await db.execute(
            select(
                func.count(
                    ProfileInformation.id
                )
            ).where(
                ProfileInformation.is_active
                == True
            )
        )

        total_employees = (
            employee_query.scalar()
        )

        # ---------------------------------
        # Low Stock Books
        # ---------------------------------

        low_stock_query = await db.execute(
            select(
                func.count(BookMaster.id)
            ).where(
                BookMaster.available_copies
                <=
                BookMaster.minimum_threshold
            )
        )

        low_stock_books = (
            low_stock_query.scalar()
        )

        return {

            "total_books":
                total_books,

            "issued_books":
                issued_books,

            "overdue_books":
                overdue_books,

            "pending_fines":
                pending_fines,

            "total_students":
                total_students,

            "total_employees":
                total_employees,

            "low_stock_books":
                low_stock_books
        }
    # =====================================
    # LOW STOCK BOOKS
    # =====================================

    @staticmethod
    async def get_low_stock_books(
        db: AsyncSession
    ):

        result = await db.execute(
            select(BookMaster).where(
                BookMaster.available_copies
                <=
                BookMaster.minimum_threshold
            )
        )

        return result.scalars().all()

    # =====================================
    # OVERDUE BOOKS
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
    # PENDING FINES
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
    # TOP BORROWED BOOKS
    # =====================================

    @staticmethod
    async def get_top_books(
        db: AsyncSession
    ):

        result = await db.execute(
            select(
                BookMaster.title,
                func.count(
                    BookIssue.id
                ).label("issue_count")
            )
            .join(
                BookIssue,
                BookIssue.book_id
                == BookMaster.id
            )
            .group_by(BookMaster.title)
            .order_by(
                func.count(
                    BookIssue.id
                ).desc()
            )
            .limit(10)
        )

        books = result.all()

        return [
            {
                "title": row[0],
                "issue_count": row[1]
            }
            for row in books
        ]

    # =====================================
    # ACTIVE BORROWERS
    # =====================================

    @staticmethod
    async def get_active_borrowers(
        db: AsyncSession
    ):

        student_result = await db.execute(
            select(Student).where(
                Student.current_borrowed_books
                > 0
            )
        )

        employee_result = await db.execute(
            select(ProfileInformation).where(
                ProfileInformation.current_borrowed_books
                > 0
            )
        )

        students = student_result.scalars().all()

        employees = (
            employee_result.scalars().all()
        )

        data = []

        for student in students:

            data.append({
                "borrower_type": "STUDENT",
                "name": student.student_name,
                "borrowed_books":
                    student.current_borrowed_books
            })

        for employee in employees:

            data.append({
                "borrower_type": "EMPLOYEE",
                "name": employee.employee_name,
                "borrowed_books":
                    employee.current_borrowed_books
            })

        return data

    # =====================================
    # RECENT ISSUES
    # =====================================

    @staticmethod
    async def get_recent_issues(
        db: AsyncSession
    ):

        result = await db.execute(
            select(BookIssue)
            .order_by(
                BookIssue.created_at.desc()
            )
            .limit(10)
        )

        return result.scalars().all()

    # =====================================
    # RECENT RETURNS
    # =====================================

    @staticmethod
    async def get_recent_returns(
        db: AsyncSession
    ):

        result = await db.execute(
            select(BookIssue).where(
                BookIssue.issue_status
                == "RETURNED"
            )
            .order_by(
                BookIssue.return_date.desc()
            )
            .limit(10)
        )

        return result.scalars().all()

    # =====================================
    # FINE COLLECTION
    # =====================================

    @staticmethod
    async def get_fine_collection(
        db: AsyncSession
    ):

        result = await db.execute(
            select(
                func.sum(
                    BookIssue.fine_amount
                )
            ).where(
                BookIssue.fine_paid
                == True
            )
        )

        total = result.scalar() or 0

        return {
            "total_fine_collection":
                total
        }

    # =====================================
    # LIBRARY UTILIZATION
    # =====================================

    @staticmethod
    async def get_library_utilization(
        db: AsyncSession
    ):

        total_books_result = await db.execute(
            select(
                func.sum(
                    BookMaster.total_copies
                )
            )
        )

        available_books_result = (
            await db.execute(
                select(
                    func.sum(
                        BookMaster.available_copies
                    )
                )
            )
        )

        total_books = (
            total_books_result.scalar()
            or 0
        )

        available_books = (
            available_books_result.scalar()
            or 0
        )

        issued_books = (
            total_books
            -
            available_books
        )

        utilization_percentage = 0

        if total_books > 0:

            utilization_percentage = (
                issued_books
                /
                total_books
            ) * 100

        return {

            "total_books":
                total_books,

            "available_books":
                available_books,

            "issued_books":
                issued_books,

            "utilization_percentage":
                round(
                    utilization_percentage,
                    2
                )
        }

    # =====================================
    # BLOCKED USERS
    # =====================================

    @staticmethod
    async def get_blocked_users(
        db: AsyncSession
    ):

        student_result = await db.execute(
            select(Student).where(
                Student.is_library_blocked
                == True
            )
        )

        employee_result = await db.execute(
            select(ProfileInformation).where(
                ProfileInformation.is_library_blocked
                == True
            )
        )

        students = student_result.scalars().all()

        employees = (
            employee_result.scalars().all()
        )

        data = []

        for student in students:

            data.append({
                "type": "STUDENT",
                "name": student.student_name,
                "pending_fine":
                    student.pending_fine_amount
            })

        for employee in employees:

            data.append({
                "type": "EMPLOYEE",
                "name": employee.employee_name,
                "pending_fine":
                    employee.pending_fine_amount
            })

        return data