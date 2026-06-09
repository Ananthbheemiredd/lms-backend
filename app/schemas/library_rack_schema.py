from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ==========================
# Create Rack
# ==========================

class RackCreate(BaseModel):

    school_id: int
    branch_id: int
    library_id: int
    floor_id: int

    rack_name: str

    description: Optional[str] = None

    creator_role: str

    remarks: Optional[str] = None


# ==========================
# Update Rack
# ==========================

class RackUpdate(BaseModel):
    rack_name: Optional[str] = None
    description: Optional[str] = None
    remarks: Optional[str] = None
    is_active: Optional[bool] = None

# ==========================
# Response
# ==========================

class RackResponse(BaseModel):

    id: int

    school_id: int
    branch_id: int
    library_id: int
    floor_id: int

    rack_code: str
    rack_name: str

    description: Optional[str]
    remarks: Optional[str]

    creator_role: str

    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True