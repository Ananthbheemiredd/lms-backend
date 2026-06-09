from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


# =====================================
# Create Shelf
# =====================================

class ShelfCreate(BaseModel):

    school_id: int
    branch_id: int
    library_id: int

    floor_id: int
    rack_id: int

    shelf_name: str = Field(
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

    remarks: Optional[str] = Field(
        default=None,
        max_length=500
    )


# =====================================
# Update Shelf
# =====================================

class ShelfUpdate(BaseModel):

    shelf_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    remarks: Optional[str] = Field(
        default=None,
        max_length=500
    )

    is_active: Optional[bool] = None


# =====================================
# Shelf Response
# =====================================

class ShelfResponse(BaseModel):

    id: int

    school_id: int
    branch_id: int
    library_id: int

    floor_id: int
    rack_id: int

    shelf_code: str
    shelf_name: str

    description: Optional[str]
    remarks: Optional[str]

    creator_role: str

    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True