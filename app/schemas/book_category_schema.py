from datetime import datetime
from typing import Optional, Literal

from pydantic import (
    BaseModel,
    Field
)


# =====================================
# Create Category
# =====================================

class BookCategoryCreate(BaseModel):

    school_id: int
    branch_id: int
    library_id: int

    category_name: str = Field(
        min_length=2,
        max_length=150
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    creator_role: Literal[
        "ADMIN",
        "LIBRARIAN"
    ]


# =====================================
# Update Category
# =====================================

class BookCategoryUpdate(BaseModel):

    category_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    is_active: Optional[bool] = None


# =====================================
# Response
# =====================================

class BookCategoryResponse(BaseModel):

    id: int

    school_id: int
    branch_id: int
    library_id: int

    category_code: str
    category_name: str

    description: Optional[str]

    creator_role: str

    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True