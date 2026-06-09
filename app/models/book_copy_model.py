from datetime import (
    datetime,
    date
)

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Float,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base

class BookCopy(Base):
    __tablename__ = "book_copies"

    # =====================================
    # Primary Key
    # =====================================

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
    # Book Details
    # =====================================

    book_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    # =====================================
    # Copy Identification
    # =====================================

    barcode: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    accession_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    copy_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # =====================================
    # Physical Location
    # =====================================

    floor_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True
    )

    rack_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True
    )

    shelf_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True
    )

    row_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True
    )

    # =====================================
    # Status
    # =====================================

    book_status: Mapped[str] = mapped_column(
        String(50),
        default="UNALLOCATED"
    )

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

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    created_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    updated_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    acquisition_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    acquisition_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    acquisition_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    source_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    is_reference_only: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    # created_role: Mapped[str | None] = mapped_column(
    #     String(50),
    #     nullable=True
    # )
    barcode_image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    qr_code_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )