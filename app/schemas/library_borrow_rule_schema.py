from datetime import datetime

from typing import (
    Optional,
    Literal
)

from pydantic import (
    BaseModel,
    Field
)


# =====================================
# CREATE BORROW RULE
# =====================================

class LibraryBorrowRuleCreate(BaseModel):

    school_id: int
    branch_id: int
    library_id: int

    borrower_type: Literal[
        "STUDENT",
        "EMPLOYEE"
    ]

    max_books_allowed: int = Field(
        default=1,
        ge=1
    )

    max_issue_days: int = Field(
        default=7,
        ge=1
    )

    fine_per_day: float = Field(
        default=0,
        ge=0
    )

    grace_days: int = Field(
        default=0,
        ge=0
    )

    creator_role: Literal[
        "ADMIN",
        "LIBRARIAN"
    ]


# =====================================
# UPDATE BORROW RULE
# =====================================

class LibraryBorrowRuleUpdate(BaseModel):

    max_books_allowed: Optional[int] = Field(
        default=None,
        ge=1
    )

    max_issue_days: Optional[int] = Field(
        default=None,
        ge=1
    )

    fine_per_day: Optional[float] = Field(
        default=None,
        ge=0
    )

    grace_days: Optional[int] = Field(
        default=None,
        ge=0
    )

    is_active: Optional[bool] = None


# =====================================
# RESPONSE
# =====================================

class LibraryBorrowRuleResponse(BaseModel):

    id: int

    school_id: int
    branch_id: int
    library_id: int

    borrower_type: str

    max_books_allowed: int

    max_issue_days: int

    fine_per_day: float

    grace_days: int

    creator_role: str

    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True