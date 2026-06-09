from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    Float
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class LibraryBorrowRule(Base):
    __tablename__ = "library_borrow_rules"

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
    # Borrower Type
    # =====================================

    borrower_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    # =====================================
    # Borrow Rules
    # =====================================

    max_books_allowed: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    max_issue_days: Mapped[int] = mapped_column(
        Integer,
        default=7
    )

    fine_per_day: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    grace_days: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # =====================================
    # Status
    # =====================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # =====================================
    # Audit Fields
    # =====================================

    creator_role: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    updated_by: Mapped[int | None] = mapped_column(
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