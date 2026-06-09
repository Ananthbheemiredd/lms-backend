from datetime import datetime, date

from sqlalchemy import (
    Integer,
    String,
    Float,
    Date,
    DateTime,
    Text,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class BookStock(Base):

    __tablename__ = "book_stocks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    # Organization

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

    # Product Details

    product_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False
    )

    # Purchase Details

    supplier_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    invoice_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    purchase_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    purchase_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    # Stock Details

    received_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    available_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    damaged_quantity: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    lost_quantity: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
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