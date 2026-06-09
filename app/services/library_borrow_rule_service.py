from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.library_borrow_rule_model import (
    LibraryBorrowRule
)

from app.services.notification_service import (
    NotificationService
)


class LibraryBorrowRuleService:

    # =====================================
    # CREATE RULE
    # =====================================

    @staticmethod
    async def create_rule(
        db: AsyncSession,
        payload,
        created_by: int
    ):

        # -----------------------------
        # Duplicate Validation
        # -----------------------------

        existing_rule = await db.execute(
            select(LibraryBorrowRule).where(
                LibraryBorrowRule.school_id
                == payload.school_id,

                LibraryBorrowRule.branch_id
                == payload.branch_id,

                LibraryBorrowRule.library_id
                == payload.library_id,

                LibraryBorrowRule.borrower_type
                == payload.borrower_type
            )
        )

        if existing_rule.scalar_one_or_none():

            raise ValueError(
                f"{payload.borrower_type} "
                f"rule already exists"
            )

        # -----------------------------
        # Create Rule
        # -----------------------------

        rule = LibraryBorrowRule(
            school_id=payload.school_id,
            branch_id=payload.branch_id,
            library_id=payload.library_id,

            borrower_type=payload.borrower_type,

            max_books_allowed=(
                payload.max_books_allowed
            ),

            max_issue_days=(
                payload.max_issue_days
            ),

            fine_per_day=(
                payload.fine_per_day
            ),

            grace_days=(
                payload.grace_days
            ),

            creator_role=payload.creator_role,

            created_by=created_by
        )

        db.add(rule)

        await db.commit()

        await db.refresh(rule)

        # -----------------------------
        # Notification
        # -----------------------------

        await NotificationService.create_notification(
            db=db,
            title="Borrow Rule Created",
            message=(
                f"{payload.borrower_type} "
                f"borrow rule created successfully"
            ),
            notification_type="BORROW_RULE_CREATED",
            recipient_role=payload.creator_role
        )

        return rule

    # =====================================
    # GET ALL RULES
    # =====================================

    @staticmethod
    async def get_all_rules(
        db: AsyncSession
    ):

        result = await db.execute(
            select(LibraryBorrowRule)
        )

        return result.scalars().all()

    # =====================================
    # GET RULE BY ID
    # =====================================

    @staticmethod
    async def get_rule_by_id(
        db: AsyncSession,
        rule_id: int
    ):

        result = await db.execute(
            select(LibraryBorrowRule).where(
                LibraryBorrowRule.id == rule_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================
    # UPDATE RULE
    # =====================================

    @staticmethod
    async def update_rule(
        db: AsyncSession,
        rule_id: int,
        payload,
        updated_by: int
    ):

        rule = await (
            LibraryBorrowRuleService
            .get_rule_by_id(
                db,
                rule_id
            )
        )

        if not rule:
            return None

        # -----------------------------
        # Update Fields
        # -----------------------------

        if payload.max_books_allowed is not None:

            rule.max_books_allowed = (
                payload.max_books_allowed
            )

        if payload.max_issue_days is not None:

            rule.max_issue_days = (
                payload.max_issue_days
            )

        if payload.fine_per_day is not None:

            rule.fine_per_day = (
                payload.fine_per_day
            )

        if payload.grace_days is not None:

            rule.grace_days = (
                payload.grace_days
            )

        if payload.is_active is not None:

            rule.is_active = (
                payload.is_active
            )

        rule.updated_by = updated_by

        await db.commit()

        await db.refresh(rule)

        # -----------------------------
        # Notification
        # -----------------------------

        await NotificationService.create_notification(
            db=db,
            title="Borrow Rule Updated",
            message=(
                f"{rule.borrower_type} "
                f"borrow rule updated successfully"
            ),
            notification_type="BORROW_RULE_UPDATED",
            recipient_role=rule.creator_role
        )

        return rule

    # =====================================
    # DELETE RULE
    # =====================================

    @staticmethod
    async def delete_rule(
        db: AsyncSession,
        rule_id: int
    ):

        rule = await (
            LibraryBorrowRuleService
            .get_rule_by_id(
                db,
                rule_id
            )
        )

        if not rule:
            return False

        borrower_type = rule.borrower_type
        role = rule.creator_role

        await db.delete(rule)

        await db.commit()

        # -----------------------------
        # Notification
        # -----------------------------

        await NotificationService.create_notification(
            db=db,
            title="Borrow Rule Deleted",
            message=(
                f"{borrower_type} "
                f"borrow rule deleted successfully"
            ),
            notification_type="BORROW_RULE_DELETED",
            recipient_role=role
        )

        return True