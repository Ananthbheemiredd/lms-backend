from datetime import datetime
from typing import Optional, Literal

from pydantic import (
    BaseModel,
    Field
)


# =====================================
# CREATE BOOK
# =====================================

class BookCreate(BaseModel):

    school_id: int

    branch_id: int

    library_id: int

    category_id: int

    title: str = Field(
        min_length=2,
        max_length=255
    )

    sub_title: Optional[str] = None

    author_name: str = Field(
        min_length=2,
        max_length=255
    )

    publisher_name: Optional[str] = None

    isbn_number: str = Field(
        min_length=3,
        max_length=100
    )

    edition: Optional[str] = None

    language: Optional[str] = None

    subject_name: Optional[str] = None

    book_type: Optional[str] = None

    cover_image_url: Optional[str] = None

    quantity: int = Field(
        ge=1
    )

    minimum_threshold: int = Field(
        default=5,
        ge=0
    )

    keywords: Optional[str] = None

    description: Optional[str] = None

    creator_role: Literal[
        "ADMIN",
        "LIBRARIAN"
    ]


# =====================================
# UPDATE BOOK
# =====================================

class BookUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255
    )

    sub_title: Optional[str] = None

    author_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255
    )

    publisher_name: Optional[str] = None

    edition: Optional[str] = None

    language: Optional[str] = None

    subject_name: Optional[str] = None

    book_type: Optional[str] = None

    cover_image_url: Optional[str] = None

    minimum_threshold: Optional[int] = Field(
        default=None,
        ge=0
    )

    keywords: Optional[str] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None


# =====================================
# BOOK RESPONSE
# =====================================

class BookResponse(BaseModel):

    id: int

    school_id: int

    branch_id: int

    library_id: int

    category_id: int

    product_id: str

    book_code: str

    isbn_number: str

    title: str

    sub_title: Optional[str]

    author_name: str

    publisher_name: Optional[str]

    edition: Optional[str]

    language: Optional[str]

    subject_name: Optional[str]

    book_type: Optional[str]

    cover_image_url: Optional[str]

    quantity: int

    available_copies: int

    minimum_threshold: int

    lost_copies: int

    damaged_copies: int

    reserved_copies: int

    keywords: Optional[str]

    description: Optional[str]

    creator_role: str

    is_active: bool

    created_by: Optional[int]

    updated_by: Optional[int]

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True


# =====================================
# INVENTORY SUMMARY RESPONSE
# =====================================

class BookInventorySummary(BaseModel):

    book_id: int

    title: str

    quantity: int

    available_copies: int

    issued_copies: int

    lost_copies: int

    damaged_copies: int

    reserved_copies: int

    minimum_threshold: int

    is_low_stock: bool


# =====================================
# BOOK SEARCH FILTER
# =====================================

class BookSearchFilter(BaseModel):

    category_id: Optional[int] = None

    title: Optional[str] = None

    author_name: Optional[str] = None

    isbn_number: Optional[str] = None

    subject_name: Optional[str] = None

    book_type: Optional[str] = None

    is_active: Optional[bool] = True