from datetime import (
    datetime,
    date
)

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    Date
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class ProfileInformation(Base):
    __tablename__ = "profile_information"

    # =====================================
    # Primary Key
    # =====================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
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

    # =====================================
    # Employee Details
    # =====================================

    employee_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    employee_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    mobile_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    department_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    designation: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    # =====================================
    # Library Information
    # =====================================

    current_borrowed_books: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    pending_fine_amount: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    last_issue_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    last_return_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    is_library_blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False
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

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    allocated_book_codes: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )