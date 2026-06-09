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
# CREATE EMPLOYEE
# =====================================

class ProfileInformationCreate(BaseModel):

    school_id: int

    branch_id: int

    employee_code: str

    employee_name: str

    email: EmailStr

    mobile_number: Optional[str] = None

    department_name: Optional[str] = None

    designation: Optional[str] = None


# =====================================
# UPDATE EMPLOYEE
# =====================================

class ProfileInformationUpdate(BaseModel):

    employee_name: Optional[str] = None

    email: Optional[EmailStr] = None

    mobile_number: Optional[str] = None

    department_name: Optional[str] = None

    designation: Optional[str] = None

    is_library_blocked: Optional[bool] = None

    is_active: Optional[bool] = None


# =====================================
# RESPONSE
# =====================================

class ProfileInformationResponse(BaseModel):

    id: int

    school_id: int

    branch_id: int

    employee_code: str

    employee_name: str

    email: EmailStr

    mobile_number: Optional[str]

    department_name: Optional[str]

    designation: Optional[str]

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