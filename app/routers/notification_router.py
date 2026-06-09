from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.notification_model import Notification
from app.services.email_service import EmailService

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# =====================================
# Get All Notifications
# =====================================

@router.get("")
async def get_notifications(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Notification)
        .order_by(Notification.id.desc())
    )

    return result.scalars().all()


# =====================================
# Get Admin Notifications
# =====================================

@router.get("/admin")
async def get_admin_notifications(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Notification)
        .where(
            Notification.recipient_role == "ADMIN"
        )
        .order_by(Notification.id.desc())
    )

    return result.scalars().all()


# =====================================
# Get Librarian Notifications
# =====================================

@router.get("/librarian")
async def get_librarian_notifications(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Notification)
        .where(
            Notification.recipient_role == "LIBRARIAN"
        )
        .order_by(Notification.id.desc())
    )

    return result.scalars().all()


# =====================================
# Mark Notification As Read
# =====================================

@router.put(
    "/{notification_id}/read",
    status_code=status.HTTP_200_OK
)
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db)
):

    notification = await db.get(
        Notification,
        notification_id
    )

    if not notification:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    notification.is_read = True

    await db.commit()

    return {
        "success": True,
        "message": "Notification marked as read"
    }
@router.get("/test-email")
async def test_email():

    result = await EmailService.send_email(
        to_email="your-email@gmail.com",
        subject="LMS Test Email",
        body="<h1>Email Working Successfully</h1>"
    )

    return {
        "success": result
    }