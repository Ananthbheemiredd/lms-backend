from datetime import datetime
from typing import Optional, Literal

from pydantic import (
    BaseModel,
    Field
)


# =====================================
# Create Row
# =====================================

class RowCreate(BaseModel):

    school_id: int
    branch_id: int
    library_id: int

    floor_id: int
    rack_id: int
    shelf_id: int

    row_name: str = Field(
        min_length=2,
        max_length=150
    )

    capacity: int = Field(
        default=100,
        ge=1
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
# Update Row
# =====================================

class RowUpdate(BaseModel):

    row_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    capacity: Optional[int] = Field(
        default=None,
        ge=1
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    is_active: Optional[bool] = None


# =====================================
# Response
# =====================================

class RowResponse(BaseModel):

    id: int

    school_id: int
    branch_id: int
    library_id: int

    floor_id: int
    rack_id: int
    shelf_id: int

    row_code: str
    row_name: str

    capacity: int

    description: Optional[str]

    creator_role: str

    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True