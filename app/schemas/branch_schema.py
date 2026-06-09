from datetime import datetime

from pydantic import BaseModel


class BranchCreate(BaseModel):

    school_id: int

    branch_code: str

    branch_name: str

    address: str | None = None

    is_active: bool = True


class BranchUpdate(BaseModel):

    branch_name: str | None = None

    address: str | None = None

    is_active: bool | None = None


class BranchResponse(BaseModel):

    id: int

    school_id: int

    branch_code: str

    branch_name: str

    address: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True