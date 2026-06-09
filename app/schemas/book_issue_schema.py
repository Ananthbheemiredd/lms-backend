from datetime import (
    datetime,
    date
)

from typing import (
    Optional,
    Literal
)

from pydantic import (
    BaseModel,
    Field
)


# =====================================
# ISSUE BOOK
# =====================================

class BookIssueCreate(BaseModel):

    school_id: int
    branch_id: int
    library_id: int

    borrower_type: Literal[
        "STUDENT",
        "EMPLOYEE"
    ]

    student_id: Optional[int] = None

    employee_id: Optional[int] = None

    book_copy_id: int
    remarks: Optional[str] = None

    creator_role: Literal[
        "ADMIN",
        "LIBRARIAN"
    ]


# =====================================
# RETURN BOOK
# =====================================

class BookReturnUpdate(BaseModel):

    return_date: date

    fine_paid: bool = False

    remarks: Optional[str] = None


# =====================================
# UPDATE ISSUE STATUS
# =====================================

class BookIssueUpdate(BaseModel):

    issue_status: Optional[str] = Field(
        default=None,
        max_length=50
    )

    fine_amount: Optional[float] = Field(
        default=None,
        ge=0
    )
    fine_paid: Optional[bool] = None

    remarks: Optional[str] = None


# =====================================
# RESPONSE
# =====================================

class BookIssueResponse(BaseModel):

    id: int

    school_id: int
    branch_id: int
    library_id: int

    borrower_type: str

    student_id: Optional[int]

    employee_id: Optional[int]

    book_id: int

    book_copy_id: int

    issue_date: date

    due_date: date

    return_date: Optional[date]

    issue_status: str

    fine_amount: float

    fine_paid: bool

    fine_paid_date: Optional[date]

    remarks: Optional[str]

    creator_role: str

    issued_by: Optional[int]

    returned_by: Optional[int]
    renew_count: int

    fine_collected_by: Optional[int]

    is_active: bool

    return_remarks: Optional[str]

    created_at: datetime
    updated_at: datetime
    return_remarks: Optional[str]


    fine_collected_by: Optional[int]


    class Config:
        from_attributes = True