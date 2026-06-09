from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BookSearchResponse(BaseModel):

    id: int

    school_id: int
    branch_id: int
    library_id: int

    category_id: int

    product_id: str
    book_code: str
    isbn_number: str

    title: str
    sub_title: Optional[str] = None

    author_name: str
    publisher_name: Optional[str] = None

    edition: Optional[str] = None
    language: Optional[str] = None

    subject_name: Optional[str] = None
    book_type: Optional[str] = None

    cover_image_url: Optional[str] = None

    quantity: int
    available_copies: int

    minimum_threshold: int

    lost_copies: int
    damaged_copies: int
    reserved_copies: int

    keywords: Optional[str] = None
    description: Optional[str] = None

    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True