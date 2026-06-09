from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.book_issue_schema import (
    BookIssueCreate,
    BookIssueResponse,
    BookReturnUpdate
)

from app.services.book_issue_service import (
    BookIssueService
)

router = APIRouter(
    prefix="/book-issues",
    tags=["Book Issues"]
)


# =====================================
# ISSUE BOOK
# =====================================

@router.post(
    "",
    response_model=BookIssueResponse,
    status_code=status.HTTP_201_CREATED
)
async def issue_book(
    payload: BookIssueCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        issue = await (
            BookIssueService.issue_book(
                db=db,
                payload=payload,
                issued_by=1
                # current_user.id
            )
        )

        return issue

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to issue book: {str(e)}"
        )


# =====================================
# RETURN BOOK
# =====================================

@router.put(
    "/return/{issue_id}",
    response_model=BookIssueResponse
)
async def return_book(
    issue_id: int,
    payload: BookReturnUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        issue = await (
            BookIssueService.return_book(
                db=db,
                issue_id=issue_id,
                payload=payload,
                returned_by=1
                # current_user.id
            )
        )

        return issue

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to return book: {str(e)}"
        )


# =====================================
# GET ALL ISSUES
# =====================================

@router.get(
    "",
    response_model=List[BookIssueResponse]
)
async def get_all_issues(
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService.get_all_issues(
                db
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch issues: {str(e)}"
        )

# =====================================
# GET ACTIVE ISSUES
# =====================================

@router.get(
    "/active",
    response_model=List[BookIssueResponse]
)
async def get_active_issues(
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService.get_active_issues(
                db
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =====================================
# GET ISSUE BY ID
# =====================================

@router.get(
    "/{issue_id}",
    response_model=BookIssueResponse
)
async def get_issue_by_id(
    issue_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issue = await (
            BookIssueService.get_issue_by_id(
                db,
                issue_id
            )
        )

        if not issue:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Issue record not found"
            )

        return issue

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch issue: {str(e)}"
        )


# =====================================
# GET STUDENT ISSUES
# =====================================

@router.get(
    "/student/{student_id}",
    response_model=List[BookIssueResponse]
)
async def get_student_issues(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService.get_student_issues(
                db,
                student_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                f"Failed to fetch "
                f"student issues: {str(e)}"
            )
        )


# =====================================
# GET EMPLOYEE ISSUES
# =====================================

@router.get(
    "/employee/{employee_id}",
    response_model=List[BookIssueResponse]
)
async def get_employee_issues(
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService.get_employee_issues(
                db,
                employee_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                f"Failed to fetch "
                f"employee issues: {str(e)}"
            )
        )


# =====================================
# GET OVERDUE BOOKS
# =====================================

@router.get(
    "/reports/overdue",
    response_model=List[BookIssueResponse]
)
async def get_overdue_books(
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService.get_overdue_books(
                db
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                f"Failed to fetch "
                f"overdue books: {str(e)}"
            )
        )


# =====================================
# GET PENDING FINES
# =====================================

@router.get(
    "/reports/pending-fines",
    response_model=List[BookIssueResponse]
)
async def get_pending_fines(
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService.get_pending_fines(
                db
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                f"Failed to fetch "
                f"pending fines: {str(e)}"
            )
        )
# =====================================
# STUDENT OVERDUE BOOKS
# =====================================

@router.get(
    "/student/{student_id}/overdue",
    response_model=List[BookIssueResponse]
)
async def get_student_overdue_books(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService
            .get_student_overdue_books(
                db,
                student_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# STUDENT PENDING FINES
# =====================================

@router.get(
    "/student/{student_id}/pending-fines",
    response_model=List[BookIssueResponse]
)
async def get_student_pending_fines(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService
            .get_student_pending_fines(
                db,
                student_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# STUDENT ACTIVE BOOKS
# =====================================

@router.get(
    "/student/{student_id}/active-books",
    response_model=List[BookIssueResponse]
)
async def get_student_active_books(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService
            .get_student_active_books(
                db,
                student_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# EMPLOYEE OVERDUE BOOKS
# =====================================

@router.get(
    "/employee/{employee_id}/overdue",
    response_model=List[BookIssueResponse]
)
async def get_employee_overdue_books(
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService
            .get_employee_overdue_books(
                db,
                employee_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# EMPLOYEE PENDING FINES
# =====================================

@router.get(
    "/employee/{employee_id}/pending-fines",
    response_model=List[BookIssueResponse]
)
async def get_employee_pending_fines(
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService
            .get_employee_pending_fines(
                db,
                employee_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# EMPLOYEE ACTIVE BOOKS
# =====================================

@router.get(
    "/employee/{employee_id}/active-books",
    response_model=List[BookIssueResponse]
)
async def get_employee_active_books(
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService
            .get_employee_active_books(
                db,
                employee_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =====================================
# DELETE ISSUE
# =====================================

@router.delete("/{issue_id}")
async def delete_issue(
    issue_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        deleted = await (
            BookIssueService.delete_issue(
                db,
                issue_id
            )
        )

        if not deleted:

            raise HTTPException(
                status_code=404,
                detail="Issue not found"
            )

        return {
            "status": "success",
            "message":
                "Issue deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =====================================
# PAY FINE
# =====================================

@router.put(
    "/pay-fine/{issue_id}",
    response_model=BookIssueResponse
)
async def pay_fine(
    issue_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issue = await (
            BookIssueService.pay_fine(
                db,
                issue_id
            )
        )

        return issue

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =====================================
# STUDENT HISTORY
# =====================================

@router.get(
    "/student/{student_id}/history",
    response_model=List[BookIssueResponse]
)
async def get_student_history(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService.get_student_history(
                db,
                student_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# EMPLOYEE HISTORY
# =====================================

@router.get(
    "/employee/{employee_id}/history",
    response_model=List[BookIssueResponse]
)
async def get_employee_history(
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):

    try:

        issues = await (
            BookIssueService.get_employee_history(
                db,
                employee_id
            )
        )

        return issues

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )