from datetime import datetime
from typing import Text

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class BookStockRequest(Base):

    __tablename__ = "book_stock_requests"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    product_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False
    )

    requested_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    approved_quantity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    request_status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING"
    )

    requested_by: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    approved_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
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
    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
