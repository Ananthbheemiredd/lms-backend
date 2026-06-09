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


class LibraryRow(Base):
    __tablename__ = "library_rows"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

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

    floor_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    rack_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    shelf_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    row_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    row_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        default=100
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    creator_role: Mapped[str] = mapped_column(
        String(50),
        nullable=False
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