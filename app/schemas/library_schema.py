from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class LibraryCreate(BaseModel):

    school_id: int
    branch_id: int

    library_name: str
    description: str | None = None

    creator_role: Literal[
        "ADMIN",
        "LIBRARIAN"
    ]

class LibraryUpdate(BaseModel):

    library_name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class LibraryResponse(BaseModel):

    id: int

    school_id: int
    branch_id: int

    library_code: str
    library_name: str

    description: str | None

    creator_role: str

    is_active: bool

    created_at: datetime

    class Config:
        from_attributes = True