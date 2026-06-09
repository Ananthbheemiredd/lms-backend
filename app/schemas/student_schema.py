from datetime import (
    datetime,
    date
)

from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr
)


# =====================================
# CREATE STUDENT
# =====================================

class StudentCreate(BaseModel):

    school_id: int

    branch_id: int

    student_code: str

    student_name: str

    email: EmailStr

    mobile_number: Optional[str] = None

    class_name: Optional[str] = None

    section_name: Optional[str] = None


# =====================================
# UPDATE STUDENT
# =====================================

class StudentUpdate(BaseModel):

    student_name: Optional[str] = None

    email: Optional[EmailStr] = None

    mobile_number: Optional[str] = None

    class_name: Optional[str] = None

    section_name: Optional[str] = None

    is_library_blocked: Optional[bool] = None

    is_active: Optional[bool] = None


# =====================================
# RESPONSE
# =====================================

class StudentResponse(BaseModel):

    id: int

    school_id: int

    branch_id: int

    student_code: str

    student_name: str

    email: EmailStr

    mobile_number: Optional[str]

    class_name: Optional[str]

    section_name: Optional[str]

    current_borrowed_books: int

    pending_fine_amount: float

    allocated_book_codes: Optional[str]

    last_issue_date: Optional[date]

    last_return_date: Optional[date]

    is_library_blocked: bool

    is_active: bool

    created_at: datetime

    class Config:
        from_attributes = True