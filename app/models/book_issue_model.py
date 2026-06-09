
from sqlalchemy import (
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Float,
    Text
)
from datetime import (
    datetime,
    date
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class BookIssue(Base):
    __tablename__ = "book_issues"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    # =====================================
    # Organization Details
    # =====================================

    school_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    branch_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    library_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    # =====================================
    # Borrower Details
    # =====================================

    borrower_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    student_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True
    )

    employee_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True
    )

    # =====================================
    # Book Details
    # =====================================

    book_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    book_copy_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    # =====================================
    # Issue Details
    # =====================================

    # issue_date: Mapped[datetime] = mapped_column(
    #     Date,
    #     nullable=False
    # )


    issue_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    return_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    # =====================================
    # Status
    # =====================================

    issue_status: Mapped[str] = mapped_column(
        String(50),
        default="ISSUED"
    )

    # =====================================
    # Fine Details
    # =====================================

    fine_amount: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    fine_paid: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    fine_paid_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    # =====================================
    # Remarks
    # =====================================

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # =====================================
    # Audit Fields
    # =====================================

    creator_role: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    issued_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    returned_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    return_remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
    renew_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    fine_collected_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )