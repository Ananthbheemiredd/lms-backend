from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.database.session import (
    get_db
)

from app.schemas.branch_schema import (

    BranchCreate,

    BranchUpdate,

    BranchResponse
)

from app.services.branch_service import (
    BranchService
)

router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)


# =====================================
# CREATE BRANCH
# =====================================

@router.post(
    "",
    response_model=BranchResponse
)
async def create_branch(
    payload: BranchCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        branch = await (
            BranchService.create_branch(
                db,
                payload
            )
        )

        return branch

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =====================================
# GET ALL BRANCHES
# =====================================

@router.get(
    "",
    response_model=List[BranchResponse]
)
async def get_all_branches(
    db: AsyncSession = Depends(get_db)
):

    return await (
        BranchService.get_all_branches(
            db
        )
    )


# =====================================
# GET BRANCHES BY SCHOOL
# =====================================

@router.get(
    "/school/{school_id}",
    response_model=List[BranchResponse]
)
async def get_branches_by_school(
    school_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await (
        BranchService.get_branches_by_school(
            db,
            school_id
        )
    )


# =====================================
# UPDATE BRANCH
# =====================================

@router.put(
    "/{branch_id}",
    response_model=BranchResponse
)
async def update_branch(
    branch_id: int,
    payload: BranchUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            BranchService.update_branch(
                db,
                branch_id,
                payload
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )