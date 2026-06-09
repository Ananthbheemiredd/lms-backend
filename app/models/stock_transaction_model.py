from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class StockTransaction(Base):

    __tablename__ = "stock_transactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    product_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False,
        index=True
    )

    transaction_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    reference_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    created_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )