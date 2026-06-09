from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification_model import Notification
from app.websocket.connection_manager import manager


class NotificationService:

    @staticmethod
    async def create_notification(
        db: AsyncSession,
        title: str,
        message: str,
        notification_type: str,
        recipient_role: str
    ):

        notification = Notification(
            title=title,
            message=message,
            notification_type=notification_type,
            recipient_role=recipient_role,
            is_read=False
        )

        db.add(notification)

        await db.commit()

        await db.refresh(notification)

        try:
            await manager.broadcast(
                {
                    "title": title,
                    "message": message,
                    "notification_type": notification_type,
                    "recipient_role": recipient_role
                }
            )
        except Exception:
            pass

        return notification