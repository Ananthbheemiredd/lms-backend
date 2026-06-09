from datetime import date
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.database.session import (
    get_db
)

from app.services.report_service import (
    ReportService
)

from app.schemas.book_issue_schema import (
    BookIssueResponse
)

from app.schemas.report_schema import (
    InventoryReportResponse,
    OverdueReportResponse,
    ReturnReportResponse,
    FineReportResponse,
    DashboardReportResponse
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# =====================================
# ISSUE REPORT
# =====================================

@router.get(
    "/issues",
    response_model=List[BookIssueResponse]
)
async def get_issue_report(

    from_date: date | None = Query(None),
    to_date: date | None = Query(None),

    student_id: int | None = Query(None),
    employee_id: int | None = Query(None),

    book_id: int | None = Query(None),

    issue_status: str | None = Query(None),

    borrower_type: str | None = Query(None),

    db: AsyncSession = Depends(get_db)
):

    try:

        return await ReportService.get_issue_report(
            db=db,
            from_date=from_date,
            to_date=to_date,
            student_id=student_id,
            employee_id=employee_id,
            book_id=book_id,
            issue_status=issue_status,
            borrower_type=borrower_type
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =====================================
# INVENTORY REPORT
# =====================================

@router.get(
    "/inventory",
    response_model=List[InventoryReportResponse]
)
async def get_inventory_report(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await ReportService.get_inventory_report(
            db
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =====================================
# OVERDUE REPORT
# =====================================

@router.get(
    "/overdue",
    response_model=List[OverdueReportResponse]
)
async def get_overdue_report(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await ReportService.get_overdue_report(
            db
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =====================================
# RETURN REPORT
# =====================================

@router.get(
    "/returns",
    response_model=List[ReturnReportResponse]
)
async def get_return_report(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await ReportService.get_return_report(
            db
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =====================================
# FINE REPORT
# =====================================

@router.get(
    "/fines",
    response_model=List[FineReportResponse]
)
async def get_fine_report(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await ReportService.get_fine_report(
            db
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =====================================
# DASHBOARD REPORT
# =====================================

@router.get(
    "/dashboard",
    response_model=DashboardReportResponse
)
async def get_dashboard_report(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await ReportService.get_dashboard_report(
            db
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )