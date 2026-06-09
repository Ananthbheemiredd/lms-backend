from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    school_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    branch_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    branch_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
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