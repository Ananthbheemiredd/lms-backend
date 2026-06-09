from datetime import datetime

from pydantic import BaseModel


# =====================================
# CREATE SCHOOL
# =====================================

class SchoolCreate(BaseModel):

    school_code: str

    school_name: str

    address: str | None = None

    is_active: bool = True


# =====================================
# UPDATE SCHOOL
# =====================================

class SchoolUpdate(BaseModel):

    school_name: str | None = None

    address: str | None = None

    is_active: bool | None = None


# =====================================
# RESPONSE
# =====================================

class SchoolResponse(BaseModel):

    id: int

    school_code: str

    school_name: str

    address: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True