from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.services.dashboard_service import (
    DashboardService
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# =====================================
# DASHBOARD SUMMARY
# =====================================

@router.get("/summary")
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_dashboard_summary(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# LOW STOCK BOOKS
# =====================================

@router.get("/low-stock-books")
async def get_low_stock_books(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_low_stock_books(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# OVERDUE BOOKS
# =====================================

@router.get("/overdue-books")
async def get_overdue_books(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_overdue_books(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# PENDING FINES
# =====================================

@router.get("/pending-fines")
async def get_pending_fines(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_pending_fines(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# TOP BORROWED BOOKS
# =====================================

@router.get("/top-books")
async def get_top_books(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_top_books(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# ACTIVE BORROWERS
# =====================================

@router.get("/active-borrowers")
async def get_active_borrowers(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_active_borrowers(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# RECENT ISSUES
# =====================================

@router.get("/recent-issues")
async def get_recent_issues(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_recent_issues(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# RECENT RETURNS
# =====================================

@router.get("/recent-returns")
async def get_recent_returns(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_recent_returns(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# FINE COLLECTION
# =====================================

@router.get("/fine-collection")
async def get_fine_collection(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_fine_collection(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# LIBRARY UTILIZATION
# =====================================

@router.get("/library-utilization")
async def get_library_utilization(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_library_utilization(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# BLOCKED USERS
# =====================================

@router.get("/blocked-users")
async def get_blocked_users(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DashboardService
            .get_blocked_users(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )