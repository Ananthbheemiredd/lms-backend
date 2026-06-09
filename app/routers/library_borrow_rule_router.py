from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.library_borrow_rule_schema import (
    LibraryBorrowRuleCreate,
    LibraryBorrowRuleUpdate,
    LibraryBorrowRuleResponse
)

from app.services.library_borrow_rule_service import (
    LibraryBorrowRuleService
)

router = APIRouter(
    prefix="/borrow-rules",
    tags=["Library Borrow Rules"]
)


# =====================================
# CREATE RULE
# =====================================

@router.post(
    "",
    response_model=LibraryBorrowRuleResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_rule(
    payload: LibraryBorrowRuleCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryBorrowRuleService
            .create_rule(
                db=db,
                payload=payload,
                created_by=1
                # current_user.id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create rule: {str(e)}"
        )


# =====================================
# GET ALL RULES
# =====================================

@router.get(
    "",
    response_model=List[LibraryBorrowRuleResponse]
)
async def get_all_rules(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            LibraryBorrowRuleService
            .get_all_rules(db)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch rules: {str(e)}"
        )


# =====================================
# GET RULE BY ID
# =====================================

@router.get(
    "/{rule_id}",
    response_model=LibraryBorrowRuleResponse
)
async def get_rule_by_id(
    rule_id: int,
    db: AsyncSession = Depends(get_db)
):

    rule = await (
        LibraryBorrowRuleService
        .get_rule_by_id(
            db,
            rule_id
        )
    )

    if not rule:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrow rule not found"
        )

    return rule


# =====================================
# UPDATE RULE
# =====================================

@router.put(
    "/{rule_id}",
    response_model=LibraryBorrowRuleResponse
)
async def update_rule(
    rule_id: int,
    payload: LibraryBorrowRuleUpdate,
    db: AsyncSession = Depends(get_db)
):

    rule = await (
        LibraryBorrowRuleService
        .update_rule(
            db=db,
            rule_id=rule_id,
            payload=payload,
            updated_by=1
            # current_user.id
        )
    )

    if not rule:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrow rule not found"
        )

    return rule


# =====================================
# DELETE RULE
# =====================================

@router.delete(
    "/{rule_id}"
)
async def delete_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted = await (
        LibraryBorrowRuleService
        .delete_rule(
            db,
            rule_id
        )
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrow rule not found"
        )

    return {
        "message":
            "Borrow rule deleted successfully"
    }