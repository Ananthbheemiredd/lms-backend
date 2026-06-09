from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Text,
    Boolean,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class Book(Base):
    __tablename__ = "books"

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
    # Category Details
    # =====================================

    category_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    # =====================================
    # Book Identification
    # =====================================

    product_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    book_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    isbn_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    # =====================================
    # Book Information
    # =====================================

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    sub_title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    author_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    publisher_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    edition: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    subject_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    book_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    cover_image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    # =====================================
    # Inventory Details
    # =====================================

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    available_copies: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    minimum_threshold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5
    )

    lost_copies: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    damaged_copies: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    reserved_copies: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    low_stock_alert: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # =====================================
    # Search Support
    # =====================================

    keywords: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # =====================================
    # Status
    # =====================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
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
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
