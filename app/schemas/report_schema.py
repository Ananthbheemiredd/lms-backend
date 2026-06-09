from datetime import date

from pydantic import BaseModel


# =====================================
# INVENTORY REPORT
# =====================================

class InventoryReportResponse(BaseModel):

    book_id: int

    title: str

    author_name: str

    quantity: int

    available_copies: int

    lost_copies: int

    damaged_copies: int

    reserved_copies: int

    low_stock_alert: bool

# =====================================
# OVERDUE REPORT
# =====================================

class OverdueReportResponse(BaseModel):

    issue_id: int

    book_id: int

    borrower_type: str

    student_id: int | None = None

    employee_id: int | None = None

    issue_date: date

    due_date: date

    days_overdue: int


# =====================================
# FINE REPORT
# =====================================

class FineReportResponse(BaseModel):

    issue_id: int

    book_id: int

    borrower_type: str

    student_id: int | None = None

    employee_id: int | None = None

    fine_amount: float

    fine_paid: bool

    fine_paid_date: date | None = None


# =====================================
# RETURN REPORT
# =====================================

class ReturnReportResponse(BaseModel):

    issue_id: int

    book_id: int

    borrower_type: str

    student_id: int | None = None

    employee_id: int | None = None

    issue_date: date

    due_date: date

    return_date: date | None = None

    fine_amount: float


# =====================================
# DASHBOARD REPORT
# =====================================

class DashboardReportResponse(BaseModel):

    total_books: int

    total_available_books: int

    total_issued_books: int

    total_returned_books: int

    total_overdue_books: int

    total_pending_fines: float