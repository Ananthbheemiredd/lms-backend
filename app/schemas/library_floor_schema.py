from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FloorCreate(BaseModel):
    school_id: int
    branch_id: int
    library_id: int
    floor_name: str
    description: Optional[str] = None
    creator_role: str


class FloorUpdate(BaseModel):
    floor_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class FloorResponse(BaseModel):
    id: int

    school_id: int
    branch_id: int
    library_id: int

    floor_code: str
    floor_name: str
    description: Optional[str]

    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True